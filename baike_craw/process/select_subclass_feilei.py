    # ('TOP', '病毒'),
    # ('TOP', '疾病'),
    # ('TOP', '细菌'),
    # ('TOP', '药品'),
    # ('TOP', '症状'),
    # ('TOP', '医疗'),
    # ('TOP', '医学'),
    # ('TOP', '健康')

import os

def output_subclass_list(current_class, layer, pair_list):
    subclass_list = []
    for i in range(layer*2)  :
        print("-" ,end="")
    print(current_class)
    for pair in pair_list:
        if pair[0] == current_class:
            subclass_list.append(pair[1])
    for subclass in subclass_list:
        output_subclass_list(subclass, layer+1, pair_list)

if __name__ == '__main__':
    hudong_pair_list = []
    baidu_pair_list = []
    with open(os.path.join('../data/xinguan_hudongbaike', 'hudongbaike_fenlei_subclass_bigram.txt'), 'r',
              encoding='utf-8') as f:
        line = f.readline()
        while line != '':
            pair = line.strip('\n').split(';;;;ll;;;;')
            hudong_pair_list.append((pair[0], pair[1]))
            line = f.readline()
    with open(os.path.join('../data/xinguan_baidubaike', 'baidubaike_fenlei_subclass_bigram.txt'), 'r',
              encoding='utf-8') as f:
        line = f.readline()
        while line != '':
            pair = line.strip('\n').split(';;;;ll;;;;')
            baidu_pair_list.append((pair[0], pair[1]))
            line = f.readline()
    layer = 0
    top = "医疗检测"
    print("互动百科:")
    output_subclass_list(top, layer, hudong_pair_list)
    print("百度百科:")
    output_subclass_list(top, layer, baidu_pair_list)

