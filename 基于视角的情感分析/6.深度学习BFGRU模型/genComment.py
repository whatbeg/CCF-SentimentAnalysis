#! usr/bin/python
# coding=utf-8
"""
File Name: generate Comment.all / label / test
Description:
Date: 2016-12-06
Author: QIU HU
"""
import Tools
import jieba
import copy
import time
from jieba import analyse
import sys
reload(sys)
sys.setdefaultencoding('utf8')
jieba.load_userdict('MidData/user.dict')


def tokenize_text(text):   # 分词
    tokens = []
    for txt in text:
        tokens.extend(jieba.lcut(txt))
    return tokens


def genTrainData_Multi(maxlen=200):   # 将原始训练集数据做分词等处理，对每个视角或同一个视角的不同出现位置，分出左右两部分

    LEFT_all = open('CoreData/A_LEFT_COMMENT{}.all'.format(maxlen), 'w')
    lbl = open('CoreData/A_COMMENT{}.lbl'.format(maxlen), 'w')
    RIGHT_all = open('CoreData/A_RIGHT_COMMENT{}.all'.format(maxlen), 'w')
    views = Tools.get_views('MidData/user.dict')
    with open('CoreData/train_id_view_pol_trans_all.txt', 'r') as f:
        for line in f.readlines():
            lis = line.strip().split('\t')
            ID = lis[0]
            VIEW = lis[1]
            POL = lis[2]
            sentence = "".join(lis[3:])
            viewlen = len(VIEW)
            cnt = 1
            start = 0
            for _ in range(cnt):
                ind = sentence.find(VIEW, start)
                start = ind + 1
                back = ind + viewlen
                LEFT = sentence[:ind]
                RIGHT = sentence[back:]
                # print("LEFT, RIGHT = {} / {}".format(LEFT, RIGHT))
                l_sentence = map(lambda x: x.decode('utf8'), tokenize_text([LEFT]))  # 分词
                l_sentence = Tools.drop_stopwords(l_sentence)  # 去除停用词
                l_sentence = Tools.find_view_unfinded(l_sentence, views)  # 找出分错词的汽车品牌，重新整合句子
                r_sentence = map(lambda x: x.decode('utf8'), tokenize_text([RIGHT]))  # 分词
                r_sentence = Tools.drop_stopwords(r_sentence)  # 去除停用词
                r_sentence = Tools.find_view_unfinded(r_sentence, views)  # 找出分错词的汽车品牌，重新整合句子
                # print("lsentence, rsentence = {} / {}".format(l_sentence, r_sentence))
                if len(r_sentence) >= maxlen:
                    tagwords = jieba.analyse.extract_tags(" ".join(r_sentence), topK=maxlen-3)
                    if VIEW not in tagwords:
                        tagwords.append(VIEW)
                    r_sentence = Tools.sentence_keep_key(r_sentence, tagwords)   # 保留关键词，使整个句子的长度小于等于 max_sentence_length
                if len(l_sentence) >= maxlen:
                    tagwords = jieba.analyse.extract_tags(" ".join(l_sentence), topK=maxlen-3)
                    if VIEW not in tagwords:
                        tagwords.append(VIEW)
                    l_sentence = Tools.sentence_keep_key(l_sentence, tagwords)   # 保留关键词，使整个句子的长度小于等于 max_sentence_length
                if len(l_sentence) == 0:
                    l_sentence = copy.deepcopy(r_sentence)
                elif len(r_sentence) == 0:
                    r_sentence = copy.deepcopy(l_sentence)
                LEFT_all.write("\t".join(l_sentence))
                LEFT_all.write('\n')
                r_sentence.reverse()
                RIGHT_all.write("\t".join(r_sentence))
                RIGHT_all.write('\n')
                lbl.write(POL)
                lbl.write('\n')
    LEFT_all.close()
    lbl.close()
    RIGHT_all.close()


