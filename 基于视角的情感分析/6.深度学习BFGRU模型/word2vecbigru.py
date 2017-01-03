#! usr/bin/python
# coding=utf-8

from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.data_utils import to_categorical
import DataOperation as do
import datetime
import time
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def add(filename):     # 将无视角的一些句子ID加入最终提交结果中
    IDS = {}
    with open('CoreData/TestSecond.csv') as f:
        for line in f.readlines():
            sid = line.strip().split('\t')[0]
            IDS[sid] = 0
    PUTED = {}
    with open(filename) as f:
        for line in f.readlines():
            sid = line.strip().split(',')[0]
            PUTED[sid] = 0
    thisfilename = filename.split('.')[0] + "x.csv"
    with open(thisfilename, 'w') as f:
        LINES = list(open(filename, 'r').readlines())
        for line in LINES:
            if line.count('^'):
                line = line.replace('^', ' ')
            triple = line.split(',')[:3]
            if len(triple) == 3:
                ID = triple[0]
                view = triple[1]
                ret_view = filter_view(ID, view)
                if isinstance(ret_view, list):
                    for rv in ret_view:
                        if len(rv) > 0:
                            triple[1] = rv
                            f.write(','.join(triple))
                else:
                    if len(ret_view) > 0:
                        triple[1] = ret_view
                        f.write(','.join(triple))
        for ids in IDS:
            if ids not in PUTED:
                f.write(ids + ',,' + '\n')


def filter_view(ID, view):    # 筛选视角
    if len(view) == 0:
        return ""

    if len(view) >= 2 and view[:2] == '经典':
        view = view[2:]

    if view == '新捷达':
        return '捷达'

    if view == '新途观':
        return '途观'

    if view == '新胜达':
        return '胜达'

    if view == '新帝豪':
        return '帝豪'

    if view.count('新') and not view.count('新能源'):
        vs = view.split('新')
        return vs

    return view


def post_handle(filename='Result/result_2016121021_x.csv'):   # 后处理，将一个句子中一个视角的多种情绪总结一下
    dic = {}
    outf = filename.split('.')[0] + "x.csv"
    fout = open(outf, 'w')
    fout.write("SentenceId,View,Opinion\n")
    with open(filename) as f:
        for line in f.readlines()[1:]:
            lis = line.strip().split(',')
            if lis[1] == "" and lis[2] == "":
                fout.write(line.strip() + '\n')
                continue
            if lis[0]+','+lis[1].decode('utf8') not in dic:
                dic[lis[0]+','+lis[1].decode('utf8')] = [lis[2], ]
            elif lis[0]+','+lis[1].decode('utf8') in dic:
                haha = dic[lis[0]+','+lis[1].decode('utf8')]
                dic[lis[0]+','+lis[1].decode('utf8')] = haha + [lis[2], ]

    for key in dic.keys():
        lis = dic[key]
        if len(lis) == 1:
            fout.write(key + ',' + lis[0] + '\n')
        elif len(lis) == 2:
            fout.write(key + ',' + lis[1] + '\n')
        else:
            pos = neu = neg = 0
            for k in lis:
                if k == 'pos':
                    pos += 1
                elif k == 'neu':
                    neu += 1
                else:
                    neg += 1
            if pos >= neg and pos >= neu:
                fout.write(key + ',pos\n')
            elif neg >= neu and neg >= pos:
                fout.write(key + ',neg\n')
            else:
                fout.write(key + ',neu\n')
    fout.close()
    return outf


def vote_by_score(filename):   # 根据最后总的分数决定最终情绪
    dic = {}
    outf = filename.split('.')[0] + "x.csv"
    fout = open(outf, 'w')
    fout.write("SentenceId,View,Opinion\n")
    with open(filename) as f:
        for line in f.readlines()[1:]:
            lis = line.strip().split(',')
            if lis[0]+','+lis[1].decode('utf8') not in dic:
                dic[lis[0]+','+lis[1].decode('utf8')] = np.array(map(float, lis[3:]))
            elif lis[0]+','+lis[1].decode('utf8') in dic:
                haha = dic[lis[0]+','+lis[1].decode('utf8')]
                dic[lis[0]+','+lis[1].decode('utf8')] = haha + np.array(map(float, lis[3:]))
    idx2cla = {0: 'neu', 1: 'pos', 2: 'neg'}
    for key in dic.keys():
        lis = dic[key]
        idx = np.argmax(lis)
        fout.write(key + ',' + idx2cla[idx])
        # neu, pos, neg = lis[:]
        # if (neu > neg and pos > neg and abs(neu - pos) <= 0.1) \
        #         or (neu > pos and neg > pos and abs(neu - neg) <= 0.1) \
        #         or (pos > neu and neg > neu and abs(pos - neg) <= 0.1):
        #     # fout.write(",AB[{}, {}, {}]".format(neu, pos, neg))
        #     pass
        fout.write('\n')
    fout.close()
    return outf


def train(maxlen=100, embedding_dim=128):   # 主训练/测试代码
    start = time.time()
    l_trainX, r_trainX, ret_labels, l_topredictX, r_topredictX = do.load_data_bi_word2vec(maxlen=maxlen,
                                                                                          words_keep=50000,
                                                                                          validation_portion=0.,
                                                                                          embedding_dim=embedding_dim,
                                                                                          ma="A")
    trainY = to_categorical(ret_labels, nb_classes=3)
    del ret_labels
    lnet = tflearn.input_data([None, maxlen, embedding_dim])
    rnet = tflearn.input_data([None, maxlen, embedding_dim])
    lnet = tflearn.gru(lnet, embedding_dim, dropout=0.8, return_seq=False, dynamic=True)
    rnet = tflearn.gru(rnet, embedding_dim, dropout=0.8, return_seq=False, dynamic=True)
    net = tflearn.layers.merge_outputs([lnet, rnet])
    net = tflearn.fully_connected(net, 3, activation='softmax')
    net = tflearn.regression(net, optimizer='adam', learning_rate=0.001,
                             loss='categorical_crossentropy')
    # Training
    model = tflearn.DNN(net, tensorboard_verbose=0)
    model.fit([l_trainX, r_trainX], trainY, validation_set=0.1, show_metric=True,
              batch_size=32)
    model.save('MODELS/E_W2V_GRU_TC{}_{}.dy'.format(embedding_dim, maxlen))
    # model.load('MODELS/E_W2V_GRU_TC{}_{}.dy'.format(embedding_dim, maxlen))
    del l_trainX
    del r_trainX
    del trainY
    idx2cla = {0: 'neu', 1: 'pos', 2: 'neg'}
    filename = "Result/result_{}.csv".format(datetime.datetime.now().strftime("%Y%m%d%H%M"))
    prefix = list(open('Result/A_AFTER_NRP_200', 'r').readlines())
    f = open(filename, 'w')
    f.write('SentenceId,View,Opinion\n')
    a = [0,     5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000]
    b = [5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 65000]
    ANS = []
    for i in range(12):
        ans = model.predict([l_topredictX[a[i]:b[i]], r_topredictX[a[i]:b[i]]])
        ANS.extend([s for s in ans])
        print("ANS.LENGTH: {}".format(len(ans)))
    for i, r in enumerate(ANS):
        f.write(prefix[i].strip())
        idx = int(np.argmax(r))
        f.write(idx2cla[idx])
        k = ""
        for l in r:
            k += ',{:.4f}'.format(l)
        f.write(k)
        f.write('\n')
    f.close()
    end = time.time()
    print("TIME COST: {}".format(end-start))
    outf = vote_by_score(filename)
    add(outf)

train(100, 128)    # 左右各100长度，词嵌入128维

