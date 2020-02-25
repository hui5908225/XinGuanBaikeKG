import os
import json
wf = open(os.path.join('../data/final/', 'wiki-COVID-19-v0.2.json'), 'w', encoding='utf-8')
with open(os.path.join('../data/final/', 'class_graph.json'), 'r', encoding='utf-8') as f:
    class_graph = json.load(f)
with open(os.path.join('../data/final/', 'property_graph.json'), 'r', encoding='utf-8') as f:
    property_graph = json.load(f)
with open(os.path.join('../data/final/', 'relation_graph.json'), 'r', encoding='utf-8') as f:
    relation_graph = json.load(f)
with open(os.path.join('../data/final/', 'resource_graph.json'), 'r', encoding='utf-8') as f:
    resource_graph = json.load(f)
with open(os.path.join('../data/final/', 'context.json'), 'r', encoding='utf-8') as f:
    context = json.load(f)

dict = {}

class_list = class_graph["@graph"]
property_list = property_graph["@graph"]
relation_list = relation_graph["@graph"]
resource_list = resource_graph["@graph"]
graph_list = class_list + property_list + relation_list + resource_list

dict["@graph"] = graph_list
dict["@context"] = context

json.dump(dict, wf, ensure_ascii=False, indent=4)