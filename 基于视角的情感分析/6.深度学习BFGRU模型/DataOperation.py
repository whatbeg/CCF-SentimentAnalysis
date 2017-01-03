#! usr/bin/python
# coding=utf-8
"""
File Name: Data Operation
Description:
Date: 2016-11-29
Author: QIU HU
"""
import collections
import numpy as np
import gensim


def get_train_all_views():   # TC模式会用到
    train_views = []
    with open('CoreData/train_id_view_pol_trans.txt') as f:
        for line in f.readlines():
            lis = line.strip().split('\t')
            train_views.append(lis[1])
    return train_views


# 务必先生成AFTER_NRP
def get_test_all_views():    # TC模式会用到
    test_views = []
    with open('Result/AFTER_NRP') as f:
        for line in f.readlines():
            lis = line.strip().split(',')
            test_views.append(lis[1])
    return test_views


def get_vocab_bi(word_keep, ma):   # 读取文件到矩阵中
    WORDS = collections.defaultdict(int)
    l_trainX = list(open('CoreData/{}_LEFT_COMMENT200.all'.format(ma), 'r').readlines())
    r_trainX = list(open('CoreData/{}_RIGHT_COMMENT200.all'.format(ma), 'r').readlines())
    l_trainX = [x.strip().split('\t') for x in l_trainX]
    r_trainX = [x.strip().split('\t') for x in r_trainX]
    for sen in l_trainX:
        for w in sen:
            w = w.decode('utf8')
            if len(w) > 0:
                WORDS[w] += 1
    for sen in r_trainX:
        for w in sen:
            w = w.decode('utf8')
            if len(w) > 0:
                WORDS[w] += 1
    testL = list(open('CoreData/{}_LEFT_COMMENT200.test'.format(ma), 'r').readlines())
    testL = [x.strip().split('\t') for x in testL]
    testR = list(open('CoreData/{}_RIGHT_COMMENT200.test'.format(ma), 'r').readlines())
    testR = [x.strip().split('\t') for x in testR]
    for sen in testL:
        for w in sen:
            w = w.decode('utf8')
            if len(w) > 0:
                WORDS[w] += 1
    for sen in testR:
        for w in sen:
            w = w.decode('utf8')
            if len(w) > 0:
                WORDS[w] += 1
    sorted_word = sorted(WORDS.iteritems(), key=lambda x: x[1], reverse=True)
    NEW_WORDS = {}
    i = 1
    for tu in sorted_word[:min(word_keep, len(sorted_word))]:
        NEW_WORDS[tu[0]] = i
        if i == min(word_keep, len(sorted_word)):
            NEW_WORDS[tu[0]] = 0
        i += 1

    labels = list(open('CoreData/{}_COMMENT200.lbl'.format(ma), 'r').readlines())
    labels = [x.strip() for x in labels]
    if labels[0].count("\xef\xbb\xbf"):
        labels[0] = labels[0].replace("\xef\xbb\xbf", "")
    print(labels[0])
    return NEW_WORDS, np.array(l_trainX), np.array(r_trainX), labels, np.array(testL), np.array(testR)


def pad_sequence(vec, maxlen, embedding_dim):   # 规整到固定长度maxlen，不够的不全，超过的截取
    for i, subvec in enumerate(vec):
        zero = np.zeros(embedding_dim)
        if len(subvec) > maxlen:
            vec[i] = vec[i][:maxlen]
        else:
            less = maxlen - len(subvec)
            vec[i].extend([zero for _ in range(less)])
    return vec


