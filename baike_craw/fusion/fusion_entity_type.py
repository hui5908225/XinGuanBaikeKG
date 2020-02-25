import os

category_list = ['virus', 'bacteria', 'disease', 'medicine']
for category in category_list:
    filename = 'znwiki_' + category + '_entity.txt'

    entity_name_set = set()
    entity_property_set = set()
    entity_summary_label_set = set()
    with open(os.path.join('../data/xinguan_znwiki/entity/entity_by_name', filename), 'r', encoding='utf-8') as f:
        for line in f:
            if line and line.strip():
                entity = line.strip('\n')
                entity_name_set.add(entity)
        f.close()

    with open(os.path.join('../data/xinguan_znwiki/entity/entity_by_property', filename), 'r', encoding='utf-8') as f:
        for line in f:
            if line and line.strip():
                entity = line.strip('\n')
                entity_property_set.add(entity)
        f.close()

    with open(os.path.join('../data/xinguan_znwiki/entity/entity_by_summary_label', filename), 'r', encoding='utf-8') as f:
        for line in f:
            if line and line.strip():
                entity = line.strip('\n')
                entity_summary_label_set.add(entity)
        f.close()

    # 以name为基准，对property和summary_label进行校验
    with open(os.path.join('../data/xinguan_znwiki/entity/entity_by_summary_label', filename), 'r', encoding='utf-8') as f:
        for line in f:
            if line and line.strip():
                entity = line.strip('\n')
                entity_summary_label_set.add(entity)

    fusion_set = entity_name_set.union(entity_property_set).union(entity_summary_label_set)
    with open(os.path.join('../data/xinguan_znwiki/entity/entity_type_fusion', filename), 'w', encoding='utf-8') as f:
        for entity in fusion_set:
            f.write(entity + '\n')