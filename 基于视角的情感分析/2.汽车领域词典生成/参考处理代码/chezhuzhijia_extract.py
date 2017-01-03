# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 15:52:44 2016

@author: Archer
"""
import re
import string
path='F:\\1-program\\1.3-contest\-ccf\quarter-final\\view_extraction\\'


def deal_chezhuzhijia(file_path,result_path):
    """
    deal the view from chezhuzhijia website
    :param path:
    :return:
    """
    with open(path+file_path,encoding='utf-8') as f:
        view_result=[]
        view_result.append('DS神韵')
        #index=0
        fw=open(path + result_path,'w',encoding='utf-8')
        index=1
        for line in f:
            line_split=line.replace('{','').replace('}','').split(',')
            brand=line_split[0].split(':')[1].replace('"','').replace('"','').strip()
            company=line_split[2].split(':')[1].replace('"','').replace('"','').strip()
            detail=line_split[3].split(':')[1].replace('"','').replace('"','').strip()
            #print(brand + '#' + company + '#' + detail)
            #print(brand+'#'+company+'#'+detail)
            #index+=1
            '''
            deal with the exception
            '''
            if brand == '阿尔法·罗密欧':
                print(brand+'#'+company+'#'+detail)
                view=company+detail
                if view not in view_result:
                    view_result.append(view)
                if company not in view_result:
                    view_result.append(company)
                index += 1
                continue

            if brand== '北汽绅宝':
                print(brand+'#'+company+'#'+detail)
                brand_deal=brand.replace('绅宝','')
                view=brand_deal+detail
                if view not in view_result:
                    view_result.append(view)
                if brand not in view_result:
                    view_result.append(brand)
                if detail not in view_result:
                    view_result.append(detail)
                index += 1
                continue

            if brand == '北汽制造':
                print(brand+'#'+company+'#'+detail)
                if '北汽' not in detail:
                    view_1 = '北汽'+detail
                    if view_1 not in view_result:
                        view_result.append(view_1)
                if '北京' not in detail:
                    view_2 = '北京'+detail
                    if view_2 not in view_result:
                        view_result.append(view_2)
                if detail not in view_result:
                    view_result.append(detail)
                index += 1
                continue

            if company == '长安轻型车':
                print(brand+'#'+company+'#'+detail)
                view= '长安商用'+detail
                if detail not in view_result:
                    view_result.append(detail)
                if view not in view_result:
                    view_result.append(view)
                if '长安商用' not in view_result:
                    view_result.append('长安商用')
                index += 1
                continue

            if company == '长安跨越':
                print(brand+'#'+company+'#'+detail)
                if detail not in view_result:
                    view_result.append(detail)
                index += 1
                continue

            if brand == '东风':
                print(brand+'#'+company+'#'+detail)
                view='东风郑州日产'+detail
                if detail not in view_result:
                    view_result.append(detail)
                if view not in view_result:
                    view_result.append(view)
                index += 1
                continue

            if brand == '福汽新龙马':
                print(brand+'#'+company+'#'+detail)
                if brand not in view_result:
                    view_result.append(brand)
                view='福汽'+detail
                if detail not in view_result:
                    view_result.append(detail)
                if view not in view_result:
                    view_result.append(view)
                index += 1
                continue

            if brand== '黄海':
                print(brand+'#'+company+'#'+detail)
                if brand not in view_result:
                    view_result.append(brand)
                if company not in view_result:
                    view_result.append(company)
                if detail not in view_result:
                    view_result.append(detail)
                view_1= brand+detail
                view_2=company+detail
                if view_1 not in view_result:
                    view_result.append(view_1)
                if view_2 not in view_result:
                    view_result.append(view_2)
                index += 1
                continue

            if brand== 'SPIRRA':
                print(brand+'#'+company+'#'+detail)
                if brand not in view_result:
                    view_result.append(brand)
                if company not in view_result:
                    view_result.append(brand)
                if detail not in view_result:
                    view_result.append(detail)
                index += 1
                continue

            if brand == '纳智捷':
                print(brand+'#'+company+'#'+detail)
                view_1=brand+detail
                view_2=company+brand+detail
                if brand not in view_result:
                    view_result.append(brand)
                if company not in view_result:
                    view_result.append(company)
                if detail not in view_result:
                    view_result.append(detail)
                if view_1 not in view_result:
                    view_result.append(view_1)
                if view_2 not in view_result:
                    view_result.append(view_2)
                index += 1
                continue

            if brand == '迷你MINI':
                print(brand+'#'+company+'#'+detail)
                if company not in view_result:
                    view_result.append(company)
                if detail not in view_result:
                    view_result.append(detail)
                index += 1
                continue

            if brand == '猎豹':
                print(brand+'#'+company+'#'+detail)
                view_1=company+brand
                view_2= company+brand+detail
                if brand not in view_result:
                    view_result.append(brand)
                if detail not in view_result:
                    view_result.append(detail)
                if view_1 not in view_result:
                    view_result.append(view_1)
                if view_2 not in view_result:
                    view_result.append(view_2)
                index += 1
                continue

            if brand == '金杯':
                print(brand+'#'+company+'#'+detail)
                view_1= '华晨'+brand+detail
                view_2=brand+detail
                if detail not in view_result:
                    view_result.append(detail)
                if view_1 not in view_result:
                    view_result.append(view_1)
                if view_2 not in view_result:
                    view_result.append(view_2)
                index += 1
                continue

            if brand == 'JEEP':
                print(brand+'#'+company+'#'+detail)
                view_1=''
                view_2=''
                view_3=''
                if detail == '大切诺基':
                    view_1=brand+detail
                    view_2=company+detail
                    view_3='北京'+detail
                if detail == '大切诺基 SRT':
                    view_2= brand+detail
                    view_3='北京'+detail
                if view_1 != '' and view_1 not in view_result:
                    view_result.append(view_1)
                if view_2 != '' and view_2 not in view_result:
                    view_result.append(view_2)
                if view_3 != '' and view_3 not in view_result:
                    view_result.append(view_3)
                index += 1
                continue

            if brand == '华晨华颂':
                print(brand+'#'+company+'#'+detail)
                view_1=brand + '7'
                if brand not in view_result:
                    view_result.append(brand)
                if company not in view_result:
                    view_result.append(company)
                if detail not in view_result:
                    view_result.append(detail)
                if view_1 not in view_result:
                    view_result.append(view_1)
                index += 1
                continue

            if brand == '长城华冠':
                view_1=brand+detail
                if brand not in view_result:
                    view_result.append(brand)
                if company not in view_result:
                    view_result.append(brand)
                if detail not in view_result:
                    view_result.append(detail)
                if view_1 not in view_result:
                    view_result.append(view_1)
                # exception deal over
            if detail.endswith(brand):
                print(brand+'#'+company+'#'+detail)
                if detail == brand:
                    if detail == company:
                        if detail not in view_result:
                            view_result.append(detail)
                    else:
                        if company.endswith(detail) or company.startswith(detail):
                            if company not in view_result:
                                view_result.append(company)
                        else:
                            view_1= company +detail
                            if view_1 not in view_result:
                                view_result.append(view_1)
                index += 1
                continue

            if detail.startswith(brand):
                print(brand+'#'+company+'#'+detail)
               # fw.write(brand+'#'+company+'#'+detail+'\n')
                if detail not in view_result:
                    view_result.append(detail)
                if company != brand and company.endswith(brand):
                    view_1=company.replace(brand,'')+detail
                    if view_1 not in view_result:
                        view_result.append(view_1)
                index += 1
                continue

            if company.endswith(brand):
                print(brand+'#'+company+'#'+detail)
                #print(brand+'#'+company)
                if company not in view_result:
                    view_result.append(company)
                if detail not in view_result:
                    view_result.append(detail)
                if not detail.startswith(brand):
                    view_1=brand+detail
                    if view_1 not in view_result:
                        view_result.append(view_1)
                index += 1
                continue

            if company.startswith(brand):
                print(brand+'#'+company+'#'+detail)
                if detail not in view_result:
                    view_result.append(detail)
                if company != '奔驰AMG':
                    view_1=company+detail
                    if view_1 not in view_result:
                        view_result.append(view_1)
                index += 1
                continue
        for key in view_result:
            fw.write(key + '\n')

        fw.close()

    print('over')


if __name__ == '__main__':
    deal_chezhuzhijia('chezhuzhijiacars.json','chezhuzhijia_extract.txt')