def genTestData_Multi(maxlen=200):    # 将原始测试集数据做分词等处理，对每个视角或同一个视角的不同出现位置，分出左右两部分

    LEFT_all = open('CoreData/A_LEFT_COMMENT{}.test'.format(maxlen), 'w')
    RIGHT_all = open('CoreData/A_RIGHT_COMMENT{}.test'.format(maxlen), 'w')
    views = Tools.get_views('MidData/user.dict')
    after_new_res_pre = open('Result/A_AFTER_NRP_{}'.format(maxlen), 'w')
    # with open('CoreData/test_second_id_view_rectified12.9.txt', 'r') as f:
    with open('CoreData/test_second_id_view_all12.12.txt', 'r') as f:
        for line in f.readlines():
            lis = line.strip().split('\t')
            ID = lis[0]
            VIEW = lis[1]   # 就采用test_second_id_view里面的
            sentence = "".join(lis[2:])
            viewlen = len(VIEW)
            cnt = sentence.count(VIEW)
            start = 0
            for _ in range(cnt):
                ind = sentence.find(VIEW, start)
                start = ind + 1
                back = ind + viewlen
                LEFT = sentence[:ind]
                RIGHT = sentence[back:]
                # print("LEFT, RIGHT = {} / {}".format(LEFT, RIGHT))
                l_sentence = map(lambda x: x.decode('utf8'), tokenize_text([LEFT]))  # 分词
                l_sentence = Tools.drop_stopwords(l_sentence)  # 去除停用词
                l_sentence = Tools.find_view_unfinded(l_sentence, views)  # 找出分错词的汽车品牌，重新整合句子
                r_sentence = map(lambda x: x.decode('utf8'), tokenize_text([RIGHT]))  # 分词
                r_sentence = Tools.drop_stopwords(r_sentence)  # 去除停用词
                r_sentence = Tools.find_view_unfinded(r_sentence, views)  # 找出分错词的汽车品牌，重新整合句子
                # print("lsentence, rsentence = {} / {}".format(l_sentence, r_sentence))
                if len(r_sentence) >= maxlen:
                    tagwords = jieba.analyse.extract_tags(" ".join(r_sentence), topK=maxlen-3)
                    if VIEW not in tagwords:
                        tagwords.append(VIEW)
                    r_sentence = Tools.sentence_keep_key(r_sentence, tagwords)   # 保留关键词，使整个句子的长度小于等于 max_sentence_length
                if len(l_sentence) >= maxlen:
                    tagwords = jieba.analyse.extract_tags(" ".join(l_sentence), topK=maxlen-3)
                    if VIEW not in tagwords:
                        tagwords.append(VIEW)
                    l_sentence = Tools.sentence_keep_key(l_sentence, tagwords)   # 保留关键词，使整个句子的长度小于等于 max_sentence_length
                if len(l_sentence) == 0:
                    l_sentence = copy.deepcopy(r_sentence)
                elif len(r_sentence) == 0:
                    r_sentence = copy.deepcopy(l_sentence)
                LEFT_all.write("\t".join(l_sentence))
                LEFT_all.write('\n')
                r_sentence.reverse()
                RIGHT_all.write("\t".join(r_sentence))
                RIGHT_all.write('\n')
                after_new_res_pre.write(ID + ',' + VIEW + ',' + '\n')
    LEFT_all.close()
    RIGHT_all.close()
    after_new_res_pre.close()

start = time.time()
genTrainData_Multi(200)
print("Train Data Generated~")
genTestData_Multi(200)
end = time.time()
print("TIME COST: {}".format(end-start))

import matplotlib.pylab as plt


def calc_length():    # 计算评论的长度分布

    l_train = list(open('CoreData/LEFT_COMMENT200.all').readlines())
    ltrain = [len(sen.strip().split('\t')) for sen in l_train]
    plt.hist(ltrain, bins=100)

    r_train = list(open('CoreData/RIGHT_COMMENT200.all').readlines())
    rtrain = [len(sen.strip().split('\t')) for sen in r_train]
    plt.hist(rtrain, bins=100)

    l_test = list(open('CoreData/LEFT_COMMENT200.test').readlines())
    ltest = [len(sen.strip().split('\t')) for sen in l_test]
    # plt.hist(ltest, bins=100)

    r_test = list(open('CoreData/RIGHT_COMMENT200.test').readlines())
    rtest = [len(sen.strip().split('\t')) for sen in r_test]
    # plt.hist(rtest, bins=100)
    plt.show()


def get_Corpus_for_word2vec():   # 合并一些语料用来进行word2vec训练
    fout = open('for_word2vec3.txt', 'a')
    with open('comment.txt') as f:
        i = 0
        for line in f.readlines():
            i += 1
            tokens = tokenize_text([line.strip()])
            fout.write(" ".join(tokens))
            fout.write('\n')
            if i % 10000 == 0:
                print("Line {} ...".format(i))
    # with open('context2.txt') as f:
    #     for line in f.readlines():
    #         tokens = tokenize_text([line.strip()])
    #         fout.write(" ".join(tokens))
    #         fout.write('\n')
    # with open('context3.txt') as f:
    #     for line in f.readlines():
    #         tokens = tokenize_text([line.strip()])
    #         fout.write(" ".join(tokens))
    #         fout.write('\n')
    # with open('jindong_comment') as f:
    #     for line in f.readlines():
    #         fout.write(line.strip())
    #         fout.write('\n')
    # with open('old_comment200.all') as f:
    #     for line in f.readlines():
    #         tokens = line.strip().split('\t')
    #         fout.write(" ".join(tokens) + '\n')
    #
    # with open('old_comment200.test') as f:
    #     for line in f.readlines():
    #         tokens = line.strip().split('\t')
    #         fout.write(" ".join(tokens) + '\n')
    fout.close()


# get_Corpus_for_word2vec()

