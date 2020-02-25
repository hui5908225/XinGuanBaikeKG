
import requests
from bs4 import BeautifulSoup
import bs4
import lxml
import os
import re
import json
from urllib.parse import urljoin, quote, unquote


data1 = set()
data2 = set()
data3 = set()

with open('E:\Monash\Coronavirus\crawler\seperateclass\医学百科_疾病jiao.txt', 'r') as f:
    i = f.readline()
    i = i.split('\n')[0]
    data1.add(i)
    i = f.readline()
    while(i != ''):
        i = i.split('\n')[0]
        data1.add(i)
        i = f.readline()

with open('E:\Monash\Coronavirus\crawler\seperateclass\医学百科_病毒jiao.txt', 'r') as f:
    i = f.readline()
    i = i.split('\n')[0]
    data2.add(i)
    i = f.readline()
    while(i != ''):
        i = i.split('\n')[0]
        data2.add(i)
        i = f.readline()

with open('E:\Monash\Coronavirus\crawler\firstrounddata\医学百科_细菌jiao', 'r') as f:
    i = f.readline()
    i = i.split('\n')[0]
    data3.add(i)
    i = f.readline()
    while(i != ''):
        i = i.split('\n')[0]
        data3.add(i)
        i = f.readline()

wholedata = set()
wholedata = data1 | data2 | data3


def have_next(ele):
    try:
        ele.next()
    except:
        return False
    return True

def is_child(child, father):
    if child in father:
        return True
    seek_list = father.contents
    for i in seek_list:
        if isinstance(i, bs4.element.NavigableString):
            pass
        elif child in i:
            return True
        else:
            flag = is_child(child, i)
            if flag == True:
                return True
    return False

def get_content_between_tables(pre, nxt):
    #如果第二个table在第一个里面
    txt = ""
    if is_child(nxt, pre):
        cur = pre.next_element
        while cur != nxt and cur is not None:
            if isinstance(cur, bs4.element.NavigableString):
                txt += cur
            cur = cur.next_element
    #类似并列关系
    else:
        #先找到pre结束的下一个元素
        cur = pre.next_element
        while is_child(cur, pre):
            cur = cur.next_element
        #获取内容
        while cur != nxt and cur is not None:
            if isinstance(cur, bs4.element.NavigableString):
                txt += cur
            cur = cur.next_element
    return txt

def findrelation(page_source,title):
    page_source = re.sub(title, '<a href="/w/' + title+ '" >'+ title + '</a>', page_source)
    page_source = re.sub('[这]', '<a href="/w/' + title+ '" >'+ title + '</a>', page_source)
    html = BeautifulSoup(page_source, 'lxml')
    url = html.find_all('a')
    texts = []
    for i in range(len(url)-1):
        txt = get_content_between_tables(url[i], url[i+1] )
        reg1 = r'[!。；， ：,.?:;\n]'
        pattern = re.compile(reg1)
        if len(pattern.findall(txt)) < 1:
            try:
                line = 'head:' +  unquote(str(url[i]['href']).split('/w/')[1]) +  '\t'+ '\t'+'tail' + unquote(str(url[i+1]['href']).split('/w/')[1]) + '\t'+ '\t'+'rel:'+  str(txt)
                if unquote(str(url[i]['href']).split('/w/')[1]) in wholedata or unquote(str(url[i+1]['href']).split('/w/')[1]) in wholedata:
                    texts.append(line)
            except:
                continue
    return texts



