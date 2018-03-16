# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy
from numpy import array, sum, sqrt
import time
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import scale
from bitarray import bitarray
from matplotlib import pyplot as plt

cutlines = dict()
cutlines[2] = [0, float('inf')]
cutlines[3] = [-0.43, 0.43, float('inf')]
cutlines[4] = [-0.67, 0, 0.67, float('inf')]
cutlines[5] = [-0.84, -0.25, 0.25, 0.84, float('inf')]
cutlines[6] = [-0.97, -0.43, 0, 0.43, 0.97, float('inf')]
cutlines[7] = [-1.07, -0.57, -0.18, 0.18, 0.57, 1.07, float('inf')]
cutlines[8] = [-1.15, -0.67, -0.32, 0, 0.32, 0.67, 1.15, float('inf')]
cutlines[9] = [-1.22, -0.76, -0.43, -0.14, 0.14, 0.43, 0.76, 1.22, float('inf')]
cutlines[10] = [-1.28, -0.84, -0.52, -0.25, 0, 0.25, 0.52, 0.84, 1.28, float('inf')]


data = numpy.loadtxt('dataSets/handoutlines', delimiter=',')
labels = data[:, 0]
data = data[:, 1:]

rows, cols = data.shape

for a in range(2, 10):
    for w in range(2, 10):
        words = a
        win_size = w

        symbol_data = list()
        bit_data = list()
        for d in data:
            tmp = list()
            d = scale(d)
            bit_tmp = list()
            for i in range(0, len(d), win_size):
                low = i
                high = min(len(d), i + win_size)
                b = bitarray()
                for j in range(low, high-1):
                    if d[j] < d[j+1]:
                        b.append(True)
                    else:
                        b.append(False)
                bit_tmp.append(b)
                PAA = sum(d[low: high]) / (high - low)
                for k in range(words):
                    if PAA < cutlines[words][k]:
                        break
                tmp.append(k)
            symbol_data.append(tmp)
            bit_data.append(bit_tmp)

        scores = list()
        for i in range(rows):
            min_dist = float('inf')
            for j in range(rows):
                if i == j:
                    continue
                # dist = (array(symbol_data[i]) - array(symbol_data[j]))**2
                dist = 0
                for k in range(len(symbol_data[i])):
                    dist += ((symbol_data[i][k] - symbol_data[j][k]) ** 2 + (bit_data[i][k] ^ bit_data[j][k]).count()*1.0 / (win_size-1))
                min_dist = min(min_dist, dist**0.5)
            scores.append(min_dist)

        auc = roc_auc_score(labels, scores)
        if auc < 0.5:
            auc = 1-auc

        print auc


