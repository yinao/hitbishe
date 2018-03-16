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


def sax_ed_dist(a, b, w):
    distance = 0
    for i in range(len(a)):
        if abs(int(a[i]) - int(b[i])) <= 1:
            distance += 0
        else:
            distance += cutlines[w][max(a[i], b[i])-1] - cutlines[w][min(a[i], b[i])]
    return distance

data = numpy.loadtxt('cluster/trace', delimiter=',')
labels = data[:, 0]
data = data[:, 1:]
rows, cols = data.shape

for i in range(2, 15):
    win_size = i
    words = 7

    bit_data = list()
    # paa_data = list()
    sax_data = list()
    for d in data:
        tmp = list()
        bit_tmp = ''
        # paa_tmp = list()
        for i in range(0, len(d), win_size):
            low = i
            high = min(len(d), i + win_size)
            PAA = sum(d[low: high]) / (high - low)
            k = 0
            while k < words and PAA > cutlines[words][k]:
                k += 1
            tmp.append(k)
            for j in range(low, high):
                if d[j] < PAA:
                    bit_tmp += '0'
                else:
                    bit_tmp += '1'
        bit_data.append(int(bit_tmp,2))
        sax_data.append(tmp)
        # paa_data.append(paa_tmp)

    # paa_data = numpy.array(paa_data)

    k = 1

    raw_dist = numpy.zeros((rows, rows))
    pred = list()
    for i in range(rows):
        for j in range(i+1, rows):
            raw_dist[i, j] = sax_ed_dist(sax_data[i], sax_data[j], words)
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