import os
import json

index = 0

corr = {}
corr['disease'] = "疾病"
corr['drug'] = "药物"
corr['symptom'] = "症状"
corr['virus'] = '病毒'
corr['bacteria'] = "细菌"
corr['inspect'] = '检查科目'
corr['speciality'] = '医学专科'
corr['Baidu'] = '百度百科'
corr['Hudong'] = '互动百科'
corr['Znwiki'] = '中文维基百科'
corr['Yixue'] = '医学百科'

with open(os.path.join('../data/final', 'property_graph.json'), 'r', encoding='utf-8') as f:
    property_graph = json.load(f)

with open(os.path.join('../data/final', 'relation_graph.json'), 'r', encoding='utf-8') as f:
    relation_graph = json.load(f)

with open(os.path.join('../data/final', 'class_graph.json'), 'r', encoding='utf-8') as f:
    class_graph = json.load(f)

def get_tail_id(str):
    b = "P"
    return str[str.rfind(b):]

def get_id_by_name(list, na):
    for dict in list:
        label = dict["label"]
        name = label["@value"]
        if name == na:
            return dict["@id"]

def get_id_by_name_domain(list, na, do_id):
    for dict in list:
        label = dict["label"]
        name = label["@value"]
        if name == na:
            domain = dict["domain"]
            if domain == do_id:
                return dict["@id"]

def get_id_by_name_source(list, na, s):
    for dict in list:
        label = dict["label"]
        name = label["@value"]
        if name == na:
            source1 = dict.get("P44", "")
            source2 = dict.get("P45", "")
            source3 = dict.get("P46", "")
            source4 = dict.get("P47", "")
            source5 = dict.get("P48", "")
            source6 = dict.get("P49", "")
            source7 = dict.get("P50", "")
            if source1 == s or source2 == s or source3 == s or source4 == s or source5 == s or source6 == s or source7 == s:
                return [dict["@id"], dict["@type"]]
    return []

graph_list = []
# 先导入所有实体
# Baidubaike
category_list = [('bacteria','细菌'), ('disease','疾病'), ('drug','药物'), ('inspect','检查科目'), ('specialty','医学专科'), ('symptom','症状'), ('virus','病毒')]
for category in category_list:
    filename = category[0] + '_entity_property_final.json'
    with open(os.path.join('../data/final/property/baidubaike', filename), 'r', encoding='utf-8') as f:
        dict = json.load(f)
        for entity in dict.items():
            entity_dict = {}
            subject = entity[0]
            entity_dict["@id"] = "http://www.openkg.cn/COVID-19/wiki/resource/R" + str(index)
            index = index + 1
            entity_dict["@type"] = get_id_by_name(class_graph["@graph"], category[1])
            label_dict = {}
            label_dict["@language"] = "zh"
            label_dict["@value"] = subject
            entity_dict["label"] = label_dict
            source_id = get_id_by_name_domain(
                property_graph["@graph"], "来源", get_id_by_name(class_graph["@graph"], category[1]))
            entity_dict[get_tail_id(source_id)] = "百度百科"
            for property_value in entity[1].items():
                property = property_value[0]
                value = property_value[1]
                if value != "" and value != "NULL":
                    id = get_id_by_name(property_graph["@graph"], property)
                    entity_dict[get_tail_id(id)] = value
            graph_list.append(entity_dict)

# Hudongbaike
category_list = [('bacteria','细菌'), ('disease','疾病'), ('drug','药物'), ('inspect','检查科目'), ('specialty','医学专科'), ('symptom','症状'), ('virus','病毒')]
for category in category_list:
    filename = category[0] + '_entity_property_final.json'
    with open(os.path.join('../data/final/property/hudongbaike', filename), 'r', encoding='utf-8') as f:
        dict = json.load(f)
        for entity in dict.items():
            entity_dict = {}
            subject = entity[0]
            entity_dict["@id"] = "http://www.openkg.cn/COVID-19/wiki/resource/R" + str(index)
            index = index + 1
            entity_dict["@type"] = get_id_by_name(class_graph["@graph"], category[1])
            label_dict = {}
            label_dict["@language"] = "zh"
            label_dict["@value"] = subject
            entity_dict["label"] = label_dict
            source_id = get_id_by_name_domain(
                property_graph["@graph"], "来源", get_id_by_name(class_graph["@graph"], category[1]))
            entity_dict[get_tail_id(source_id)] = "互动百科"
            for property_value in entity[1].items():
                property = property_value[0]
                value = property_value[1]
                if value != "" and value != "NULL":
                    id = get_id_by_name(property_graph["@graph"], property)
                    entity_dict[get_tail_id(id)] = value
            graph_list.append(entity_dict)


