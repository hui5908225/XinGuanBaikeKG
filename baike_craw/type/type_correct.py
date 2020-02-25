import os
from process.process_utils import get_triple

# disease_set = set()
# with open(os.path.join('../data/xinguan_hudongbaike/entity/entity_type_fusion', 'hudongbaike_confict_entity.txt'), 'r', encoding='utf-8') as f:
#     for line in f:
#         if line and line.strip():
#             s, p, o = get_triple(line)
#             if s == 'virus' and p == 'disease':
#                 disease_set.add(o.strip('\n'))
#
# virus_set = set()
# with open(os.path.join('../data/xinguan_hudongbaike/entity/entity_type_fusion', 'hudongbaike_virus_entity.txt'), 'r', encoding='utf-8') as f:
#     for line in f:
#         if line and line.strip():
#             virus_set.add(line.strip('\n'))
#     f.close()
#
# for disease in disease_set:
#     virus_set.remove(disease)
#
# with open(os.path.join('../data/xinguan_hudongbaike/entity/entity_type_fusion', 'hudongbaike_virus_entity_corrected.txt'), 'w', encoding='utf-8') as f:
#     for virus in virus_set:
#         f.write(virus + '\n')



bacteria_set = set()
with open(os.path.join('../data/xinguan_hudongbaike/entity/entity_type_fusion', 'hudongbaike_confict_entity.txt'), 'r', encoding='utf-8') as f:
    for line in f:
        if line and line.strip():
            s, p, o = get_triple(line)
            if s == 'bacteria' and p == 'disease':
                bacteria_set.add(o.strip('\n'))

virus_set = set()
with open(os.path.join('../data/xinguan_hudongbaike/entity/entity_type_fusion', 'hudongbaike_bacteria_entity.txt'), 'r', encoding='utf-8') as f:
    for line in f:
        if line and line.strip():
            virus_set.add(line.strip('\n'))
    f.close()

for bacteria in bacteria_set:
    virus_set.remove(bacteria)

with open(os.path.join('../data/xinguan_hudongbaike/entity/entity_type_fusion', 'hudongbaike_bacteria_entity.txt'), 'w', encoding='utf-8') as f:
    for virus in virus_set:
        f.write(virus + '\n')