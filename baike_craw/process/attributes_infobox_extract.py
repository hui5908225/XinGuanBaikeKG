import os
import json
from process.process_utils import get_bigram, get_triple


pf = open(os.path.join('../data/xinguan_hudongbaike', 'schema_template2property.json'), 'r', encoding='utf-8')
all_fenlei_property_dict = json.load(pf)

def get_entity_from_category(category):
    entity_set = set()
    filename = 'hudongbaike_' + category + '_entity.txt'
    # filename = 'test.txt'
    with open(os.path.join('../data/xinguan_hudongbaike/entity/entity_type_fusion', filename), 'r', encoding='utf-8') as hf:
        for line in hf:
            if line and line.strip():
                entity_set.add(line.strip('\n'))
    return entity_set

# 实体的infobox抽取
def extract_json_infobox():
    entity_dict = {}
    with open(os.path.join('../data/xinguan_hudongbaike', 'hudongbaike_infobox_triples.txt'), 'r', encoding='utf-8') as hf:
        for line in hf:
            if line and line.strip():
                s, p, o = get_triple(line)
                property_value_dict = entity_dict.get(s, {})
                property_value_dict[p] = o.strip('\n')
                entity_dict[s] = property_value_dict
        hf.close()
    return entity_dict

# 实体属性抽取
def attriute_extract_from_infobox(dict, entity_set):
    for entity in entity_set:
        entity_dict = {}
        property_dict = all_fenlei_property_dict[category]
        for property in property_dict.values():
            entity_dict[property] = ''
        property_value_dict = dict.get(entity, {})
        for key, value in property_value_dict.items():
            new_value = property_dict.get(key, 'unknown')
            if new_value != 'unknown':
                entity_dict[new_value] = value
        entity_property_value_dict[entity] = entity_dict


if __name__ == '__main__':
    category_list = ['bacteria', 'disease', 'medicine', 'virus']
    for category in category_list:
        # 实体 属性与属性值
        entity_property_value_dict = {}
        # 存所有分类
        entity_set = get_entity_from_category(category)
        dict = extract_json_infobox()
        attriute_extract_from_infobox(dict, entity_set)
        filename = category + '_entity_property.json'
        with open(os.path.join('../data/xinguan_hudongbaike/entity_property', filename), 'w', encoding='utf-8') as epf:
            json.dump(entity_property_value_dict, epf, ensure_ascii=False, indent=4)
