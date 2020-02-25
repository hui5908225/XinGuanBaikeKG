import json
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import os
from craw.craw_utils import get_html


def items_in_class(_class):
    base_class_url = 'http://fenlei.baike.com/'
    url_suffix = '/list'

    item_urls = {}

    print(_class, end='\t')
    class_url = base_class_url + urllib.parse.quote(_class) + url_suffix
    print(class_url)

    html = get_html(class_url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        dl = soup.find('dl', {'class': 'link_blue'})
        if dl:
            all_links = dl.find_all('a', {'target': '_blank'})
            for a in all_links:
                if 'href' in a.attrs:
                    item_urls[a.get_text()] = a.attrs['href']

    print('available items %d' % len(item_urls), end='\t')
    return item_urls, len(item_urls)


def download_all_item_url():
    total_url_cnt = 0
    class2urls = {}
    with open(os.path.join('../data/xinguan_hudongbaike', 'hudongbaike_fenlei.txt'), 'r', encoding='utf-8') as f,\
            open(os.path.join('../data/xinguan_hudongbaike', 'hudongbaike_fenlei_entity_url.json'), 'w', encoding='utf-8') as dest_f:
        lines = [line.strip() for line in f]
        for i, line in enumerate(lines):
            urls, cnt = items_in_class(line)
            class2urls[line] = urls
            total_url_cnt += cnt
            print('class %d/%d' % (i + 1, len(lines)))
        print('total', total_url_cnt)
        json.dump(class2urls, dest_f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    download_all_item_url()

