import os
import json


full_property_value = []
for i in range(1,13):
    filename = 'property_' + str(i) + '.json'
    with open(os.path.join('../data/xinguan_hudongbaike/property_extract_from_text', filename), 'r', encoding='utf-8') as f:
        property_value_dict = json.load(f)
        full_property_value.append(property_value_dict)

category_list = ['virus', 'bacteria', 'disease', 'medicine']
for category in category_list:
    ca_filename = category + '_entity_property.json'
    with open(os.path.join('../data/xinguan_hudongbaike/entity_property', ca_filename), 'r', encoding='utf-8') as f:
        ca_property_value_dict = json.load(f)
        f.close()

    # 补全
    for key, dict_value in ca_property_value_dict.items():
        text_dict = {}
        for full_dict in full_property_value:
            for full_name, full_value in full_dict.items():
                if key == full_name:
                    text_dict[key] = full_value
        for inner_key, inner_value in dict_value.items():
            d = text_dict.get(key, {})
            if d != {}:
                if inner_value == '':
                    rich_value = d.get(inner_key, '')
                    if rich_value != '':
                        dict_value[inner_key] = rich_value
                        print('补全:'+ key + ":" + inner_key + ":" + rich_value)

    ca_filename = category + '_entity_property_rich.json'
    with open(os.path.join('../data/xinguan_hudongbaike/entity_property', ca_filename), 'w', encoding='utf-8') as f:
        json.dump(ca_property_value_dict, f, ensure_ascii=False, indent=4)
        f.close()