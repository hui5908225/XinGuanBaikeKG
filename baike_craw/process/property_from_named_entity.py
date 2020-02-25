import os
from process.process_utils import get_triple

fenlei_list = ['virus', 'bacteria', 'disease', 'medicine']

def get_entity_list(fenlei):
    entity_set = set()
    filename = 'hudongbaike_' + fenlei + '_entity.txt'
    with open(os.path.join('../data/xinguan_hudongbaike/entity/entity_by_name', filename), 'r', encoding='utf-8') as f:
        for line in f:
            entity = line.strip()
            entity_set.add(entity)
        f.close()
    return entity_set

def get_property_from_triples(entity_set, fenlei):
    property_dict = {}
    for entity in entity_set:
        with open(os.path.join('../data/xinguan_hudongbaike', 'hudongbaike_infobox_triples.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                if line and line.strip():
                    s, p, o = get_triple(line)
                    if s == entity:
                        if property_dict.get(p, -1) == -1:
                            property_dict[p] = 1
                        else:
                            property_dict[p] += 1
        f.close()
    sort_property = sorted(property_dict.items(), key=lambda item: item[1], reverse=True)
    print(fenlei)
    print(sort_property)

if __name__ == '__main__':
    for fenlei in fenlei_list:
        entity_set = get_entity_list(fenlei)
        get_property_from_triples(entity_set, fenlei)