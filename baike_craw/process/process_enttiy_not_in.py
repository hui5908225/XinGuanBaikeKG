import os
import json
wf =  open(os.path.join('../data/xinguan_baike/hudongbaike', 'symptom_entity_property_final.json'), 'w', encoding='utf-8')
with open(os.path.join('../data/xinguan_baike/hudongbaike', 'symptom_entity_property.json'), 'r', encoding='utf-8') as f:
    dict = json.load(f)
    f.close()
entity_set = set()
with open(os.path.join('../data/final/type', 'symptom.txt'), 'r', encoding='utf-8') as f:
    for line in f:
        if line and line.strip():
            entity_set.add(line.strip('\n'))

new_dict = {}
for d in dict.items():
    if d[0] in entity_set:
        new_dict[d[0]] = d[1]

json.dump(new_dict, wf, ensure_ascii=False, indent=4)