# Yixuebaike
category_list = [('bacteria','细菌'), ('disease','疾病'),('virus','病毒')]
for category in category_list:
    filename = category[0] + '_entity_property_final.json'
    with open(os.path.join('../data/final/property/hudongbaike', filename), 'r', encoding='utf-8') as f:
        dict = json.load(f)
        for entity in dict.items():
            entity_dict = {}
            subject = entity[0]
            entity_dict["@id"] = "http://www.openkg.cn/COVID-19/wiki/resource/R" + str(index)
            index = index + 1
            entity_dict["@type"] = get_id_by_name(class_graph["@graph"], category[1])
            label_dict = {}
            label_dict["@language"] = "zh"
            label_dict["@value"] = subject
            entity_dict["label"] = label_dict
            source_id = get_id_by_name_domain(property_graph["@graph"], "来源", get_id_by_name(class_graph["@graph"], category[1]))
            entity_dict[get_tail_id(source_id)] = "医学百科"
            for property_value in entity[1].items():
                property = property_value[0]
                value = property_value[1]
                if value != "" and value != "NULL":
                    id = get_id_by_name(property_graph["@graph"], property)
                    entity_dict[get_tail_id(id)] = value
            graph_list.append(entity_dict)

# Znwiki
category_list = [('bacteria','细菌'), ('disease','疾病'),('virus','病毒'), ('drug', '药物')]
for category in category_list:
    filename = category[0] + '_entity_property_final.json'
    with open(os.path.join('../data/final/property/hudongbaike', filename), 'r', encoding='utf-8') as f:
        dict = json.load(f)
        for entity in dict.items():
            entity_dict = {}
            subject = entity[0]
            entity_dict["@id"] = "http://www.openkg.cn/COVID-19/wiki/resource/R" + str(index)
            index = index + 1
            entity_dict["@type"] = get_id_by_name(class_graph["@graph"], category[1])
            label_dict = {}
            label_dict["@language"] = "zh"
            label_dict["@value"] = subject
            entity_dict["label"] = label_dict
            source_id = get_id_by_name_domain(
                property_graph["@graph"], "来源", get_id_by_name(class_graph["@graph"], category[1]))
            entity_dict[get_tail_id(source_id)] = "中文维基百科"
            for property_value in entity[1].items():
                property = property_value[0]
                value = property_value[1]
                if value != "" and value != "NULL":
                    id = get_id_by_name(property_graph["@graph"], property)
                    entity_dict[get_tail_id(id)] = value
            graph_list.append(entity_dict)

# 为所有实体创建链接
with open(os.path.join('../data/final', 'relation_triples_final.txt'), 'r', encoding='utf-8') as f:
    for line in f:
        if line and line.strip():
            pair = line.split(":")
            domain = corr[pair[0].split(";;;;ll;;;;")[0]]
            value = pair[1].split(";;;;ll;;;;")[1]
            domain_id = get_id_by_name(class_graph["@graph"], domain)
            value_id = get_id_by_name_domain(relation_graph["@graph"], value, domain_id)
            if value_id is None:
                continue
            subject = pair[1].split(";;;;ll;;;;")[0]
            object = pair[1].split(";;;;ll;;;;")[2].strip("\n")
            sub_id = get_id_by_name(graph_list, subject)
            obj_id = get_id_by_name(graph_list, subject)
            for entity in graph_list:
                if entity["@id"] == sub_id:
                    entity[get_tail_id(value_id)] = obj_id
                    #print(entity)

# sameAs 关系
with open(os.path.join('../data/final/property', 'sameas_relation.txt'), 'r', encoding='utf-8') as f:
    for line in f:
        if line and line.strip():
            triple = line.split(";;;;ll;;;;")
            s1 = corr[triple[1]]
            s2 = corr[triple[2].strip('\n')]
            list1 = get_id_by_name_source(graph_list, triple[0], s1)
            list2 = get_id_by_name_source(graph_list, triple[0], s2)
            if len(list1) !=0 and len(list2) != 0:
                e1 = list1[0]
                e2 = list2[0]
                t1 = list1[1]
                t2 = list2[1]
                sameAs_id_1 = get_id_by_name_domain(relation_graph["@graph"], "sameAs", t1)
                sameAs_id_2 = get_id_by_name_domain(relation_graph["@graph"], "sameAs", t2)
                for entity in graph_list:
                    if entity["@id"] == e1:
                        entity[get_tail_id(sameAs_id_1)] = e2
                    if entity["@id"] == e2:
                        entity[get_tail_id(sameAs_id_2)] = e1


graph_dict = {}
graph_dict["@graph"] = graph_list

# 写入
with open(os.path.join('../data/final', 'resource_graph.json'), 'w', encoding='utf-8') as f:
    json.dump(graph_dict, f, ensure_ascii=False, indent=4)