# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy
import time
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics import roc_auc_score

data = numpy.loadtxt('dataSets/ECG200/ecg200')
labels = data[:, 0]
data = data[:, 1:]
# data = data[100:150]

# data = numpy.loadtxt('dataSets/egg13.txt')
# labels = numpy.loadtxt('dataSets/label13.txt', dtype='int')
# data = data[100:150]
# labels = labels[100:150]

data = numpy.loadtxt('dataSets/gun1', delimiter=',')
labels = data[:, 0]
data = data[:, 1:]

begin = time.clock()

# dists = euclidean_distances(data).tolist()
#
# min_dist = list()
# for i in range(len(dists)):
#     tmp = dists[i][0:i] + dists[i][i+1:]
#     min_dist.append(min(tmp))

min_dist = list()
for i in range(len(data)):
    p = data[i]
    tmp = float('inf')
    for j in range(len(data)):
        if i == j:
            continue
        q = data[j]
        # dist = numpy.sqrt(numpy.sum((p - q)**2))
        dist = 0
        for k in range(len(p)):
            dist += (p[k] - q[k])**2
        tmp = min(dist, tmp)
    min_dist.append(tmp)

print 'time cost : %f' %(time.clock() - begin)

auc = roc_auc_score(labels, min_dist)
if auc < 0.5:
    print 1-auc
else:
    print auc