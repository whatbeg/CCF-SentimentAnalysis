#! usr/bin/python
# coding=utf-8
"""
File Name: Data Operation
Description:
Date: 2016-11-29
Author: QIU HU
"""

fout = open('user.dict', 'a')
with open('car_2_id.txt') as f:
    for line in f.readlines():
        lis = line.strip().split(',')
        if lis[0].count(' '):
            lis[0] = lis[0].replace(' ', '^')
        fout.write(lis[0] + ' 100 n\n')
fout.close()
