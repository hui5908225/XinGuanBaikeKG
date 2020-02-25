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


def extract_summary():
    entity_set = set()

    # i = 1,2 ...,12
    i = 12
    file_name = 'entity_pages_' + str(i) + '.xml'
    with open(os.path.join('../data/xinguan_hudongbaike/entity_page', file_name), 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
        all_page = soup.find_all('page')
        for page in all_page:
            if page.title:
                title = page.title.string
                summary = page.find('div', {'class': 'summary'})
                label_div = page.find('div', {'class': 'place'})
                if summary and label_div:
                    label_tags = label_div.find_all('a')
                    for label_tag in label_tags:
                        label = label_tag.get_text()
                        if label == '药品' or label == '疫苗' or label == '中药':
                            regex = re.compile('((\u6cbb\u7597|\u6291\u5236|\u7981\u7528|\u6740\u706d)+)')
                            result = regex.findall(summary.get_text())
                            if len(result) != 0:
                                entity_set.add(title + '\n')
        f.close()
    wf = open(os.path.join('../data/xinguan_hudongbaike/entity/entity_by_summary_label', 'hudongbaike_medicine_entity.txt'), 'a', encoding='utf-8')
    for entity in entity_set:
        wf.write(entity)
if __name__ == '__main__':
    extract_summary()
