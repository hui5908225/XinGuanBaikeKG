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
import re

#保存所有分类
all_fenlei = set()
#当前工作队列
work_list = queue.Queue()
#subclass二元关系
fenlei_subclass_bigram = set()
#相关分类二元关系
#fenlei_related_bigram = set()
#失败列表
failed_list = list()
#特定分类url
fenlei_url_dict = {}
pattern = r"医院"



def get_in_fenlei(fenlei):
    time.sleep(0.5)
    fenlei_quote = urllib.parse.quote(fenlei)
    fenlei_url = 'http://fenlei.baike.com/%s/' %fenlei_quote
    html = get_html(fenlei_url)
    if not html:
        print('FAILED:', fenlei)
        failed_list.append(fenlei)
        return None

    fenlei_url_dict[fenlei] = fenlei_url
    # 获取分类
    soup = BeautifulSoup(html, 'html.parser')
    fenlei_soup = soup.find('div', {'class': 'sort'})
    if fenlei_soup is not None:
        # #上一级 下一级 相关
        #         # if len(fenlei_soup.find_all('h3')) == 3:
        #         #     sub_p = fenlei_soup.find_all('p')[1]
        #         #     sub_items = sub_p.find_all('a')
        #         #     for item in sub_items:
        #         #         text = item.get_text()
        #         #         fenlei_subclass_bigram.add((fenlei, text))
        #         #         if text not in all_fenlei:
        #         #             all_fenlei.add(text)
        #         #             work_list.put(text)
        #         #
        #         #     related_p = fenlei_soup.find_all('p')[2]
        #         #     related_items = related_p.find_all('a')
        #         #     for item in related_items:
        #         #         text = item.get_text()
        #         #         fenlei_related_bigram.add((fenlei, text))
        #         #         if text not in all_fenlei:
        #         #             all_fenlei.add(text)
        #         #             work_list.put(text)
        #上一级 下一级
        if len(fenlei_soup.find_all('h3')) >= 2:
            sub_p = fenlei_soup.find_all('p')[1]
            sub_items = sub_p.find_all('a')
            for item in sub_items:
                text = item.get_text()
                if re.search(pattern, text) is None:
                    fenlei_subclass_bigram.add((fenlei, text))
                    if text not in all_fenlei:
                        all_fenlei.add(text)
                        work_list.put(text)

        print('FENLEI:%s, all_fenlei size:%d, rest in work_list:%d' %
              (fenlei, len(all_fenlei), work_list.qsize()))
        return 1

# In[5]:

#百科种子
# seeds = [
#     ('TOP', '自然'),
#     ('TOP', '文化'),
#     ('TOP', '人物'),
#     ('TOP', '历史'),
#     ('TOP', '生活'),
#     ('TOP', '社会'),
#     ('TOP', '艺术'),
#     ('TOP', '经济'),
#     ('TOP', '科学'),
#     ('TOP', '体育'),
#     ('TOP', '技术')
# ]

#新冠种子
seeds = [
    ('TOP', '病毒'),
    ('TOP', '疾病'),
    ('TOP', '细菌'),
    ('TOP', '药物'),
    ('TOP', '症状'),
    ('TOP', '医疗'),
    ('TOP', '医学')
]

for seed in seeds:
    fenlei_subclass_bigram.add(seed)
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

threads = []
for i in range(3):
    t = threading.Thread(target=download_from_work_list, args=(work_list,))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()



# 对失败的类别，多进行十次尝试
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

with open(os.path.join('../data/hudongbaike', 'hudongbaike_fenlei_failed_list.txt'), 'w', encoding='utf-8') as f:
    for failed_item in failed_list:
        f.write(failed_item + '\n')

print(len(fenlei_subclass_bigram))

fenlei_subclass_bigram_list = list(fenlei_subclass_bigram)
fenlei_subclass_bigram_list.sort(key=itemgetter(0))


with open(os.path.join('../data/xinguan_hudongbaike', 'hudongbaike_fenlei_subclass_bigram.txt'), 'w', encoding='utf-8') as f:
    for father, child in fenlei_subclass_bigram_list:
        f.write(father + sep + child + '\n')

with open(os.path.join('../data/xinguan_hudongbaike', 'hudongbaike_fenlei_url.json'), 'w', encoding='utf-8') as f:
    json.dump(fenlei_url_dict, f, ensure_ascii=False, indent=4)

with open(os.path.join('../data/xinguan_hudongbaike', 'hudongbaike_fenlei.txt'), 'w', encoding='utf-8') as f:
    fenlei = set()
    for sup, sub in fenlei_subclass_bigram_list:
        fenlei.add(sup)
        fenlei.add(sub)
    fenlei_list = list(fenlei)
    fenlei_list.remove('TOP')
    for fe in fenlei_list:
        f.write(fe + '\n')



