import os
import json

with open(os.path.join('../data/final', 'class_graph.json'), 'r', encoding='utf-8') as f:
    class_graph = json.load(f)

basic_set = set()
with open(os.path.join('../data/final/schema', 'schema_category.txt'), 'r', encoding='utf-8') as f:
    for line in f:
        if line and line.strip():
            basic_set.add(line.strip('\n'))


def get_id_by_name(list, na):
    for dict in list:
        label = dict["label"]
        name = label["@value"]
        if name == na:
            return dict["@id"]

# index
# 唯一标识符
index = 0

# 获取所有property
graph_list = []
with open(os.path.join('../data/final/schema', 'schema_property.txt'), 'r', encoding='utf-8') as f:
    for line in f:
        if line and line.strip():
            list = line.split(';;;;ll;;;;')
            property_list = list[1].strip('\n').split(',')
            for property in property_list:
                property_dict = {}
                property_dict["@id"] = "http://www.openkg.cn/COVID-19/wiki/property/P" + str(index)
                index = index + 1
                property_dict["@type"] = "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"
                label_dict = {}
                label_dict["@language"] = "zh"
                label_dict["@value"] = property
                property_dict["label"] = label_dict
                property_dict["domain"] = get_id_by_name(class_graph["@graph"], list[0])
                property_dict["range"] = "http://www.w3.org/2001/XMLSchema#string"
                graph_list.append(property_dict)

# 特殊属性 source
for basic_class in basic_set:
    property_dict = {}
    property_dict["@id"] = "http://www.openkg.cn/COVID-19/wiki/property/P" + str(index)
    index = index + 1
    property_dict["@type"] = "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"
    label_dict = {}
    label_dict["@language"] = "zh"
    label_dict["@value"] = "来源"
    property_dict["label"] = label_dict
    property_dict["domain"] = get_id_by_name(class_graph["@graph"], basic_class)
    property_dict["range"] = "http://www.w3.org/2001/XMLSchema#string"
    graph_list.append(property_dict)
print(index)

# 构造graph dict
graph_dict = {}
graph_dict["@graph"] = graph_list

# 写入
with open(os.path.join('../data/final', 'property_graph.json'), 'w', encoding='utf-8') as f:
    json.dump(graph_dict, f, ensure_ascii=False, indent=4)