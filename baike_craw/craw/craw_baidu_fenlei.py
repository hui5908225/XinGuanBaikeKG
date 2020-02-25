from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import time
import queue
import os
import json
from operator import itemgetter
import threading
from craw.craw_utils import get_html, sep

# 爬取百科所有分类



#保存所有分类
all_fenlei = set()
#当前工作队列
work_list = queue.Queue()
#subclass二元关系
fenlei_subclass_bigram = set()
#相关分类二元关系
fenlei_related_bigram = set()
#失败列表
failed_list = list()
#特定分类下entity的url信息
fenlei_entity_url = {}
#特定分类下entity的开放分类信息
fenlei_entity_ca = {}
#特定分类url
fenlei_url_dict = {}
#特殊页
special_page = {}

# 返回None 页面链接失败 返回1 页面处理成功
def get_in_fenlei(fenlei):
    time.sleep(0.5)
    fenlei_quote = urllib.parse.quote(fenlei)
    fenlei_url = 'http://baike.baidu.com/fenlei/%s' %fenlei_quote
    url_suffix = '?limit=10000'
    html = get_html(fenlei_url + url_suffix)
    if not html:
        print('FAILED:', fenlei)
        failed_list.append(fenlei)
        return None

    entity2category_dict = {}
    entity2url_dict = {}
    fenlei_url_dict[fenlei] = fenlei_url
    # 获取分类信息
    soup = BeautifulSoup(html, 'html.parser')
    special_soup = soup.findAll('div', {'class': 'category-title p-category-relation'})
    if len(special_soup) != 0 :
        print("special page: " + fenlei + '\n' + fenlei_url + '\n')
        special_page[fenlei] = fenlei_url
        for spe_div in special_soup:
            subclass = spe_div.find('span', {'class' : 'inner'}).get_text()
            fenlei_subclass_bigram.add((fenlei, subclass))
            if subclass not in all_fenlei:
                all_fenlei.add(subclass)
                work_list.put(subclass)
            subsubclasses_tag = spe_div.find_all('a', {'class' : 'child-link nslog:7449'})
            for subsubclass_tag in subsubclasses_tag:
                subsubclass = subsubclass_tag.get_text()
                fenlei_subclass_bigram.add((subclass, subsubclass))
                if subsubclass not in all_fenlei:
                    all_fenlei.add(subsubclass)
                    work_list.put(subsubclass)
    else:
        fenlei_soup = soup.findAll('div', {'class': 'category-title'})
        if fenlei_soup is not None:
            if len(fenlei_soup) == 2:
                sub_items = fenlei_soup[0].find_all('a')
                for item in sub_items:
                    text = item.get_text()
                    fenlei_subclass_bigram.add((fenlei, text))
                    if text not in all_fenlei:
                        all_fenlei.add(text)
                        work_list.put(text)
                # related_items = fenlei_soup[1].find_all('a')
                # for item in related_items:
                #     text = item.get_text()
                #     fenlei_related_bigram.add((fenlei, text))
                #     if text not in all_fenlei:
                #         all_fenlei.add(text)
                #         work_list.put(text)
            if fenlei_soup == 1:
                related_items = fenlei_soup[0].find_all('a')
                for item in related_items:
                    text = item.get_text()
                    fenlei_related_bigram.add((fenlei, text))
                    if text not in all_fenlei:
                        all_fenlei.add(text)
                        work_list.put(text)

            print('FENLEI:%s, all_fenlei size:%d, rest in work_list:%d' %
                  (fenlei, len(all_fenlei), work_list.qsize()))


        #获取entity信息
        #从hotcontent中获取
        hot_soup = soup.findAll('div', {'class': 'hotcontent'})
        if len(hot_soup) != 0 :
            for entity in hot_soup:
                a = entity.findAll('a')
                url = a[0].get('href')
                name = a[0].get_text()
                ca_list = []
                for index in range(1,len(a)):
                    ca_list.append(a[index].get_text())
                entity2url_dict[name] = url
                entity2category_dict[name] = ca_list

        #从list中获取
        entity_soup = soup.findAll('div', {'class': 'list'})
        for entity in entity_soup:
            name = entity.find('a', {'class': 'title nslog:7450'}).get_text()
            url = entity.find('a', {'class': 'title nslog:7450'}).get('href')
            entity2url_dict[name] = url
            open_ca_div = entity.find('div', {'class': 'text'})
            open_ca = open_ca_div.findAll('a')
            ca_list = []
            for ca in open_ca:
                ca_list.append(ca.get_text())
            entity2category_dict[name] = ca_list
        fenlei_entity_url[fenlei] = entity2url_dict
        fenlei_entity_ca[fenlei] = entity2category_dict
    return 1

