#! usr/bin/python
# coding=utf-8
"""
File Name: Pre processing
Description:
Date: 2016-10-10
Author: QIU HU
"""

import jieba
import gensim
import numpy as np
from numpy import *
import jieba.posseg as pseg
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def pl(lis):
    """
    打印列表
    :param lis: list need to be print
    :return: None
    """
    for li in lis:
        print(li)


def extract_views(views, sentence):    # 抽取视角
    views_index = set()
    views_name = set()
    i = 0
    for word in sentence:
        if word in views:
            views_index.add(i)
            views_name.add(word)
        i += 1
    return views_index, views_name


def sentence_keep_key(sentence, keep_lis):    # 保持句子中的某些词，去掉其他
    cuted = []
    for word in sentence:
        if word in keep_lis:
            cuted.append(word)
    return cuted


def find_view_unfinded(sentence, views):     # 找出分词分开了的视角，将部分合并成该视角
    new_sen = []
    i = 0
    while i < len(sentence)-1:
        if i < len(sentence)-3 and sentence[i] + sentence[i+1] + sentence[i+2] + sentence[i+3] in views:
            new_sen.append(sentence[i] + sentence[i+1] + sentence[i+2] + sentence[i+3])
            i += 3
        elif i < len(sentence)-2 and sentence[i] + sentence[i+1] + sentence[i+2] in views:
            new_sen.append(sentence[i] + sentence[i+1] + sentence[i+2])
            i += 2
        elif sentence[i] + sentence[i+1] in views:
            new_sen.append(sentence[i]+sentence[i+1])
            i += 1
        elif sentence[i] + " " + sentence[i+1] in views:
            new_sen.append(sentence[i] + " " + sentence[i+1])
            # print("FIND WSP")
            i += 1
        elif sentence[i] + sentence[i+1] in ['2008年', '2008款']:
            new_sen.append(sentence[i] + sentence[i + 1])
            i += 1
        else:
            new_sen.append(sentence[i])
        i += 1
    if i == len(sentence) - 1:
        new_sen.append(sentence[i])
    return new_sen


def get_views(viewfile='MidData/user.dict'):    # 从视角字典中导入视角

    views = []
    with open(viewfile) as f:
        for line in f.readlines():
            lis = line.strip().split('\t')
            view = lis[0].decode('utf8')
            views.append(view)
    return views


def drop_stopwords(sentence, stopfile='MidData/stopwords'):   # 去停用词
    stopwords = []
    with open(stopfile) as f:
        stopwords = [line.strip() for line in f]
    stopwords.append(' ')
    stopwords.append('\n')
    droped = []
    for word in sentence:
        if word not in stopwords:
            droped.append(word)
    return droped


def get_RES_PRE():         # 从整理的test集中顺序得到结果集的前缀，如 "030002,奥迪A6,"

    fout = open('Result/NEW_RES_PRE', 'w')
    with open('CoreData/test_second_id_view_trans_12.9.txt') as f:
        for line in f.readlines():
            lis = line.strip().split('\t')
            fout.write(lis[0] + ',' + lis[1] + ',\n')
    fout.close()


def drop_30etal():      # 去除30, 3.0, 世纪 等视角， 拆分 全新, 经典 等视角

    fout = open('Result/result_2016120921_xx.csv', 'w')
    with open('Result/result_2016120921_x.csv') as f:
        for line in f.readlines():
            if line.count(',30,') or line.count(',3.0,') or line.count(',世纪,'):
                continue
            tag = 0
            for SP in ['全新', '经典']:
                if line.count(SP):
                    lis = line.strip().split(',')
                    views = lis[1].split(SP)
                    fout.write(lis[0] + ',' + views[0] + ',' + lis[2] + '\n')
                    fout.write(lis[0] + ',' + views[1] + ',' + lis[2] + '\n')
                    tag = 1
            if not tag:
                fout.write(line)
    fout.close()


def select_ambitious():              # 选择有歧义视角的句子
    fout = open('CoreData/test_ambitious.txt', 'w')
    results = list(open('Result/result_2016121011_x.csv').readlines()[1:])
    final_sentiment = [x.strip().split(',')[2] for x in results]
    with open('CoreData/test_second_id_view_trans_12.9.txt') as f:
        i = 0
        for line in f.readlines():
            lis = line.strip().split('\t')
            view = lis[1]
            sen = " ".join(lis[2:])
            if sen.count(view) > 1:
                fout.write(final_sentiment[i] + "\t" + line.strip() + '\n')
            i += 1
    fout.close()


def rectify_test_second_id_view(filename='CoreData/test_second_id_view_trans.txt'):    # 纠正一些视角问题
    fout = open('CoreData/test_second_id_view_rectified12.9.txt', 'w')
    with open(filename) as f:
        for line in f.readlines():
            lis = line.strip().split('\t')
            view = lis[1]
            sen = "".join(lis[2:])
            if view in ['征服', 'ceo', '地球梦', '超越', "赛马", '无限', '风光']:
                continue
            if view == '大陆' and not sen.count('林肯'):
                continue
            if view == '前途' and (sen.count('有前途') or sen.count('前途无量') or sen.count('前途暗淡')):
                continue
            if view == '新科' and sen.count('新科技'):
                continue
            if view == '新凯' and sen.count('新凯越'):
                view = '凯越'
            if view == '新凯' and sen.count('新凯尊'):
                view = '凯尊'
            lis[1] = view
            fout.write('\t'.join(lis) + '\n')
    fout.close()


def trans_added_data():    # 对爬取数据做一些变换
    fout = open('train_added.txt', 'w')
    tofind = ['【最满意的一点】', '【最不满意的一点】', '【空间】', '【动力】', '【操控】', '【油耗】']
    with open('plus_train.txt') as f:
        for line in f.readlines():
            line = line.strip()
            start = 0
            i = 0
            while True:
                if i >= len(tofind):
                    break
                idx = line.find(tofind[i], start)
                if idx == -1:
                    i += 1
                    if i >= len(tofind):
                        break
                    continue
                if len(line[start:idx]) > 0:
                    fout.write(line[start:idx])
                    fout.write('\n')
                start = idx + len(tofind[i])
                i += 1

    fout.close()


def extract_for_train_added():      # 对爬取数据再做转换
    VIEWS = []
    with open('MidData/user.dict') as f:
        for line in f.readlines():
            view = line.strip().split(' ')[0]
            VIEWS.append(view)
    fout = open('train_plusplus.txt', 'w')
    num = 100020
    with open('train_added.txt') as f:
        for line in f.readlines():
            tag = 0
            for v in VIEWS:
                if line.count(v):
                    fout.write('{}\t{}\t{}\t{}'.format(num, v, 'neu', line))
                    tag = 1
            if not tag:
                fout.write('{}\t{}\t{}\t{}'.format(num, '视角', 'neu', line))
            num += 1
    fout.close()

if __name__ == '__main__':

    # get_RES_PRE()
    # drop_30etal()
    # tran_answer_to_RES_PRE()
    # select_ambitious()
    # rectify_test_second_id_view('CoreData/test_second_id_view_trans_12.9.txt')
    # trans_added_data()
    extract_for_train_added()
