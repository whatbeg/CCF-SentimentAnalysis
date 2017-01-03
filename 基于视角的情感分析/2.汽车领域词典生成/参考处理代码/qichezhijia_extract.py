# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 15:52:44 2016

@author: Archer
"""
import json

path='F:\\1-program\\1.3-contest\-ccf\quarter-final\\view_extraction\\'

def del_qichezhijia(text_path,result_path):
    view_result = []
    fw=open(path + result_path, 'w', encoding='utf-8')
    index=0
    with open(path + text_path, encoding='utf-8') as f:
        brand = ''
        company = ''
        detail = []
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
                        for key in detail:
                            print(brand+'#'+company+'#'+key)
                            fw.write(brand+'#'+company+'#'+key+'\n')
                        detail=[]
                    else:
                        if '}' not in line:
                            detail.append(line.split(',')[0].strip().replace('"','').replace('(进口)',''))
    fw.close()


def exception(text_path,result_path):
    brand_company=[]
    view_result=[]
    fw=open(path+result_path,'w',encoding='utf-8')
    with open(path+text_path,encoding='utf-8') as f:
        for line in f:
            brand,company,detail=line.split('#')
            brand=brand.replace('(海外)','').strip('\n')
            company=company.replace('(海外)','').strip('\n')
            detail=detail.replace('(海外)','').strip('\n')
            # content=brand
            # if not company.startswith(brand) and not company.endswith(brand):
            #     if content not in brand_company:
            #         brand_company.append(content)
            if company == brand:
                # view_1=brand+'#'+company
                # if view_1 not in brand_company:
                #     brand_company.append(view_1)
                if company == '奥迪':
                    if not detail.startswith(company):
                        view_1=company+detail
                        if view_1 != '':
                            if view_1 not in view_result:
                                view_result.append(view_1)
                    if detail not in view_result:
                        view_result.append(detail)
                    if company not in view_result:
                        view_result.append(company)
                    continue
                if company == '悍马':
                    if detail not in view_result:
                        view_result.append(detail)
                    if company not in view_result:
                        view_result.append(company)
                    continue
                if company == '江铃集团新能源':
                    if detail not in view_result:
                        view_result.append(detail)
                    continue
                if company == '汉腾汽车':
                    if company not in view_result:
                        view_result.append(company)
                    if detail not in view_result:
                        view_result.append(detail)
                    continue
                if company == 'LYNK&CO':
                    if detail== '01概念车':
                        if 'LYNK&CO 01' not in view_result:
                            view_result.append('LYNK&CO 01')
                    if detail == 'LYNK&CO CX11':
                        if detail not in view_result:
                            view_result.append(detail)
                    if company not in view_result:
                        view_result.append(company)
                    continue
                if company == 'Zenvo' or company == '迈巴赫':
                    if company not in view_result:
                        view_result.append(company)
                    continue
                if company == '长城汽车' or company == '野马汽车' or company=='成功汽车' or company=='莲花汽车' or company=='吉利汽车' \
                        or company=='力帆汽车' or company == '猎豹汽车':
                    if detail == '欧拉':
                        if '长城欧拉' not in view_result:
                            view_result.append('长城欧拉')
                    else:
                        co=company.replace('汽车','')
                        if not detail.startswith(co):
                            view_1=co+detail
                            if view_1 not in view_result:
                                view_result.append(view_1)
                        if company not in view_result:
                            view_result.append(company)
                        if detail not in view_result:
                            view_result.append(detail)
                    continue
                if company == '路虎':
                    if not detail.startswith('第一代'):
                        if detail not in view_result:
                            view_result.append(detail)
                        if not detail.startswith(company):
                            view_1=company+detail
                            if view_1 not in view_result:
                                view_result.append(view_1)
                    continue
                if company ==  '安凯客车':
                    view_1='安凯宝斯通'
                    if view_1 not in view_result:
                        view_result.append(view_1)
                    if company not in view_result:
                        view_result.append(company)
                    if detail not in view_result:
                        view_result.append(detail)
                    continue
                if company == '依维柯':
                    if company not in view_result:
                        view_result.append(company)
                    if detail not in view_result:
                        view_result.append(detail)
                    continue
                if company == '萨博':
                    if company not in view_result:
                        view_result.append(company)
                    if detail not in view_result:
                        view_result.append(detail)
                    view_1=company+detail.split()[1]
                    if view_1 not in view_result:
                        view_result.append(view_1)
                    continue
                if  not detail.startswith(company):
                    view_1=company+detail
                    if view_1 not in view_result:
                        view_result.append(view_1)
                if company not in view_result:
                    view_result.append(company)
                if detail not in view_result:
                    view_result.append(detail)
            else:
                if company.startswith(brand):
                    # view_1 = brand + '#' + company
                    # if view_1 not in brand_company:
                    #     brand_company.append(view_1)
                    if company==brand+'汽车':
                        #print(brand+'#'+company)
                        view_1=company+detail.replace(brand,'')
                        view_2=brand+detail.replace(brand,'')
                        if view_1 not in view_result:
                            view_result.append(view_1)
                        if view_2 not in view_result:
                            view_result.append(view_2)
                        if company not in view_result:
                            view_result.append(company)
                        if detail not in view_result:
                            view_result.append(detail)
                    else:
                        #print(brand+'#'+company)
                        if company == '奥迪RS' or company == '雷克萨斯F' or company== 'MINI JCW' or company=='游侠电车' \
                                or company=='海马郑州' or company == '宝马M':
                            if company not in view_result:
                                view_result.append(company)
                            if detail not in view_result:
                                view_result.append(detail)
                            if brand not in view_result:
                                view_result.append(brand)
                        if company == '一汽吉林'or company =='光冈自动车' or company=='沃尔沃亚太':
                            co=detail.split()[0]
                            view_1=brand+co
                            if co not in view_result:
                                view_result.append(co)
                            if company not in view_result:
                                view_result.append(company)
                            if brand not in view_result:
                                view_result.append(brand)
                            if view_1 not in view_result:
                                view_result.append(view_1)
                            if company != '沃尔沃亚太':
                                view_2 = company + co
                                if view_2 not in view_result:
                                    view_result.append(view_2)
                else:
                    if company.endswith(brand):
                        if detail not in view_result:
                            view_result.append(detail)
                        view_1=company+detail.replace(brand,'')
                        if not detail.startswith(brand):
                            view_2=brand+detail
                            if view_2 not in view_result:
                                view_result.append(view_2)
                        if view_1 not in view_result:
                            view_result.append(view_1)
                    else:
                        if brand == '潍柴英致' or brand=='纳智捷' or brand=='五菱汽车' or brand=='驭胜' or brand=='东风风光' \
                                or brand=='领志' or brand == '长江EV' or brand=='海格' or brand=='华凯' or brand=='福田乘用车'\
                                or brand=='MG':
                            view_1 = '潍柴' + detail
                            if brand=='纳智捷':
                                view_1 = brand + detail
                            if brand=='五菱汽车' or brand=='领志'or brand=='海格':
                                view_1 = company + detail
                                if detail.startswith('五菱'):
                                    view_1 = '上海通用' + detail
                            if brand=='驭胜' or brand=='华凯' or brand=='福田乘用车':
                                view_2=company+detail
                                if view_2 not in view_result:
                                    view_result.append(view_2)
                                view_1=company.replace('汽车','')
                            if brand == 'MG':
                                view_1 = '上汽' + brand
                                view_2 = '上汽' + brand + detail.replace(brand, '')
                                if view_2 not in view_result:
                                    view_result.append(view_2)
                            if brand=='东风风光' or brand=='长江EV':
                                view_1=''
                            if view_1!='' and view_1 not in view_result:
                                view_result.append(view_1)
                            if detail not in view_result:
                                view_result.append(detail)
                            if company not in view_result:
                                view_result.append(company)
                            if brand not in view_result:
                                view_result.append(brand)
                        if brand=='DS' or brand=='东风'or brand=='大发':
                            view_1= brand+' '+detail
                            if detail.startswith(brand):
                                view_1=detail
                            view_2=company+view_1
                            if brand == '东风':
                                view_1 = brand + company + detail
                                view_2 = company + detail
                            if brand=='大发':
                                view_1 = company+brand + detail
                                view_2 = company + detail
                                view_3=brand+detail
                                if view_3 not in view_result:
                                    view_result.append(view_3)
                            if detail not in view_result:
                                view_result.append(detail)
                            if company not in view_result:
                                view_result.append(company)
                            if brand not in view_result:
                                view_result.append(brand)
                            if view_1 not in view_result:
                                view_result.append(view_1)
                            if view_2 not in view_result:
                                view_result.append(view_2)
                        if brand == '广汽传祺' or brand=='哈弗' or brand=='ARCFOX' or brand=='三菱' or brand=='宝骏' or brand=='华骐'\
                                 or brand=='之诺' or brand=='克莱斯勒':
                            view_1=detail
                            if not detail.startswith('传祺'):
                                view_1='传祺'+detail
                            view_2='广汽'+detail
                            if brand =='哈弗':
                                view_1='长城'+detail
                                view_2=''
                            if brand=='之诺':
                                view_1=company+brand
                                view_2=company+detail
                                if company not in view_result:
                                    view_result.append(company)
                            if brand=='克莱斯勒':
                                view_1=brand+' '+company
                                view_2=company
                            if brand=='ARCFOX':
                                view_1=company+detail
                                view_2=''
                            if brand=='三菱':
                                view_1=brand+detail.replace(brand,'')
                                view_2='东南'+view_1
                            if brand=='宝骏':
                                view_1=company+brand
                                view_2=company+detail
                                if company not in view_result:
                                    view_result.append(company)
                            if brand=='华骐':
                                view_1=company+brand
                                view_2=company+detail
                                if company not in view_result:
                                    view_result.append(company)
                            if brand not in view_result:
                                view_result.append(brand)
                            if view_1 not in view_result:
                                view_result.append(view_1)
                            if view_2!='' and view_2 not in view_result:
                                view_result.append(view_2)
                            if detail not in view_result:
                                view_result.append(detail)
                        if brand=='SPIRRA' :
                            view_1=company+brand
                            view_2='思派朗'
                            if brand not in view_result:
                                view_result.append(brand)
                            if view_1 not in view_result:
                                view_result.append(view_1)
                            if view_2!='' and view_2 not in view_result:
                                view_result.append(view_2)
                            if company not in view_result:
                                view_result.append(company)
                        if brand=='北汽威旺' or brand=='上海':
                            if brand=='上海':
                                brand='上汽'
                            if brand not in view_result:
                                view_result.append(brand)
                            if detail not in view_result:
                                view_result.append(detail)
                        if brand=='朗世':
                            view_1=company+detail
                            if view_1 not in view_result:
                                view_result.append(view_1)
                            if company not in view_result:
                                view_result.append(company)
                            if detail not in view_result:
                                view_result.append(detail)
                        if brand=='奔驰':
                            for key in [brand,company,detail]:
                                if key not in view_result:
                                    view_result.append(key)
                        if brand=='启辰':
                            view_1=company+brand
                            view_2=company+detail
                            for key in [brand,company,detail,view_1,view_2]:
                                if key not in view_result:
                                    view_result.append(key)
                        if brand=='道奇':
                            for key in [brand,company,detail]:
                                if key not in view_result:
                                    view_result.append(key)
                            if company=='东南汽车':
                                view_1='东南'+brand
                                view_2='东南'+brand+detail
                                for key in [view_1,view_2]:
                                    if key not in view_result:
                                        view_result.append(key)
                        if brand=='荣威':
                            view_1=brand+detail.replace(brand,'')
                            view_2='上汽'+brand
                            view_3='上汽'+view_1
                            for key in [brand,detail,view_1,view_2,view_3]:
                                if key not in view_result:
                                    view_result.append(key)
                        if brand=='北汽绅宝' or brand=='Jeep' or brand=='华利':
                            view_1=brand+'CC'
                            if brand=='Jeep' or brand=='华利':
                                view_1=company
                            for key in [brand,detail,view_1]:
                                if key not in view_result:
                                    view_result.append(key)
                        if brand=='WEY' or brand=='威麟' or brand=='瑞麒' or brand=='黄海':
                            view_1=company+brand
                            view_2=company+detail
                            if brand == '威麟' or brand=='瑞麒' or brand=='黄海':
                                view_1 = company.replace('汽车','') + brand
                                view_2 = company.replace('汽车','')+ detail
                            for key in [brand, detail, view_1,view_2,company]:
                                if key not in view_result:
                                    view_result.append(key)
                        if brand=='金杯':
                            view_1='华晨鑫源金杯750'
                            view_2='华晨金杯T32'
                            view_3='华晨鑫源金杯T32'
                            for key in [view_1,view_2,view_3,brand,company,detail]:
                                if key not in view_result:
                                    view_result.append(key)
                        if brand=='长安商用':
                            view_1 = brand + detail
                            if view_1 not in view_result:
                                view_result.append(view_1)
                            if detail not in view_result:
                                view_result.append(detail)
                            if '长安汽车' not in view_result:
                                view_result.append('长安汽车')
    for key in view_result:
        fw.write(key+'\n')
        #print(key)





def compare(text_path1,text_path2,result_path):
    qi_list=[]
    tai_list=[]
    fw=open(path+result_path,'w',encoding='utf-8')
    with open(path+text_path1,encoding='utf-8') as f:
        for line in f:
            qi_list.append(line.strip('\n'))
    print('over')
    with open(path+text_path2,encoding='utf-8') as f:
        for line in f:
            tai_list.append(line.strip('\n'))
    print('over')
    for key in qi_list:
        if key not in tai_list:
            fw.write(key+'\n')

def extract_view(text_path,result_path):
    fw=open(path+result_path,'w',encoding='utf-8')
    with open(path+text_path,encoding='utf-8') as f:
        next(f)
        for line in f:
            view=line.split('\t')[1].strip()
            fw.write(view+'\n')
    fw.close()

def del_text(text_path,result_path):
    list=[]
    fw = open(path + result_path, 'w', encoding='utf-8')
    with open(path+text_path,encoding='utf-8') as f:
        for line in f:
            view=line.strip('\n')
            if view not in list:
                list.append(view)
    print(len(list))
    for key in list:
        fw.write(key+'\n')

    fw.close()

def filter_view(text_path,result_path):
    list=[]
    fw=open(path+result_path,'w',encoding='utf-8')
    with open(path+text_path,encoding='utf-8') as f:
        for line in f:
            content = line.strip('\n').replace('全新','').replace('运动版','').replace('经典','')
            if content not in list:
                list.append(content)
    for key in list:
        fw.write(key+'\n')
    fw.close()



if __name__ == '__main__':
    #del_qichezhijia('qichezhijiacars.json','deal_qichezhijiacars.txt')
    #filter('brand_all.txt','brand_user.txt')
    #exception('exception_qichezhijia.txt','222222.txt')
    #compare('deal_qichezhijiacars.txt','deal_taipingyangcars.txt','exception_qichezhijia.txt')
    #extract_view('Label.csv','333.txt')
    del_text('user.txt','final_user_1.txt')
    #filter_view('new_brand.txt','new_new-brand.txt')
