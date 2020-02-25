import os
import json
from craw.craw_utils import sep
wf = open(os.path.join('../data/xinguan_baike', 'sameas_relation.txt'), 'a', encoding='utf-8')

with open(os.path.join('../data/xinguan_baike/baidubaike', 'specialty_entity_property_final.json'), 'r', encoding='utf-8') as f:
    dict_1 = json.load(f)
    f.close()

with open(os.path.join('../data/xinguan_baike/hudongbaike', 'specialty_entity_property_final.json'), 'r', encoding='utf-8') as f:
    dict_2 = json.load(f)
    f.close()

for name_1 in dict_1.keys():
    for name_2 in dict_2.keys():
        if name_1 == name_2:
            wf.write(name_1 + sep + 'Baidu' + sep + 'Hudong' + '\n')

# baidubaike
# yixuebaike
# hudongbaike
# znwiki

# Baidu Hudong Znwiki Yixue