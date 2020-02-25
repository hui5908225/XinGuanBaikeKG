import os
from craw.craw_utils import sep
category_list = ['bacteria', 'disease', 'drug', 'inspect', 'specialty', 'symptom', 'virus']

property_dict = {}
category_dict = {}
triple_dict = {}
for category in category_list:
    file_name = category + '.txt'
    ca_file = open(os.path.join('../data/xinguan_baike/type', file_name), 'r', encoding='utf-8')
    for line in ca_file:
        if line and line.strip():
            category_dict[line.strip('\n')] = category
cwf = open(os.path.join('../data/xinguan_baike', 'category_relation_statistic.txt'), 'w', encoding='utf-8')

with open(os.path.join('../data/xinguan_baike', 'triples_mining.txt'), 'r', encoding='utf-8') as f:
    for line in f:
        if line and line.strip():
            triple = line.split('-')
            if len(triple) == 3:
                s = triple[0]
                p = triple[1]
                o = triple[2].strip('\n')
                c_s = category_dict.get(s, '')
                c_o = category_dict.get(o, '')
                if c_s.strip() and c_o.strip():
                    new_triple = c_s + sep + p + sep + c_o
                    num = triple_dict.get(new_triple, 0)
                    triple_dict[new_triple] = num + 1

sort_property = sorted(triple_dict.items(), key=lambda item: item[1], reverse=True)
sort_property.sort()
for property in sort_property:
    cwf.write(property[0] + ' num: ' + str(property[1]) + '\n')
