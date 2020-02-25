import os
import json
from process.process_utils import get_triple

category_key_dict = {
    'virus': ['病毒'],
    'bacteria': ['菌'],
    'medicine': ['胶囊', '丸', '液', '片', '膏', '素', '丹', '散', '剂',
                 '贴', '粒', '疫苗'],
    'disease': ['病', '炎', '症']
}


def infer(fenlei):
    entity_set = set()
    with open(os.path.join('../data/xinguan_hudongbaike', 'hudongbaike_fenlei_entity_url.json'), 'r', encoding='utf-8') as tf:
        category_entity_dict = json.load(tf)

    for entity_url_dict in category_entity_dict.values():
        for entity in entity_url_dict.keys():
            if len(entity) > 2:
                key_list = category_key_dict[fenlei]
                for key in key_list:
                    if (entity[-2:] == key) or (entity[-1:] == key):
                        entity_set.add(entity)
    filename = 'hudongbaike_' + fenlei + '_entity.txt'
    fenlei_f = open(os.path.join('../data/xinguan_hudongbaike/entity/entity_by_name', filename), 'w', encoding='utf-8')
    for entity in entity_set:
        fenlei_f.write(entity + '\n')

if __name__ == '__main__':
    for category in category_key_dict.keys():
        infer(category)