# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy
import operator
from numpy import array, sum, sqrt
import time
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score
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


def sax_ed_dist(a, b, t_a, t_b, w):
    distance = 0
    for i in range(len(a)):
        if abs(int(a[i]) - int(b[i])) <= 1:
            distance += 0
        else:
            distance += cutlines[w][max(a[i], b[i])-1] - cutlines[w][min(a[i], b[i])]
        # print t_a[i]
        distance += 1.0/win_size * ((t_a[i][0]-t_b[i][0])**2 + (t_a[i][1]-t_b[i][1])**2)**0.5
    return (distance*win_size)

data = numpy.loadtxt('cluster/trace', delimiter=',')
labels = data[:, 0]
data = data[:, 1:]

rows, cols = data.shape
# print rows, cols
for a in range(2, 15):
    for w in range(2, 15):
        words = a
        win_size = w

        symbol_data = list()
        trend_data = list()
        bit_data = list()
        for d in data:
            tmp = list()
            d = scale(d)
            bit_tmp = ''
            t_tmp = list()
            for i in range(0, len(d), win_size):
                low = i
                high = min(len(d), i + win_size)
                PAA = sum(d[low: high]) / (high - low)
                for j in range(low, high):
                    if d[j] < PAA:
                        bit_tmp += '0'
                    else:
                        bit_tmp += '1'
                k = 0
                while k < words and PAA > cutlines[words][k]:
                    k += 1
                tmp.append(k)
                t_tmp.append((d[low] - PAA,d[high-1] - PAA))
            symbol_data.append(tmp)
            trend_data.append(t_tmp)
            bit_data.append(int(bit_tmp, 2))

        s_cols = len(symbol_data[0])

        k = 1
        dist = numpy.zeros((rows, rows))
        pred = list()
        for i in range(rows):
            for j in range(i+1, rows):
                if i == j:
                    continue
                tmp = sax_ed_dist(symbol_data[i], symbol_data[j], trend_data[i], trend_data[j], words)
                c = bit_data[i] ^ bit_data[j]
                ones = 0
                while c:
                    ones += 1
                    c &= (c - 1)
                tmp += ones * 1.0 / win_size
                tmp **= 0.5
                # tmp = win_size
                dist[i, j] = tmp
                dist[j, i] = tmp

            arg_index = numpy.argsort(dist[i])
            tmp = dict()
            if i in arg_index[:k]:
                for l in arg_index[:k + 1]:
                    if l == i:
                        continue
                    tmp[labels[l]] = tmp.get(labels[l], 0) + 1
            else:
                for l in arg_index[:k]:
                    tmp[labels[l]] = tmp.get(labels[l], 0) + 1

            pre = sorted(tmp.items(), key=operator.itemgetter(1), reverse=True)[0][0]
            pred.append(pre)

        for i in range(rows):
            if labels[i] != 1:
                labels[i] = 0

            if pred[i] != 1.0:
                pred[i] = 0

        print 'Precision: %f, Recall: %f, F1: %f' % \
            (precision_score(labels, pred, average='macro'),
             recall_score(labels, pred, average='macro'),
             f1_score(labels, pred, average='macro'))
