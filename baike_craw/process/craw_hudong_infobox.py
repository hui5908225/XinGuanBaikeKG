from urllib.parse import unquote
import os
import os.path
from bs4 import BeautifulSoup
from craw.craw_utils import sep
import re


def clean(s):
    s = re.sub(r'\s+', '', s)
    if s.endswith('：'):
        s = s[:-1]
    return s


def extract_infobox():
    # triples_fp
    # triples_detail_fp
    # properties_fp

    base_url = 'http://www.baike.com/wiki/'
    base_len = len(base_url)
    page_cnt, extract_cnt, success_cnt = 0, 0, 0

    # i = 1,2 ...,12
    i = 12
    file_name = 'entity_pages_' + str(i) + '.xml'
    with open(os.path.join('../data/xinguan_hudongbaike/entity_page', file_name), 'r', encoding='utf-8') as f:
        with open(os.path.join('../data/xinguan_hudongbaike', 'hudongbaike_infobox_triples.txt'), 'a', encoding='utf-8') as dest_f:
            soup = BeautifulSoup(f.read(), 'lxml')
            all_page = soup.find_all('page')
            for page in all_page:
                page_cnt += 1
                if page.title:
                    title = page.title.string
                    infobox = page.find('div', {'name': 'datamodule'})
                    if infobox:
                        extract_cnt += 1
                        tds = list(infobox.find_all('td'))
                        if tds:
                            success_cnt += 1
                            for td in tds:
                                strong = td.find('strong')
                                span = td.find('span')
                                if strong and span:
                                    pre = clean(strong.get_text())
                                    obj = clean(span.get_text())
                                    # a = span.find_all('a')
                                    # if len(a) == 1:
                                    #     a = a[0]
                                    #     if a and'href' in a.attrs and a.attrs['href'].startswith(base_url):
                                    #         obj = '<' + clean(unquote(a.attrs['href'][base_len:])) + '>'
                                    # else:
                                    #     obj = '"' + clean(span.get_text()) + '"'
                                    dest_f.write(title + sep + pre + sep + obj + '\n')
            print('page_cnt', page_cnt, 'has_infobox_cnt', extract_cnt, 'success_cnt', success_cnt)


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
