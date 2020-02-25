import json
with open('virus_json.json', 'r', encoding='utf-8') as f:
    dict = json.load(f)
    f.close()

new_dict = {}
list = dict["RECORDS"]
for d in list:
    name = d['名称']
    new_dict[name] = d


with open('virus_entity_property.json', 'w', encoding='utf-8') as f:
    json.dump(new_dict, f, ensure_ascii=False, indent=4)
    f.close()