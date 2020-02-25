import json
import os
from craw.craw_utils import get_html_with_header
from bs4 import BeautifulSoup
import time

title_inner_link_dict = {}

def get_page_and_inner_link(title, url):
    s = '\n\n<page>\n'
    s += '<title>' + title + '</title>\n'
    html = get_html_with_header(url)
    if html:
        # soup = BeautifulSoup(html, 'html.parser')
        # inner_link = soup.find_all('a', {'class': 'innerlink'})
        # title_href_list = []
        # if inner_link:
        #     for link in inner_link:
        #         link_title = link.get_text()
        #         href = link.get('href')
        #         title_href_list.append([link_title,href])
        #     title_inner_link_dict[title] = title_href_list
        s += html + '\n'
        s += '</page>\n'
        return s
    else:
        return ""



def download_pages():
    #entity
    dest_f = open(os.path.join('../data/xinguan_hudongbaike', 'entity_pages.xml'), 'w', encoding='utf-8')
    urls = set()
    with open(os.path.join('../data/xinguan_hudongbaike', 'hudongbaike_fenlei_entity_url.json'), 'r', encoding='utf-8') as f:
        class2urls = json.load(f)
    # 去重
    for v in class2urls.values():
        for title, url in v.items():
            urls.add((title, url))
    success_cnt = 0
    for i, (title, url) in enumerate(urls):
        page = get_page_and_inner_link(title, url)
        if page:
            dest_f.write(page)
            success_cnt += 1
        if i % 10 == 0:
            print('pages success/process:%d/%d, total:%d' % (success_cnt, i, len(urls)))
    dest_f.close()

    #class
    dest_f = open(os.path.join('../data/xinguan_hudongbaike', 'class_pages.xml'), 'w', encoding='utf-8')
    urls = set()
    with open(os.path.join('../data/xinguan_hudongbaike', 'hudongbaike_fenlei_url.json'), 'r', encoding='utf-8') as f:
        class2urls = json.load(f)
    # 去重
    for title,url in class2urls.items():
        urls.add((title, url))
    success_cnt = 0
    for i, (title, url) in enumerate(urls):
        page = get_page_and_inner_link(title, url)
        if page:
            dest_f.write(page)
            success_cnt += 1
        if i % 10 == 0:
            print('pages success/process:%d/%d, total:%d' % (success_cnt, i, len(urls)))
    dest_f.close()

    #inner_link
    # with open(os.path.join('../data/xinguan_hudongbaike', 'inner_link.json'), 'a', encoding='utf-8') as inner_f:
    #     json.dump(title_inner_link_dict, inner_f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    download_pages()

