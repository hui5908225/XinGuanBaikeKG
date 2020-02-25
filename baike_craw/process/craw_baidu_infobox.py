import json
import os
import os.path
from bs4 import BeautifulSoup
from craw.craw_utils import sep,get_html_with_header
import re
import time

def clean(s):
    s = re.sub(r'\s+', '', s)
    if s.endswith('：'):
        s = s[:-1]
    return s

entity_url_dict = {}
failed_entity_url_dict = {}
def get_entity_url_dict():
    with open(os.path.join('../data/xinguan_baidubaike','bdsymptoms.json'), 'r', encoding='utf-8') as f:
        class2urls = json.load(f)
        for class_entities in class2urls.values():
            for item in class_entities.items():
                entity_url_dict[item[0]] = item[1]
    print(len(entity_url_dict))

def extract_infobox(dict):
    base_url = 'https://baike.baidu.com'
    with open(os.path.join('../data/xinguan_baidubaike', 'baidubaike_infobox_triples_1.txt'), 'a', encoding='utf-8') as f:
        sum = len(dict)
        current = 1
        for item in dict.items():
            print("process: " + str(current) + "/" + str(sum) + '\n')
            name = item[0]
            url = item[1]
            time.sleep(1)
            html = get_html_with_header(url)
            time.sleep(1)
            if not html:
                print('FAILED:', name)
                failed_entity_url_dict[name] = url
            soup = BeautifulSoup(html, 'html.parser')
            infobox_soup = soup.find('div', {'class', 'basic-info cmn-clearfix'})
            if infobox_soup is not None:
                dt_tags = infobox_soup.find_all('dt', {'class', 'basicInfo-item name'})
                dd_tags = infobox_soup.find_all('dd', {'class', 'basicInfo-item value'})
                if len(dt_tags) == len(dd_tags):
                    for i in range(len(dt_tags)):
                        predicate = clean(dt_tags[i].get_text())
                        object = clean(dd_tags[i].get_text())
                        f.write(name + sep + predicate + sep + object + '\n')
            current += 1

if __name__ == '__main__':
    #5240
    get_entity_url_dict()
    extract_infobox(entity_url_dict)
    #失败再处理一次
    if len(failed_entity_url_dict) > 0:
        extract_infobox(failed_entity_url_dict)