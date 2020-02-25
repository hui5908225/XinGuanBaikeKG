from urllib.parse import unquote
import os
import os.path
from bs4 import BeautifulSoup
import json
from craw.craw_utils import sep
import re


def clean(s):
    s = re.sub(r'\s+', '', s)
    if s.endswith('：'):
        s = s[:-1]
    return s


def extract_inner_link():
    # triples_fp
    # triples_detail_fp
    # properties_fp

    page_cnt, extract_cnt, success_cnt = 0, 0, 0

    # i = 1,2 ...,12
    i = 11
    file_name = 'entity_pages_' + str(i) + '.xml'
    inner_link_dict = {}
    with open(os.path.join('../data/xinguan_hudongbaike/entity_page', file_name), 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
        all_page = soup.find_all('page')
        for page in all_page:
            inner_link_set = set()
            page_cnt += 1
            if page.title:
                title = page.title.string
                content = page.find('div', {'id':'content'})
                if content:
                    inner_link_list = content.find_all('a', {'class': 'innerlink'})
                    if len(inner_link_list) != 0:
                        for inner_link in inner_link_list:
                            inner_link_set.add(inner_link.get_text())
            inner_link_dict[title] = list(inner_link_set)
        print('page_cnt', page_cnt, 'has_infobox_cnt', extract_cnt, 'success_cnt', success_cnt)
    filename = 'hudongbaike_innerlink_' + str(i) +'.txt'
    wf = open(os.path.join('../data/xinguan_hudongbaike/inner_link', filename), 'w', encoding='utf-8')
    json.dump(inner_link_dict, wf, ensure_ascii=False, indent=4)
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
    extract_inner_link()
    # page_cnt 3070 has_infobox_cnt 1630 success_cnt 1629

    #extract_properties()
    # 721
