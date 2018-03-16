# !/usr/bin/env python
# -*-coding:utf-8-*-

import os
import sys
import numpy
import random
from numpy import array, sum, sqrt
import time
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import scale, StandardScaler
from bitarray import bitarray
from matplotlib import pyplot as plt
from LocalOutlierFactor import *

data = numpy.loadtxt('../dataSets/egg13.txt')
labels = numpy.loadtxt('../dataSets/label13.txt', dtype='int')
# data = data[100:150]
# labels = labels[100:150]

rows, cols = data.shape
for i in range(rows):
    data[i] = scale(data[i])

for i in range(1, 15):
    win_size = i
    bit_data = list()
    paa_data = list()
    for d in data:
        tmp = list()
        bit_tmp = list()
        paa_tmp = list()
        for i in range(0, len(d), win_size):
            low = i
            high = min(len(d), i + win_size)
            PAA = sum(d[low: high]) / (high - low)
            paa_tmp.append(PAA)
            b = bitarray()
            for j in range(low, high):
                if d[j] < PAA:
                    b.append(False)
                else:
                    b.append(True)
            bit_tmp.append(b)
        bit_data.append(bit_tmp)
        paa_data.append(paa_tmp)

    paa_data = numpy.array(paa_data)

    # 计算距离矩阵
    dist_matrix = numpy.zeros((rows, rows))
    for i in range(rows):
        for j in range(i+1, rows):
            dist = numpy.linalg.norm(paa_data[i] - paa_data[j]) * (win_size**0.5)
            for k in range(len(bit_data[i])):
                dist += (bit_data[i][k] ^ bit_data[j][k]).count()*1.0 / win_size
            dist_matrix[i, j] = dist
            dist_matrix[j, i] = dist

    # 表示方法用在LOF中
    d_nlist, d_n = find_kdist(dist_matrix)
    rd_matrix = reach_distance(d_nlist, dist_matrix)
    lr_vector = lr_density(d_n, rd_matrix)
    lof = lo_factor(d_n, lr_vector)

    auc = roc_auc_score(labels, lof)

    if auc < 0.5:
        auc = 1-auc

    print 'win-size=%d, auc=%f' % (win_size, auc)