# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 15:52:44 2016

@author: Archer
"""
import numpy as np
import jieba
import jieba.posseg as pseg
import re
from sklearn import cross_validation
from sklearn import datasets
from sklearn.linear_model import LogisticRegression


path='F:\\1-program\\1.3-contest\\-ccf\\quarter-final\\improve_result_new\\'
t_seg_text={}
t_text={}
t_view={}
t_view_text={}
t_view_pol={}


def predeal_data(t_path,t_view_path,t_data_result_path,train_or_test,isSecond,isSeg):
    """ deal data: 0 for train_data and 1 for test_data
    """
    jieba.load_userdict(path+'user.dict')
    with open(path+t_path,encoding='utf-8') as f:
        next(f)
        for line in f:
            line_split=line.split('\t')
            key=line_split[0]
            if len(line_split)==2:
                content=line_split[1]
                t_text[key]=content
            else:
                t_seg_text[key]=[]
                t_text[key]=''
    f.close()
    with open(path+t_view_path,encoding='utf-8') as f:
        if train_or_test==0:
            next(f)
        for line in f:
            if train_or_test==0:
                key,view,pol=line.split('\t')
            else:
               # print(line)
                key,view=line.split(' ')

            if train_or_test==0:
                view=view.replace(' ','^')
            else:
                key=key.rstrip()
                view=view.lstrip().strip('\n')
                view=view.replace(' ','^')
            if key not in t_view:
                t_view[key]=[view]
            else:
                t_view[key].append(view)
            if train_or_test==0:
                t_view_pol[key+'\t'+view]=pol.strip('\n')
    f.close()
    # test for extraction of view
    if isSeg:
        view_extract_text(t_text,t_view)
        write_path=''
        if train_or_test==0:
            if isSecond==1:
                write_path='F:\\1-program\\1.3-contest\\-ccf\\quarter-final\\improve_result_new\\train_second_seg\\'
            else:
                write_path='F:\\1-program\\1.3-contest\\-ccf\\quarter-final\\improve_result_new\\train_seg\\'
        else:
            write_path='F:\\1-program\\1.3-contest\\-ccf\\quarter-final\\improve_result_new\\test_seg\\'
        fw=open(write_path+t_data_result_path,'w',encoding='utf-8')
        l=0
        for t in t_view_text.keys():
            if train_or_test==0:
                pol=''
                if t in t_view_pol.keys():
                    pol=t_view_pol[t]
                else:
                    print('error')
                fw.write(t+'\t'+pol+'\t'+str(t_view_text[t].strip('\n'))+'\n')
                l+=1
            else:
                fw.write(t.strip('\n')+'\t'+str(t_view_text[t].strip('\n'))+'\n')
                l+=1
        fw.close()
    else:
        write_path =''
        if train_or_test == 0:
            if isSecond == 1:
                write_path = 'F:\\1-program\\1.3-contest\\-ccf\\quarter-final\\improve_result_new\\train_second\\'
            else:
                write_path = 'F:\\1-program\\1.3-contest\\-ccf\\quarter-final\\improve_result_new\\train\\'
        else:
            write_path = 'F:\\1-program\\1.3-contest\\-ccf\\quarter-final\\improve_result_new\\test\\'
        fw=open(write_path+t_data_result_path,'w',encoding='utf-8')
        l=0
        for t in t_view.keys():
            l=t_view[t]
            #print(t)
            content=t_text[t]
            #print(content)
            for v in l:
                if train_or_test == 0:
                    pol=''
                    t_pol=t.strip('\n')+'\t'+v
                    if t_pol in t_view_pol.keys():
                        pol=t_view_pol[t_pol]
                    else:
                        print('error')
                    fw.write(t.strip('\n')+'\t'+v.strip('\n')+'\t'+pol+'\t'+str(content.strip('\n'))+'\n')
                else:
                    fw.write(t.strip('\n') +'\t'+v.strip('\n')+ '\t' + str(content.strip('\n')) + '\n')
        fw.close()

def seg_text(text_path,train_or_test,isSecond,isSeg,result_path,):
    """
    seg text: 0 for train_text and 1 for test_text
    """
    jieba.load_userdict(path+'user.dict')
    stopwords=[]
    with open(path+'stop_words.txt',encoding='utf-8') as f:
        for line in f:
            stopwords.append(line.strip())
    new_path =get_new_path(train_or_test,isSecond,isSeg)
    fw=open(new_path+result_path,'w',encoding='utf-8')
    with open(new_path+text_path,encoding='utf-8') as f:
        for line in f:
            if train_or_test == 2:
                content=line.strip('\n')
            else:
                line_split=line.split('\t')
                t_id=line_split[0]
                content=line_split[2]
                if train_or_test==0:
                    content=line_split[3]
            seg=jieba.cut(content)
            seg_result=[]
            index=False
            for k in seg:
                k=k.strip().strip('\n')
                if k not in stopwords and k!=' ' and k!='' and not k.isdigit() and not re.match('^[0-9.]+$',k):
                #if k !=' ' and k!='':
                    if(k=='^'):
                        index=True
                    else:
                        if(not index):
                            seg_result.append(k)
                        else:
                            key=k
                            if(len(seg_result)!=0):
                                key=seg_result[-1]+k
                                seg_result[-1]=key
                            else:
                                seg_result.append(key)
                            index=False
            #t_seg_text[t_id]=seg_result
            for k in seg_result:
                k=k.strip()
                fw.write(k+' ')
            fw.write('\n')
            #fw.write(result+'\n')
    fw.close()
    

def view_extract_text(text,view_text):
    for k in text.keys(): # text for in tranin/test
        if k in view_text.keys(): # view text
            text_k=text[k]
            view_list=view_text[k]
            # if there is only one view, give all the text
            if len(view_list)==1:
                key=k+'\t'+view_list[0]
                t_view_text[key]=text_k
            else:
                text_split=list(filter(not_empty,re.split('。|？|!',text_k)))
                # if there is only one sentence, give the whole sentence to all the view
                if len(text_split)==1:
                    for v in view_list:
                        key=k+'\t'+v
                        t_view_text[key]=text_k
                else:
                    order_view={}
                    for v in view_list:
                        v_1=v.replace('^',' ')
                        index=text_k.find(v_1)
                        order_view[v]=index
                    sorted(order_view.items(),key=lambda asd:asd[1],reverse=True)
                    view=[] # get sorted view according to the location of appearance
                    for v in order_view.keys():
                        view.append(v)
                    tag={}
                    fore_tag='' # the fore view
                    back_t=[]
                    back_in=False
                    for t in text_split:
                        for i in range(len(view_list)):
                            i_view=view_list[i]
                            i_view_1=i_view.replace('^',' ')
                            if i_view_1 in t:
                                if t in tag.keys():
                                    tag[t].append(i_view)
                                else:
                                    tag[t]=[i_view]
                                fore_tag=i
                                if back_in:
                                    for m in back_t:
                                        if m in tag.keys():
                                            tag[m].append(i_view)
                                        else:
                                            tag[m]=[i_view]
                                    back_in=False
                                    back_t=[]
                        # if there is no view in t
                        if t not in tag.keys():
                            if fore_tag != '':
                                tag[t]=[view_list[fore_tag]]
                            else:
                                back_in=True
                                back_t.append(t)
                    for t in tag.keys():
                        view_l=tag[t]
                        for v in view_l:
                            key=k+'\t'+v
                            if key in t_view_text.keys():
                                c=t_view_text[key].strip('\n')+"。"+t
                                t_view_text[key]=c
                            else:
                                t_view_text[key]=t
    return t_view_text


def trans_space(raw_path,del_path,train_or_test,isSecond,isSeg):
    new_path=get_new_path(train_or_test,isSecond,isSeg)
    fw=open(new_path+del_path,'w',encoding='utf-8')
    with open(new_path+raw_path,encoding='utf-8') as f:
        for line in f:
            line_split=line.split('\t')
            #print(line)
            key=line_split[1].rstrip('\n')
            result=''
            if train_or_test==0:
                re_k=key.replace('^',' ')
                content=line_split[3]
                co=content
                if(re_k in content):
                    co=content.replace(re_k,key)
                result=line_split[0]+'\t'+line_split[1]+'\t'+line_split[2]+'\t'+co  
            else:
                re_k=key.replace('^',' ')
                content=line_split[2]
                co=content
                if(re_k in content):
                    co=content.replace(re_k,key)
                result=line_split[0]+'\t'+line_split[1]+'\t'+co
            fw.write(result)
           # print(result)
            #fw.write(
    fw.close()
    f.close()


def extract_text(text_path,train_or_test,result_path):
    """
    :param text_path: the path of text
    :param train_or_test: 0 represents train, 1 represents test
    :param result_path: the path of dealed text
    :return: None
    """
    fw=open(path+result_path,'w',encoding='utf-8')
    with open(path+text_path,encoding='utf-8') as f:
        for line in f:
            if train_or_test==0:
                fw.write(line.split('\t')[3].strip('\n'))
                fw.write('\n')
            else:
                fw.write(line.split('\t')[2].strip('\n'))
                fw.write('\n')
    fw.close()


def filter_view(text_path,result_path,train_or_test,isSecond,isSeg):
    """
    delete some view
    :param text_path:
    :param result_path:
    :return:
    """
    jieba.load_userdict(path+'user.dict')
    user_list=[]
    with open(path+'user.dict',encoding='utf-8') as f:
        for line in f:
            v=line.split()[0]
            if v not in user_list:
                user_list.append(v)
    new_path=get_new_path(train_or_test,isSecond,isSeg)
    fw=open(new_path+result_path,'w',encoding='utf-8')
    with open(new_path+text_path,encoding='utf-8') as f:
        li=[]
        for line in f:
            id,view,text=line.split('\t')
            index=False
            # index == True means delete
            for special_word in ['汽车','全新','经典']:
                if special_word in view:
                    view_split=view.strip().split(special_word)
                    #print(view)
                    #print(len(view_split))
                    for key in view_split:
                        #print(key)
                        if key !='':
                            content=id+'\t'+key+'\t'+text.strip('\n')
                            li.append(content)
                    index=True
            del_al_view=['中意','世纪','欢动','女王','3.0','赛马','地球梦','le','如虎','超越']
            del_yg = ['阳光健康', '阳光下', '阳光干练', '阳光充足', '阳光晃的', '明媚的阳光', '阳光之星', '阳光豪生酒店', '阳光路', '阳光照射', '阳光强', \
                      '阳光直接照射', '刺眼的阳光', '外形阳光', '灿烂的阳光', '阳光富有朝气', '阳光丽景', '阳光中', '太阳光谱', '阳光明媚', '阳光之气', '反射阳光', \
                      '阳光财产', '阳光很好', '太阳光', ]
            del_so=['宋江','宋寅哲','宋予乔','宋佳','宋沛霖','宋小宝']
            del_ta=['唐河','唐克沃克','唐侯','唐唯实']
            del_qin=['福秦','秦力洪','秦皇岛']
            if view in del_al_view:
                index=True
                #print(view)
            if view =='阳光':
                for yg in del_yg:
                    if yg in text:
                        index=True
                        #print(text)
            if view == '大陆':
                te=text.replace('林肯大陆','')
                if not '林肯' in te:
                    index=True
            if '新' in view:
                if '新能源' not in view and '全新' not in view and '新世代全顺' not in view:
                    view_s = list(filter(not_empty,view.split('新')))
                    if len(view_s)!=1:
                        for key in view_s:
                            content = id + '\t' + key + '\t' + text.strip('\n')
                            li.append(content)
                    else:
                        v=view_s[0]
                        if v in user_list:
                            content = id + '\t' + v + '\t' + text.strip('\n')
                            li.append(content)
                        else:
                            location=text.find(v)
                            for i in range(6):
                                l_view=text[location:location+i+1]
                                if l_view in user_list:
                                    content = id + '\t' + l_view + '\t' + text.strip('\n')
                                    li.append(content)
                index=True
            if view == '前途':
                if text.find('有前途')+1 == text.find('前途') or text.find('前途')== text.find('前途无量') or \
                                        text.find('前途')== text.find('前途暗淡') or text.find('的前途')+1 == text.find('前途'):
                    index=True
            if view == '新科':
                if '新科技' in text:
                    index=True
            if view == '宋':
                for so in del_so:
                    if so in text:
                        index=True
            if view == '唐':
                for ta in del_ta:
                    if ta in text:
                        index=True
            if view == '秦':
                for qin in del_qin:
                    if qin in text:
                        index=True
            if view.isdigit():
                if view=='408' or view=='380':
                    index=False
                else:
                    del_view=['350','500','300','370','730','30']
                    if view in del_view:
                        index=True
                        #print(view)
                    else:
                        brand_sp=['马力','公里','千克','匹','t','牛','万','多','名','一','个','十','N','迈','/','辆','块']
                        for key in brand_sp:
                            con=view+key
                            if con in text:
                                index=True
                                #print(con)
                        con='$'+view
                        if con in text:
                            index=True
                            #print(con)
            if not index:
                li.append(line.strip('\n'))
            if len(li)==1000:
                for content in li:
                    fw.write(content+'\n')
                li=[]
        if len(li)!=0:
            for content in li:
                fw.write(content+'\n')
    fw.close()


def get_new_path(train_or_test,isSecond,isSeg):
    new_path = ''
    if train_or_test == 0:
        if isSecond == 1:
            if isSeg:
                new_path = 'F:\\1-program\\1.3-contest\\-ccf\\quarter-final\\improve_result_new\\train_second_seg\\'
            else:
                new_path = 'F:\\1-program\\1.3-contest\\-ccf\\quarter-final\\improve_result_new\\train_second\\'
        else:
            if isSeg:
                new_path = 'F:\\1-program\\1.3-contest\\-ccf\\quarter-final\\improve_result_new\\train_seg\\'
            else:
                new_path = 'F:\\1-program\\1.3-contest\\-ccf\\quarter-final\\improve_result_new\\train\\'
    else:
        if isSeg:
            new_path = 'F:\\1-program\\1.3-contest\\-ccf\\quarter-final\\improve_result_new\\test_seg\\'
        else:
            new_path = 'F:\\1-program\\1.3-contest\\-ccf\\quarter-final\\improve_result_new\\test\\'
    return new_path

def not_empty(s):
    return s and s.strip()
                  
if __name__=='__main__':
    # deal train second segment
    # 1 represents segment
    # predeal_data('TrainSecond.csv','LabelSecond.csv','train_second_id_view_pol.txt',0,1,True)
    # trans_space('train_second_id_view_pol.txt', 'train_second_id_view_pol_trans.txt',0,1,True)
    # seg_text('train_second_id_view_pol_trans.txt', 0, 1, True, 'train_second_seg.txt')

    #deal train segment
    # predeal_data('Train.csv', 'Label.csv', 'train_id_view_pol.txt', 0,0,True)
    # trans_space('train_id_view_pol.txt', 'train_id_view_pol_trans.txt', 0,0,True)
    # seg_text('train_id_view_pol_trans.txt', 0, 0, True, 'train_seg.txt')

    # deal test segment
    # predeal_data('Test.csv', 'generate_view.txt', 'test_second_id_view_text.txt', 1,0,True)
    # trans_space('test_second_id_view_text.txt', 'test_second_id_view_trans.txt', 1,0,True)
    # filter_view('test_second_id_view_trans.txt', 'test_second_id_view.txt',1,0,True)
    # seg_text('test_second_id_view.txt', 1, 0, True, 'test_seg.txt')

    # deal train second without segment
    # predeal_data('TrainSecond.csv', 'LabelSecond.csv', 'train_second_id_view_pol_t.txt', 0,1,False)
    # seg_text('train_second_id_view_pol_t.txt',0,1,False,'train_second_seg_t.txt')
    # trans_space('train_second_id_view_pol_t.txt', 'train_second_id_view_pol_trans_t.txt', 0,1,False)
    seg_text('train_second_id_view_pol_trans_t.txt', 0, 1, False, 'train_second_seg_t.txt')

    # deal train without segment
    # predeal_data('Train.csv', 'Label.csv', 'train_id_view_pol_t.txt', 0,0,False)
    # seg_text('train_id_view_pol_t.txt', 0,0,False, 'train_seg_t.txt')
    # trans_space('train_id_view_pol_t.txt', 'train_id_view_pol_trans_t.txt', 0,0,False)
    seg_text('train_id_view_pol_trans_t.txt', 0, 0, False, 'train_seg_t.txt')

    # deal train without segment
    # predeal_data('Test.csv', 'generate_view.txt', 'test_second_id_view_text_t.txt', 1,0,False)
    # seg_text('test_second_id_view_text_t.txt', 1,0,False, 'test_seg_t.txt')
    # trans_space('test_second_id_view_text_t.txt', 'test_second_id_view_trans_t.txt', 1,0,False)
    #filter_view('test_second_id_view_trans_t.txt', 'test_second_id_view_t.csv',1,0,False)
    seg_text('test_second_id_view_t.csv', 1, 0, False, 'test_seg_t.txt')




