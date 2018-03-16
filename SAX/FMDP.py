# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy
import time
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import scale
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


data = numpy.loadtxt('dataSets/Lighting2', delimiter=',')
labels = data[:, 0]
data = data[:, 1:]

words = 3
win_size = 4
sub_len = 1


begin = time.clock()

symbol_data = list()
for d in data:
    tmp = list()
    d = scale(d)
    for i in range(0, len(d), win_size):
        low = i
        high = min(len(d), i + win_size)
        PAA = sum(d[low: high]) / (high - low)
        # PAA = sum(d[i:i+win_size]) / win_size
        for k in range(words):
            if PAA < cutlines[words][k]:
                break
        tmp.append(str(k+1))
    sub_dict = dict()
    for t in range(0, len(tmp), sub_len):
        s = ''.join(tmp[t:t+sub_len])
        sub_dict[s] = sub_dict.get(s, 0) + 1

    symbol_data.append(sub_dict)

# 正则化每个子模式的次数
for i in range(len(symbol_data)):
    max_c = max(symbol_data[i].values())
    for k in symbol_data[i].keys():
        symbol_data[i][k] = 1.0*symbol_data[i][k] / max_c

scores = list()
for i in range(len(symbol_data)):
    min_dist = float('inf')
    for j in range(len(symbol_data)):
        if i == j:
            continue
        dist = 0
        a_keys = symbol_data[i].keys()
        b_keys = symbol_data[j].keys()
        keys = list(set(a_keys).union(set(b_keys)))
        for k in keys:
            dist += (symbol_data[i].get(k, 0) - symbol_data[j].get(k, 0))**2
        dist **= 0.5
        min_dist = min(dist, min_dist)
    scores.append(min_dist)

auc = roc_auc_score(labels, scores)

if auc < 0.5:
    auc = 1-auc

print auc