# In[5]:

# 种子类别
seeds = [
    # ('自然', '天文'),
    # ('文化', '文化遗产'),
    # ('地理', '地形地貌'),
    # ('历史', '历史事件'),
    # ('生活', '娱乐'),
    # ('社会', '军事'),
    # ('艺术', '绘画'),
    # ('经济', '金融'),
    # ('科学', '自然科学'),
    # ('自然科学', '数学'),
    # ('体育', '体育运动')
    # ('生活', '健康')

    #向下爬
    ('TOP', '病毒'),
    ('TOP', '疾病'),
    ('TOP', '细菌'),
    ('TOP', '药品'),
    ('TOP', '症状'),
    ('TOP', '医疗'),
    ('TOP', '医学'),
    ('TOP', '健康')
]

# 种子bigram加入
for seed in seeds:
    fenlei_subclass_bigram.add(seed)
    # all_fenlei.add(seed[0])
    all_fenlei.add(seed[1])
    work_list.put(seed[1])


# 线程运行函数 从队列中不断获取fenlei
def download_from_work_list(Q):
    while not Q.empty():
        fenlei = Q.get()
        get_in_fenlei(fenlei)

# 线程运行函数 从失败队列中不断获取fenlei
def download_from_failed_work_list(Q):
    while not Q.empty():
        fenlei = Q.get()
        output = get_in_fenlei(fenlei)
        if output is not None:
            failed_list.remove(fenlei)


# 设置三个线程运行
threads = []
for i in range(3):
    t = threading.Thread(target=download_from_work_list, args=(work_list,))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

# In[7]:


# 对失败的类别，多进行十次尝试
if len(failed_list) != 0:
    for i in range(10):
        for fen in failed_list:
            work_list.put(fen)

        threads = []
        for i in range(3):
            t = threading.Thread(target=download_from_failed_work_list, args=(work_list,))
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()


with open(os.path.join('../data/xinguan_baidubaike', 'baidubaike_fenlei_failed_list.txt'), 'w', encoding='utf-8') as f:
    for failed_item in failed_list:
        f.write(failed_item + '\n')

print(failed_list)


print(len(failed_list))
print(len(fenlei_subclass_bigram))


# 转为list 排序
fenlei_subclass_bigram_list = list(fenlei_subclass_bigram)
fenlei_subclass_bigram_list.sort(key=itemgetter(0))

#转为list 排序
fenlei_related_bigram_list = list(fenlei_related_bigram)
fenlei_related_bigram_list.sort(key=itemgetter(0))

#存subclass 二元关系
with open(os.path.join('../data/xinguan_baidubaike', 'baidubaike_fenlei_subclass_bigram.txt'), 'w', encoding='utf-8') as f:
    for father, child in fenlei_subclass_bigram_list:
        f.write(father + sep + child + '\n')

#存related 二元关系
# with open(os.path.join('../data/xinguan_baidubaike', 'baidubaike_fenlei_related_bigram.txt'), 'w', encoding='utf-8') as f:
#     for bro_1, bro_2 in fenlei_related_bigram_list:
#         f.write(bro_1 + sep + bro_2 + '\n')

#存实体的开放分类
with open(os.path.join('../data/xinguan_baidubaike', 'baidubaike_fenlei_entity_ca.json'), 'w', encoding='utf-8') as f:
    json.dump(fenlei_entity_ca, f, ensure_ascii=False, indent=4)

#存实体的url
with open(os.path.join('../data/xinguan_baidubaike', 'baidubaike_fenlei_entity_url.json'), 'w', encoding='utf-8') as f:
    json.dump(fenlei_entity_url, f, ensure_ascii=False, indent=4)

#存分类的url
with open(os.path.join('../data/xinguan_baidubaike', 'baidubaike_fenlei_url.json'), 'w', encoding='utf-8') as f:
    json.dump(fenlei_url_dict, f, ensure_ascii=False, indent=4)

#存分类
with open(os.path.join('../data/xinguan_baidubaike', 'baidubaike_fenlei.txt'), 'w', encoding='utf-8') as f:
    fenlei = set()
    for sup, sub in fenlei_subclass_bigram_list:
        fenlei.add(sup)
        fenlei.add(sub)
    fenlei_list = list(fenlei)
    for fe in fenlei_list:
        f.write(fe + '\n')

#存特殊页面
with open(os.path.join('../data/xinguan_baidubaike', 'baidubaike_special_fenlei_page.json'), 'w', encoding='utf-8') as f:
    json.dump(special_page, f, ensure_ascii=False, indent=4)