def load_data_bi_word2vec(maxlen, words_keep, validation_portion, embedding_dim, ma):  # TD模式的数据加载，将词替换为词向量，也是实际使用的
    model = gensim.models.Word2Vec.load_word2vec_format('Word2VecModel/vectors{}.bin'.format(embedding_dim), binary=True)
    WORDS, l_trainset, r_trainset, labels, l_testset, r_testset = get_vocab_bi(words_keep, ma)
    Lbl2num = {'neu': 0, 'pos': 1, 'neg': -1}
    labels = [Lbl2num[x] for x in labels]
    ones = np.ones(embedding_dim)
    l_trainX = [map(lambda x: model[x] if x in model else ones, map(lambda x: x.decode('utf8'), sen)) for sen in l_trainset]
    l_testX = [map(lambda x: model[x] if x in model else ones, map(lambda x: x.decode('utf8'), sen)) for sen in l_testset]
    r_trainX = [map(lambda x: model[x] if x in model else ones, map(lambda x: x.decode('utf8'), sen)) for sen in r_trainset]
    r_testX = [map(lambda x: model[x] if x in model else ones, map(lambda x: x.decode('utf8'), sen)) for sen in r_testset]
    l_trainX = pad_sequence(l_trainX, maxlen, embedding_dim)
    l_testX = pad_sequence(l_testX, maxlen, embedding_dim)
    r_trainX = pad_sequence(r_trainX, maxlen, embedding_dim)
    r_testX = pad_sequence(r_testX, maxlen, embedding_dim)
    print(len(l_trainX), len(l_trainX[1]))
    total = len(l_trainX)
    random_idx = np.random.permutation(total)
    n_train = int(total * (1 - validation_portion))
    print("Train / Dev: {} / {}".format(n_train, total-n_train))
    ret_L_trainX = [l_trainX[idx] for idx in random_idx[:n_train]]
    ret_R_trainX = [r_trainX[idx] for idx in random_idx[:n_train]]
    ret_labels = [labels[idx] for idx in random_idx[:n_train]]
    return ret_L_trainX, ret_R_trainX, ret_labels, l_testX, r_testX


def load_data_bi_word2vec_TC(maxlen, words_keep, validation_portion):   # TC模式的数据加载
    model = gensim.models.Word2Vec.load_word2vec_format('Word2VecModel/vectors128.bin', binary=True)
    WORDS, l_trainset, r_trainset, labels, l_testset, r_testset = get_vocab_bi(words_keep, 'A')
    train_views = get_train_all_views()
    test_views = get_test_all_views()
    ones = np.ones(128)
    train_views_w2v = [model[x] if x in model else ones for x in train_views]
    test_views_w2v = [model[x] if x in model else ones for x in test_views]
    Lbl2num = {'neu': 0, 'pos': 1, 'neg': -1}
    labels = [Lbl2num[x] for x in labels]
    l_trainX = [
        map(lambda x: np.append(model[x], train_views_w2v[i]) if x in model else np.append(ones, train_views_w2v[i]),
            map(lambda x: x.decode('utf8'), sen)) for i, sen in enumerate(l_trainset)]
    l_testX = [
        map(lambda x: np.append(model[x], test_views_w2v[i]) if x in model else np.append(ones, test_views_w2v[i]),
            map(lambda x: x.decode('utf8'), sen)) for i, sen in enumerate(l_testset)]
    r_trainX = [
        map(lambda x: np.append(model[x], train_views_w2v[i]) if x in model else np.append(ones, train_views_w2v[i]),
            map(lambda x: x.decode('utf8'), sen)) for i, sen in enumerate(r_trainset)]
    r_testX = [
        map(lambda x: np.append(model[x], test_views_w2v[i]) if x in model else np.append(ones, test_views_w2v[i]),
            map(lambda x: x.decode('utf8'), sen)) for i, sen in enumerate(r_testset)]
    l_trainX = pad_sequence(l_trainX, maxlen, 128)
    l_testX = pad_sequence(l_testX, maxlen, 128)
    r_trainX = pad_sequence(r_trainX, maxlen, 128)
    r_testX = pad_sequence(r_testX, maxlen, 128)
    print(len(l_trainX), len(l_trainX[1]))
    total = len(l_trainX)
    random_idx = np.random.permutation(total)
    n_train = int(total * (1 - validation_portion))
    print("Train / Dev: {} / {}".format(n_train, total-n_train))
    ret_L_trainX = [l_trainX[idx] for idx in random_idx[:n_train]]
    ret_R_trainX = [r_trainX[idx] for idx in random_idx[:n_train]]
    ret_labels = [labels[idx] for idx in random_idx[:n_train]]
    return ret_L_trainX, ret_R_trainX, ret_labels, l_testX, r_testX

if __name__ == '__main__':
    pass
