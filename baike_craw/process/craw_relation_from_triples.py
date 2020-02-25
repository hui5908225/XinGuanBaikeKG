import json
import os
from craw.craw_utils import sep
category_list = ['bacteria', 'disease', 'drug', 'specialty', 'symptom', 'virus']

category_dict = {}
for category in category_list:
    file_name = category + '.txt'
    ca_file = open(os.path.join('../data/xinguan_baike/type', file_name), 'r', encoding='utf-8')
    for line in ca_file:
        if line and line.strip():
            category_dict[line.strip('\n')] = category
cwf = open(os.path.join('../data/xinguan_baike', 'category_relation.txt'), 'w', encoding='utf-8')

with open(os.path.join('../data/xinguan_baike', 'relation_dict.json'), 'r', encoding='utf-8') as f:
    relation_dict = json.load(f)

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
                    o_dict = relation_dict.get(c_s, None)
                    if o_dict is not None:
                        pre_list = o_dict.get(c_o, [])
                        if len(pre_list) != 0:
                            pre = pre_list[0]
                            for pr in pre_list[1]:
                                if p == pr:
                                    cwf.write(c_s + sep + c_o + ":" + s + sep + pre + sep + o + '\n')
                                    break
