#! usr/bin/python
# coding=utf-8
"""
File Name: generate Comment.all / label / test
Description:
Date: 2016-12-06
Author: QIU HU
"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')

with open('Train_segmented.txt', 'a') as f:
    fin = open('for_word2vec3.txt')
    for line in fin.readlines():
        f.write(line.strip() + '\n')
    fin.close()

