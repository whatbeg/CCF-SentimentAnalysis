# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 15:52:44 2016

@author: Archer
"""
import json

path='F:\\1-program\\1.3-contest\-ccf\quarter-final\\view_extraction\\'


def del_taipingyangcars(file_path,result_path):
    view_result=[]
    fw=open(path+result_path,'w',encoding='utf-8')
    with open(path+file_path,encoding='utf-8') as f:
        next(f)
        brand=''
        company=''
        detail=[]

        for line in f:
            if '{' in line:
                brand=line.split(':')[0].strip().replace('"','').replace('(进口)','')
                continue
            else:
                if '[' in line:
                    company=line.split(':')[0].strip().replace('"','').replace('(进口)','')
                    continue
                else:
                    if ']' in line:
                        if company.endswith(brand):
                            view_1=''
                            if company not in view_result:
                                view_result.append(company)
                            for key in detail:
                                if key not in view_result:
                                    view_result.append(key)
                                if not key.startswith(brand):
                                    view_1 = brand + key
                                    if view_1 not in view_result:
                                        view_result.append(view_1)
                                else:
                                    view_1=company.replace(brand,'')+key
                                    if view_1 not in view_result:
                                        view_result.append(view_1)

                        else:
                            if company.startswith(brand):
                                if company==brand+'汽车':
                                    for key in detail:
                                        view_1=brand+key
                                        if view_1 not in view_result:
                                            view_result.append(view_1)
                                        if key not in view_result:
                                            view_result.append(key)
                                else:
                                    if brand != '知豆' and company !='MINI-JCW'and company != '奇瑞新能源' or \
                                        company != '沃尔沃亚太' or company != 'DS（进口）' or company!= '宝马M':
                                        for key in detail:
                                            view_1=company+key
                                            if view_1 not in view_result:
                                                view_result.append(view_1)
                                    for key in detail:
                                        if key not in view_result:
                                            view_result.append(key)
                            else:
                                if brand == '长安商用' or brand == '北汽制造' or brand == 'Jeep':
                                    for key in detail:
                                        view_1= brand +key
                                        if view_1 not in view_result:
                                            view_result.append(view_1)
                                        if key not in view_result:
                                            view_result.append(key)

                                if brand == '北汽绅宝':
                                    for key in detail:
                                        view_1='北汽'+key
                                        if view_1 not in view_result:
                                            view_result.append(view_1)
                                        if key not in view_result:
                                            view_result.append(key)

                                if brand == '黄海':
                                        for key in detail:
                                            if not str(key).startswith(brand):
                                                view_1=brand+key
                                                if view_1 not in view_result:
                                                    view_result.append(view_1)
                                                if key not in view_result:
                                                    view_result.append(key)

                                if brand == '腾势' or brand =='启辰' or brand == '前途' or brand == '思铭' or brand == '宝骏' or brand == '理念'\
                                        or brand == 'DS' or brand == '海格' or  brand == '纳智捷':
                                    for key in detail:
                                        view_1=company+key
                                        if view_1 not in view_result:
                                            view_result.append(view_1)
                                        if key not in view_result:
                                            view_result.append(key)

                                if brand == '金杯' or brand == '北汽幻速' or brand == '赛麟' or brand == '金龙汽车' or brand == '欧睿' \
                                         or brand == '东风风神':
                                    for key in detail:
                                        if key not in view_result:
                                            view_result.append(key)

                                if brand == '英致':
                                    for key in detail:
                                        view_1='潍柴'+key
                                        if view_1 not in view_result:
                                            view_result.append(view_1)
                                        if key not in view_result:
                                            view_result.append(key)

                                if brand == '奔驰':
                                    for key in detail:
                                        view_1=company+'S级'
                                        if view_1 not in view_result:
                                            view_result.append(view_1)
                                        if key not in view_result:
                                            view_result.append(key)

                                if brand == '东风风度':
                                    for key in detail:
                                        view_1=company+key.replace('风度','')
                                        if view_1 not in view_result:
                                            view_result.append(view_1)
                                        if key not in view_result:
                                            view_result.append(key)

                                if brand == '瑞麒' or brand == '捷豹':
                                    for key in detail:
                                        view_1='奇瑞'+key
                                        if view_1 not in view_result:
                                            view_result.append(view_1)
                                        if key not in view_result:
                                            view_result.append(key)

                                if brand == '哈弗' or brand == '克莱斯勒':
                                    for key in detail:
                                        view_1=company.replace('汽车','')+key
                                        if view_1 not in view_result:
                                            view_result.append(view_1)
                                        if key not in view_result:
                                            view_result.append(key)

                                if brand == '广汽传祺':
                                    for key in detail:
                                        view_1='广汽'+key
                                        if view_1 not in view_result:
                                            view_result.append(view_1)
                                        if key not in view_result:
                                            view_result.append(key)

                                if brand == '斯威汽车':
                                    for key in detail:
                                        view_1='华晨'+key
                                        if view_1 not in view_result:
                                            view_result.append(view_1)
                                        if key not in view_result:
                                            view_result.append(key)

                                if brand == 'MG名爵':
                                    for key in detail:
                                        view_1='上汽'+key
                                        if view_1 not in view_result:
                                            view_result.append(view_1)
                                        if key not in view_result:
                                            view_result.append(key)

                                if brand == '明君华凯':
                                    view_1='明君华凯皮卡'
                                    if view_1 not in view_result:
                                        view_result.append(view_1)

                                if brand == '福汽启腾':
                                    for key in detail:
                                        view_1='福汽'+key
                                        if view_1 not in view_result:
                                            view_result.append(view_1)
                                        if key not in view_result:
                                            view_result.append(key)

                                if brand == '五十铃':
                                    for key in detail:
                                        view_1=''
                                        if not key.startswith(brand):
                                            view_1=company.replace('汽车','')+brand+key
                                        else:
                                            view_1 = company.replace('汽车', '')+ key
                                        if view_1 not in view_result:
                                            view_result.append(view_1)
                                        if key not in view_result:
                                            view_result.append(key)
                        detail=[]
                    else:
                        if '}' not in line:
                            detail.append(line.split(',')[0].strip().replace('"','').replace('(进口)',''))
        for key in view_result:
            fw.write(key+'\n')
        fw.close()

def filter(text_path,result_path):
    brand=[]
    with open(path+text_path,encoding='utf-8') as f:
        for line in f:
            view=line.strip('\n')
            if view not in brand:
                brand.append(view)
    fw=open(path+result_path,'w',encoding='utf-8')
    for key in brand:
        fw.write(key+'\n')
    fw.close()












if __name__ == '__main__':
    #del_taipingyangcars('taipingyangcars.json','extract_taipingyangcars.txt')
    filter('brand_all.txt','brand_user.txt')
