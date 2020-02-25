import os
import json


# index
# 唯一标识符
index = 51


basic_set = set()
with open(os.path.join('../data/final/schema', 'schema_category.txt'), 'r', encoding='utf-8') as f:
    for line in f:
        if line and line.strip():
            basic_set.add(line.strip('\n'))


with open(os.path.join('../data/final', 'class_graph.json'), 'r', encoding='utf-8') as f:
    class_graph = json.load(f)

def get_id_by_name(list, na):
    for dict in list:
        label = dict["label"]
        name = label["@value"]
        if name == na:
            return dict["@id"]



# 获取所有property
graph_list = []

with open(os.path.join('../data/final/schema', 'relation_dict.json'), 'r', encoding='utf-8') as f:
    dict = json.load(f)

triple_dict = {}
for sub_dict in dict.items():
    subject = sub_dict[0]
    for obj_dict in sub_dict[1].items():
        object = obj_dict[0]
        value = obj_dict[1][0]
        object_list = triple_dict.get(subject + ":" + value, [])
        object_list.append(object)
        triple_dict[subject + ":" + value] = object_list

for triple in triple_dict.items():
    bigram = triple[0].split(':')
    relation_dict = {}
    relation_dict["@id"] = "http://www.openkg.cn/COVID-19/wiki/property/P" + str(index)
    index = index + 1
    relation_dict["@type"] = "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"
    label_dict = {}
    label_dict["@language"] = "zh"
    label_dict["@value"] = bigram[1]
    relation_dict["label"] = label_dict
    relation_dict["domain"] = get_id_by_name(class_graph["@graph"], bigram[0])
    if len(triple[1]) == 1:
        relation_dict["range"] = get_id_by_name(class_graph["@graph"], object)
    else:
        range_list = []
        for object in triple[1]:
            range_list.append(get_id_by_name(class_graph["@graph"], object))
        relation_dict["range"] = range_list
    graph_list.append(relation_dict)

# 特殊 relation sameAs
for basic_class in basic_set:
    relation_dict = {}
    relation_dict["@id"] = "http://www.openkg.cn/COVID-19/wiki/property/P" + str(index)
    index = index + 1
    relation_dict["@type"] = "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"
    label_dict["@language"] = "zh"
    label_dict["@value"] = "sameAs"
    relation_dict["label"] = label_dict
    relation_dict["domain"] = get_id_by_name(class_graph["@graph"], basic_class)
    id_list = []
    for basic_class in basic_set:
        id = get_id_by_name(class_graph["@graph"], basic_class)
        id_list.append(id)
    relation_dict["range"] = id_list
    graph_list.append(relation_dict)

# 构造graph dict
graph_dict = {}
graph_dict["@graph"] = graph_list

# 写入
with open(os.path.join('../data/final', 'relation_graph.json'), 'w', encoding='utf-8') as f:
    json.dump(graph_dict, f, ensure_ascii=False, indent=4)