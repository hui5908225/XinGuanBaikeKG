from bs4 import BeautifulSoup
import bs4
import lxml
import os
import re
import json
from urllib.parse import urljoin, quote, unquote
import os
from process.process_utils import get_triple

def clean(s):
    s = re.sub(r'\s+', '', s)
    if s.endswith('：'):
        s = s[:-1]
    s = s.replace('[', '')
    s = s.replace(']', '')
    s = s.replace('(', '')
    s = s.replace(')', '')
    return s

data1 = set()
data2 = set()
data3 = set()
data4 = set()
data5 = set()
data6 = set()
data7 = set()

name_dict = []
for i in range(1,13):
    file_name = 'entity_names_' + str(i) + '.json'
    with open(os.path.join('../data/xinguan_hudongbaike/entity_names', file_name), 'r', encoding='utf-8') as f:
        name_dict.append(json.load(f))
        f.close()

with open(os.path.join('../data/xinguan_hudongbaike/entity_type', 'new_bacteria.txt'), 'r', encoding='utf-8') as f:
    i = f.readline()
    i = i.split('\n')[0]
    data1.add(i)
    i = f.readline()
    while(i != ''):
        i = i.split('\n')[0]
        data1.add(i)
        i = f.readline()

with open(os.path.join('../data/xinguan_hudongbaike/entity_type', 'new_disease.txt'), 'r', encoding='utf-8') as f:
    i = f.readline()
    i = i.split('\n')[0]
    data2.add(i)
    i = f.readline()
    while(i != ''):
        i = i.split('\n')[0]
        data2.add(i)
        i = f.readline()

with open(os.path.join('../data/xinguan_hudongbaike/entity_type', 'new_drug.txt'), 'r', encoding='utf-8') as f:
    i = f.readline()
    i = i.split('\n')[0]
    data3.add(i)
    i = f.readline()
    while(i != ''):
        i = i.split('\n')[0]
        data3.add(i)
        i = f.readline()

with open(os.path.join('../data/xinguan_hudongbaike/entity_type', 'new_inspect.txt'), 'r', encoding='utf-8') as f:
    i = f.readline()
    i = i.split('\n')[0]
    data4.add(i)
    i = f.readline()
    while(i != ''):
        i = i.split('\n')[0]
        data4.add(i)
        i = f.readline()

with open(os.path.join('../data/xinguan_hudongbaike/entity_type', 'new_speciaty.txt'), 'r', encoding='utf-8') as f:
    i = f.readline()
    i = i.split('\n')[0]
    data5.add(i)
    i = f.readline()
    while(i != ''):
        i = i.split('\n')[0]
        data5.add(i)
        i = f.readline()

with open(os.path.join('../data/xinguan_hudongbaike/entity_type', 'new_symptom.txt'), 'r', encoding='utf-8') as f:
    i = f.readline()
    i = i.split('\n')[0]
    data6.add(i)
    i = f.readline()
    while(i != ''):
        i = i.split('\n')[0]
        data6.add(i)
        i = f.readline()

with open(os.path.join('../data/xinguan_hudongbaike/entity_type', 'new_virus.txt'), 'r', encoding='utf-8') as f:
    i = f.readline()
    i = i.split('\n')[0]
    data7.add(i)
    i = f.readline()
    while(i != ''):
        i = i.split('\n')[0]
        data7.add(i)
        i = f.readline()

wholedata = set()
wholedata = data1 | data2 | data3 | data4 | data5 | data6 | data7


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

def findrelation(page_source, title):
    for dict in name_dict:
        name_list = dict.get(title, [])
        if len(name_list) != 0:
            break
    title = clean(title)
    print(title)
    for name in name_list:
        page_source = re.sub(clean(name), '<a class = "innerlink" title = '+title+'>' + '</a>', page_source)
    page_source = re.sub('[这]', '<a class = "innerlink" title = '+title+'>'+ title + '</a>', page_source)
    page_source = re.sub('[该]', '<a class = "innerlink" title = '+title+'>' + title + '</a>', page_source)
    page_source = re.sub('[此]', '<a class = "innerlink" title = '+title+'>' + title + '</a>', page_source)
    page_source = re.sub('[它]', '<a class = "innerlink" title = '+title+'>' + title + '</a>', page_source)
    html = BeautifulSoup(page_source, 'lxml')
    url = html.find_all('a',{'class':'innerlink'})
    texts = []
    for i in range(len(url)-1):
        txt = get_content_between_tables(url[i], url[i+1] )
        reg1 = r'[!。；， ：,.?:;\n]'
        pattern = re.compile(reg1)
        if len(pattern.findall(txt)) < 1:
            try:
                line = unquote(str(url[i]['title'])) + ';;;;ll;;;;'+ unquote(str(url[i+1]['title'])) + ';;;;ll;;;;'+ str(txt)
                texts.append(line)
            except:
                continue
    return texts

if __name__ == '__main__':
    wf = open(os.path.join('../data/xinguan_hudongbaike/entity_sentence', 'hudongbaike_sentence.txt'), 'a', encoding='utf-8')
    # i = 1,2 ...,12
    i = 12
    file_name = 'entity_pages_' + str(i) + '.xml'
    inner_link_dict = {}
    with open(os.path.join('../data/xinguan_hudongbaike/entity_page', file_name), 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
        all_page = soup.find_all('page')
        for page in all_page:
            inner_link_set = set()
            if page.title:
                list = findrelation(str(page), page.title.string)
                for triple in list:
                    s, p, o = get_triple(triple)
                    if s in wholedata and p in wholedata:
                        if o not in ['[', ']', '']:
                            wf.write(triple + '\n')
