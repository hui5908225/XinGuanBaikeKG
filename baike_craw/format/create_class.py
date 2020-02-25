import os
import json

def get_id_by_name(list, na):
    for dict in list:
        label = dict["label"]
        name = label["@value"]
        if name == na:
            return dict["@id"]

# 获取所有class 并获得bigram
basic_set = set()
with open(os.path.join('../data/final/schema', 'schema_category.txt'), 'r', encoding='utf-8') as f:
    for line in f:
        if line and line.strip():
            basic_set.add(line.strip('\n'))

class_set = set()
subclass_dict = {}
with open(os.path.join('../data/final/schema', 'schema_subclass.txt'), 'r', encoding='utf-8') as f:
    for line in f:
        if line and line.strip():
            triple = line.split('\t')
            sub = triple[0].strip('<>')
            sup = triple[2].strip('\n').strip('<>')
            class_set.add(sub)
            if sup not in basic_set:
                class_set.add(sup)
            subclass_dict[sub] = sup
# 写入
# 先写入基础class
# index 唯一标识符
index = 0
graph_list = []
for basic_class in basic_set:
    class_dict = {}
    class_dict["@id"] = "http://www.openkg.cn/COVID-19/wiki/class/C" + str(index)
    index = index + 1
    class_dict["@type"] = "http://www.w3.org/2000/01/rdf-schema#Class"
    label_dict = {}
    label_dict["@language"] = "zh"
    label_dict["@value"] = basic_class
    class_dict["label"] = label_dict
    graph_list.append(class_dict)

# 写入低阶class
for cla in class_set:
    class_dict = {}
    class_dict["@id"] = "http://www.openkg.cn/COVID-19/wiki/class/C" + str(index)
    index = index + 1
    class_dict["@type"] = "http://www.w3.org/2000/01/rdf-schema#Class"
    label_dict = {}
    label_dict["@language"] = "zh"
    label_dict["@value"] = cla
    class_dict["label"] = label_dict
    graph_list.append(class_dict)

# 补入subclass
for c in class_set:
    sup = subclass_dict.get(c, '')
    if sup and sup.strip():
        sup_id = get_id_by_name(graph_list, sup)
    sub_id = get_id_by_name(graph_list, c)
    for dict in graph_list:
        if dict["@id"] == sub_id:
            dict["subClassOf"] = sub_id

# 构造graph dict
graph_dict = {}
graph_dict["@graph"] = graph_list

# 写入
with open(os.path.join('../data/final', 'class_graph.json'), 'w', encoding='utf-8') as f:
    json.dump(graph_dict, f, ensure_ascii=False, indent=4)