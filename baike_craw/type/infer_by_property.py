import os
import json
from process.process_utils import get_triple

category_property_dict = {
    'virus': ['病毒形状', '传播途径'],
    'bacteria': ['界'], # [界] == 细菌界
    'medicine': ['是否处方药', '不良反应', '药品禁忌', '用法用量'],
    'disease': ['临床表现', '医学专科', '发病部位', '常见病因', '传染性', '病原类型']
}


def infer(fenlei):
    entity_set = set()
    with open(os.path.join('../data/xinguan_hudongbaike', 'hudongbaike_infobox_triples.txt'), 'r', encoding='utf-8') as tf:
        for line in tf:
            if line and line.strip():
                s, p, o = get_triple(line)
                for key in category_property_dict[fenlei]:
                    if key == p:
                        if fenlei != 'bacteria':
                            entity_set.add(s)
                        elif o.strip() == '细菌界':
                            entity_set.add(s)
    filename = 'hudongbaike_' + fenlei + '_entity.txt'
    fenlei_f = open(os.path.join('../data/xinguan_hudongbaike/entity/entity_by_property', filename), 'w', encoding='utf-8')
    for entity in entity_set:
        fenlei_f.write(entity + '\n')

if __name__ == '__main__':
    for category in category_property_dict.keys():
        infer(category)