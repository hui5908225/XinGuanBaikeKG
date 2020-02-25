import os
import json
f = open(os.path.join("../data/final", 'context.json'), 'w', encoding='utf-8')
dict = {}
label_dict = {}
label_dict["@id"] = "http://www.w3.org/2000/01/rdf-schema#label"
dict["label"] = label_dict

range_dict = {}
range_dict["@id"] = "http://www.w3.org/2000/01/rdf-schema#range"
range_dict["@type"] = "@id"
dict["range"] = range_dict

domain_dict = {}
domain_dict["@id"] = "http://www.w3.org/2000/01/rdf-schema#domain"
domain_dict["@type"] = "@id"
dict["domain"] = domain_dict

subclassof_dict = {}
subclassof_dict["@id"] = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
subclassof_dict["@type"] = "@id"
dict["subClassOf"] = subclassof_dict

for i in range(0, 73):
    property_dict = {}
    property_dict["@id"] = "http://www.openkg.cn/COVID-19/wiki/property/P"+ str(i)
    property_dict["@type"] ="@id"
    dict["P" + str(i)] = property_dict

json.dump(dict, f, ensure_ascii=False, indent=4)
