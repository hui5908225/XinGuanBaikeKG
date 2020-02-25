from urllib.parse import unquote
import os
import os.path
from bs4 import BeautifulSoup
from craw.craw_utils import sep
import re
import json

def clean(s):
    s = re.sub(r'\s+', '', s)
    if s.endswith('：'):
        s = s[:-1]
    return s


def extract_infobox():
    # triples_fp
    # triples_detail_fp
    # properties_fp

    page_cnt = 0

    # i = 1,2 ...,12
    i = 12
    r_file_name = 'entity_pages_' + str(i) + '.xml'
    w_file_name = 'entity_names_' + str(i) + '.json'
    dest_f = open(os.path.join('../data/xinguan_hudongbaike/entity_names', w_file_name), 'w', encoding='utf-8')
    with open(os.path.join('../data/xinguan_hudongbaike/entity_page', r_file_name), 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
        all_page = soup.find_all('page')
        dict = {}
        for page in all_page:
            name_set = set()
            page_cnt += 1
            if page.title:
                title = page.title.string
                name_set.add(title)
                # 同义词
                polysemy = page.find('div', {'class': 'polysemy'})
                if polysemy:
                    a = polysemy.find_all('a')
                    for name in a:
                        n =name.get_text()
                        if n != '纠错' and n != '编辑多义词':
                            name_set.add(n)
                # 别称
                infobox = page.find('div', {'name': 'datamodule'})
                if infobox:
                    tds = list(infobox.find_all('td'))
                    if tds:
                        for td in tds:
                            strong = td.find('strong')
                            span = td.find('span')
                            if strong and span:
                                pre = clean(strong.get_text())
                                obj = clean(span.get_text())
                                if pre == '别称' or pre == '别名':
                                    obj_list = obj.split('、')
                                    for o in obj_list:
                                        name_set.add(o)
                                if pre in ['中文名', '中文学名', '中医学名', '名称']:
                                    name_set.add(obj)
                dict[title] = list(name_set)
        json.dump(dict, dest_f, ensure_ascii=False, indent=4)
        print('page_cnt', page_cnt)


#def extract_properties():
    # with open(os.path.join('data', 'infobox_triples.txt'), 'r', encoding='utf-8') as f, \
    #         open(os.path.join('data', 'properties.txt'), 'w', encoding='utf-8') as dest_f:
    #     ps = set()
    #     for line in f:
    #         triple = line.strip().split(sep)
    #         ps.add(triple[1])
    #     print('properties', len(ps))
    #     for p in ps:
    #         dest_f.write(p + '\n')


if __name__ == '__main__':
    extract_infobox()
    # page_cnt 3070 has_infobox_cnt 1630 success_cnt 1629

    #extract_properties()
    # 721
