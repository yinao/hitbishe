import os
import sys
import numpy
import operator
import random
from numpy import array, sum, sqrt
import time
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_predict
from sklearn.preprocessing import scale, StandardScaler
from bitarray import bitarray
from matplotlib import pyplot as plt


data = numpy.loadtxt('cluster/faceall', delimiter=',')
labels = data[:, 0]
data = data[:, 1:]
rows, cols = data.shape

for i in range(2, 15):
    win_size = i
    k = 3

    bit_data = list()
    paa_data = list()
    for d in data:
        tmp = list()
        bit_tmp = ''
        paa_tmp = list()
        for i in range(0, len(d), win_size):
            low = i
            high = min(len(d), i + win_size)
            PAA = sum(d[low: high]) / (high - low)
            paa_tmp.append(PAA)
            for j in range(low, high):
                if d[j] < PAA:
                    bit_tmp += '0'
                else:
                    bit_tmp += '1'
        bit_data.append(int(bit_tmp,2))
        paa_data.append(paa_tmp)

    paa_data = numpy.array(paa_data)

    raw_dist = numpy.zeros((rows, rows))
    pred = list()
    for i in range(rows):
        for j in range(i+1, rows):
            # raw_dist[i, j] = numpy.linalg.norm(paa_data[i] - paa_data[j]) * (win_size**0.5)
            raw_dist[i, j] = numpy.sum(numpy.square(paa_data[i] - paa_data[j]))
            c = bit_data[i] ^ bit_data[j]
            ones = 0
            while c:
                ones += 1
                c &= (c-1)
            raw_dist[i, j] *= win_size
            raw_dist[i, j] += ones * 1.0 / win_size
            raw_dist[i, j] **= 0.5
            raw_dist[j, i] = raw_dist[i, j]

        arg_index = numpy.argsort(raw_dist[i])
        tmp = dict()
        if i in arg_index[:k]:
            for l in arg_index[:k+1]:
                if l == i:
                    continue
                tmp[labels[l]] = tmp.get(labels[l], 0) + 1
        else:
            for l in arg_index[:k]:
                tmp[labels[l]] = tmp.get(labels[l], 0) + 1

        pre = sorted(tmp.items(), key=operator.itemgetter(1), reverse=True)[0][0]
        pred.append(pre)

    print 'win_size: %d, Precision: %f, Recall: %f, F1: %f '% \
        (win_size, precision_score(labels, pred, average='macro'),
         recall_score(labels, pred, average='macro'),
         f1_score(labels, pred, average='macro'))