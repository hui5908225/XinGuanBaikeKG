import os
import json

count = 0
with open(os.path.join('../data/final/property/baidubaike', 'speciality_entity_property_final.json'), 'r', encoding='utf-8') as f:
    dict = json.load(f)

for item in dict.items():
    for pair in item[1].items():
        if pair[1] != 'NULL' or pair[1] != '':
            count = count + 1
print(count)

# property
# bacteria 1396 + 3960 + 396 + 511
# disease  6398 + 49490 + 84492 + 1350
# drug 4740 + 69126 + 0 + 1267
# virus 1330 + 1356 + 315 + 301
# symptom 17442 + 16443
# inspect 245 + 190
# speciality 182 + 224

#sameas
# 3616

#relation
# 15401