#! usr/bin/python
# coding=utf-8
"""
File Name: Data Operation
Description:
Date: 2016-11-29
Author: QIU HU
"""
import matplotlib.pylab as plt
import jieba
jieba.load_userdict('../MidData/user.dict')


def tokenize_text(text):
    tokens = []
    for txt in text:
        tokens.extend(jieba.lcut(txt))
    return tokens

with open('train_id_view_pol_trans_all.txt') as f:
    LENS = []
    for line in f.readlines():
        lis = line.strip().split('\t')
        tokens = tokenize_text(lis[2:])
        LENS.append(len(tokens))
    plt.hist(LENS, bins=100)
    plt.show()

