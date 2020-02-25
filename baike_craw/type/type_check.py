import os

category_list = ['virus', 'bacteria', 'disease', 'medicine']

all_entity_dict = {}

for category in category_list:
    filename = 'znwiki_' + category + '_entity.txt'
    entity_set = set()
    with open(os.path.join('../data/xinguan_znwiki/entity/entity_type_fusion', filename), 'r', encoding='utf-8') as f:
        for line in f:
            if line and line.strip():
                entity = line.strip('\n')
                entity_set.add(entity)
        f.close()
    all_entity_dict[category] = entity_set


wf = open(os.path.join('../data/xinguan_znwiki/entity/entity_type_fusion', 'znwiki_confict_entity.txt'), 'w', encoding='utf-8')

processed_category = []
for ca in category_list:
    processed_category.append(ca)
    for ca2 in category_list:
        if ca2 not in processed_category:
            intersection_set = all_entity_dict[ca].intersection(all_entity_dict[ca2])
            for entity in intersection_set:
                wf.write(ca + ";;;;ll;;;;" + ca2 + ";;;;ll;;;;" + entity + '\n')