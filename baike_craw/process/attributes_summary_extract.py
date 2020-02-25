from urllib.parse import unquote
import os
import os.path
from bs4 import BeautifulSoup
from craw.craw_utils import sep
import re
import json


def clean(s):
    s = re.sub(r'\s+', '', s)
    if s.endswith('：'):
        s = s[:-1]
    return s


def extract_summary():
    entity_set = set()

    # i = 1,2 ...,12
    i = 12
    file_name = 'entity_pages_' + str(i) + '.xml'
    with open(os.path.join('../data/xinguan_hudongbaike/entity_page', file_name), 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
        all_page = soup.find_all('page')
        dict = {}
        # 科
        ke_regex = re.compile('(\u5c5e\u4e8e|\u5c5e)([\u4e00-\u9fa5]+)\u79d1')
        # 界
        jie_regex = re.compile('(\u5c5e\u4e8e|\u5c5e)([\u4e00-\u9fa5]+)\u754c')
        # 属
        shu_regex = re.compile('(\u5c5e\u4e8e|\u5c5e)([\u4e00-\u9fa5]+)\u5c5e')
        # 目
        mu_regex = re.compile('(\u5c5e\u4e8e|\u5c5e)([\u4e00-\u9fa5]+)\u76ee')
        # 形状 呈\具XX形
        shape_1 = re.compile('(\u5448|\u5177)([\u4e00-\u9fa5]+)\u5f62')
        # 呈XX结构
        shape_2 = re.compile('\u5448([\u4e00-\u9fa5]+)\u7ed3\u6784')
        # 为XX状
        shape_3 = re.compile('\u4e3a([\u4e00-\u9fa5]+)\u72b6')

        # 传播途径 通过XX传播
        spread_1 = re.compile('\u901a\u8fc7([\u4e00-\u9fa5]+)\u4f20\u64ad')
        # 经XX感染
        spread_2 = re.compile('\u7ecf([\u4e00-\u9fa5]+)\u611f\u67d3')
        # 以XX方式传播
        spread_3 = re.compile('\u4ee5([\u4e00-\u9fa5]+)\u65b9\u5f0f\u4f20\u64ad')

        # 医学专科
        division = re.compile('(\u5230|\u53bb|\u6cbb\u7597)([\u4e00-\u9fa5]+)\u79d1')

        # 发病部位   引起XX感染  引起XX不适
        body = re.compile('\u5f15\u8d77([\u4e00-\u9fa5]+)(\u611f\u67d3|u4e0d\u9002)')
        # 临床表现   主要症状是XXX
        symptom_1 = re.compile('\u4e3b\u8981\u75c7\u72b6\u662f([\u4e00-\u9fa5]+)(\u3002|\uff0c)')
        # 出现XXX症状
        symptom_2 = re.compile('\u51fa\u73b0([\u4e00-\u9fa5]+)\u75c7\u72b6')
        # 临床表现主要有XX
        symptom_3 = re.compile('\u4e34\u5e8a\u8868\u73b0\u4e3b\u8981\u6709([\u4e00-\u9fa5]+)(\u3002|\uff0c)')

        # 常见病因 发病机制是XX
        reason_1 = re.compile('\u53d1\u75c5\u673a\u5236\u662f([\u4e00-\u9fa5]+)(\u3002|\uff0c)')
        # 由于XXX引起 由XXX引起 由于XXX所引起
        reason_2 = re.compile('(\u7531|\u7531\u4e8e)([\u4e00-\u9fa5]+)(\u6240\u5f15\u8d77|\u5f15\u8d77)')

        # 病原类型   由XX病毒引起 由XX细菌引起
        ill_type_1 = re.compile('\u7531([\u4e00-\u9fa5]+)\u75c5\u6bd2\u5f15\u8d77')
        ill_type_2 = re.compile('\u7531([\u4e00-\u9fa5]+)\u7ec6\u83cc\u5f15\u8d77')
        # 类型 分类
        type = re.compile('\u5206\u7c7b(\u003a|\uff1a)([\u4e00-\u9fa5]+)(\u3002|\uff0c)')

        # 剂量
        dose_1 = re.compile('\u3010\u7528\u6cd5\u7528\u91cf\u3011([\u4e00-\u9fa5]+)(\u3002|\uff0c)')
        dose_2 = re.compile('\u3010\u7528\u6cd5\u3011([\u4e00-\u9fa5]+)(\u3002|\uff0c)')
        dose_3 = re.compile('\u7528\u6cd5\u7528\u91cf(\u003a|\uff1a)([\u4e00-\u9fa5]+)(\u3002|\uff0c)')

        # 是否处方药
        prescription = re.compile('(\u975e\u5904\u65b9\u836f)+')

        # 不良反应 不良反应有XXXX
        reaction = re.compile('\u4e0d\u826f\u53cd\u5e94(\u6709|\uff1a|\u003a)([\u4e00-\u9fa5]+)(\u3002|\uff0c)')

        # 禁忌
        taboo = re.compile('(\u3002|\uff0c)([\u4e00-\u9fa5]+)(\u4e0d\u5b9c\u4f7f\u7528|\u5fcc\u7528|\u7981\u7528)')
        for page in all_page:
            property_value = {}
            if page.title:
                title = page.title.string
                property_value['名称'] = title
                summary = page.find('div', {'class': 'summary'})
                label_div = page.find('div', {'class': 'place'})
                if summary and label_div:
                    ke = ke_regex.findall(summary.get_text())
                    jie = jie_regex.findall(summary.get_text())
                    shu = shu_regex.findall(summary.get_text())
                    mu = mu_regex.findall(summary.get_text())
                    shape1 = shape_1.findall(summary.get_text())
                    shape2 = shape_2.findall(summary.get_text())
                    shape3 = shape_3.findall(summary.get_text())
                    spread1 = spread_1.findall(summary.get_text())
                    spread2 = spread_2.findall(summary.get_text())
                    spread3 = spread_3.findall(summary.get_text())
                    divis = division.findall(summary.get_text())
                    bod = body.findall(summary.get_text())
                    symptom1 = symptom_1.findall(summary.get_text())
                    symptom2 = symptom_2.findall(summary.get_text())
                    symptom3 = symptom_3.findall(summary.get_text())
                    reason1 = reason_1.findall(summary.get_text())
                    reason2 = reason_2.findall(summary.get_text())
                    ill1 = ill_type_1.findall(summary.get_text())
                    ill2 = ill_type_2.findall(summary.get_text())
                    ty = type.findall(summary.get_text())
                    dose1 = dose_1.findall(summary.get_text())
                    dose2 = dose_2.findall(summary.get_text())
                    dose3 = dose_3.findall(summary.get_text())
                    pre = prescription.findall(summary.get_text())
                    rea = reaction.findall(summary.get_text())
                    tab = taboo.findall(summary.get_text())

                    if len(ke) > 0:
                        property_value['科'] = ke[0][1]
                    if len(jie) >0:
                        property_value['界'] = jie[0][1]
                    if len(shu) >0:
                        property_value['属'] = shu[0][1]
                    if len(mu) >0:
                        property_value['目'] = mu[0][1]
                    if len(shape1) >0:
                        property_value['病毒形状'] = shape1[0][1] + '形'
                    if len(shape2) >0:
                        property_value['病毒形状'] = shape2[0] + '结构'
                    if len(shape3) >0:
                        property_value['病毒形状'] = shape3[0] + '状'
                    if len(spread1) >0:
                        property_value['传播途径'] = spread1[0] + '传播'
                    if len(spread2) >0:
                        property_value['传播途径'] = spread2[0] + '感染'
                    if len(spread3) >0:
                        property_value['传播途径'] = spread3[0] + '方式传播'
                    if len(divis) > 0:
                        property_value['医学专科'] = divis[0][1] + '科'
                    if len(bod) > 0:
                        property_value['发病部位'] = bod[0][0]
                    if len(symptom1) > 0:
                        property_value['临床表现'] = symptom1[0][0]
                    if len(symptom2) > 0:
                        property_value['临床表现'] = symptom2[0]
                    if len(symptom3) > 0:
                        property_value['临床表现'] = symptom3[0][0]
                    if len(reason1) > 0:
                        property_value['常见病因'] = reason1[0][0]
                    if len(reason2) > 0:
                        property_value['常见病因'] = reason2[0][1]
                    if len(ill1) > 0:
                        property_value['病原类型'] = ill1[0] + '病毒'
                    if len(ill2) > 0:
                        property_value['病原类型'] = ill2[0] + '细菌'
                    if len(ty) > 0:
                        property_value['分类'] = ty[0][1]
                    if len(dose1) > 0:
                        property_value['剂量'] = dose1[0][0]
                    if len(dose2) > 0:
                        property_value['剂量'] = dose2[0][0]
                    if len(dose3) > 0:
                        property_value['剂量'] = dose3[0][1]
                    if len(pre) > 0:
                        property_value['非处方药'] = '是'
                    if len(rea) > 0:
                        property_value['不良反应'] = rea[0][1]
                    if len(tab) >0:
                        property_value['禁忌'] = tab[0][1]
            dict[title] = property_value
        f.close()
    w_file_name = 'property_' + str(i)+ '.json'
    wf = open(os.path.join('../data/xinguan_hudongbaike/property_extract_from_text', w_file_name), 'w', encoding='utf-8')
    json.dump(dict, wf, ensure_ascii=False, indent=4)
if __name__ == '__main__':
    extract_summary()
    # text = '恶邮差”病毒，四级恶性蠕虫病毒“恶邮差”英文名称Worm.Supnot.78858.c，是蠕虫Supnot的最新变种，且改进了以前版本通过邮件传播方面的性能，手段极其“恶毒'
    # dose_1 = re.compile('\u3010\u7528\u6cd5\u7528\u91cf\u3011([\u4e00-\u9fa5]+)(\u3002|\uff0c)')
    # dose_2 = re.compile('\u3010\u7528\u6cd5\u3011([\u4e00-\u9fa5]+)(\u3002|\uff0c)')
    # dose_3 = re.compile('\u7528\u6cd5\u7528\u91cf(\u003a|\uff1a)([\u4e00-\u9fa5]+)(\u3002|\uff0c)')
    # dose1 = dose_1.findall(text)
    # dose2 = dose_2.findall(text)[0][0]
    # dose3 = dose_3.findall(text)
    # print()

    # text = '由撒打算你病毒引起'
    # ke_regex = re.compile('\u7531([\u4e00-\u9fa5]+)\u75c5\u6bd2\u5f15\u8d77')
    # d = ke_regex.findall(text)[0]
    # print()