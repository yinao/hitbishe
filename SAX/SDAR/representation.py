# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy
import random
from numpy import array, sum, sqrt
import time
from sklearn.metrics import roc_auc_score
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

gama = 0.05


def sax_dist(a, b, words, win_size):
    dist = 0
    for i, ch in enumerate(a):
        t_a = int(ch)
        t_b = int(b[i])
        if abs(int(t_a) - int(t_b)) <= 1:
            dist += 0
        else:
            dist += (cutlines[words][max(t_a, t_b)-1-1] - cutlines[words][min(t_a, t_b)-1])**2
    return (dist*win_size)**0.5


def bit_sax_dist(a, b, s_a, s_b, words, win_size):
    dist = 0
    for i, ch in enumerate(a):
        t_a = int(ch)
        t_b = int(b[i])
        if abs(int(t_a) - int(t_b)) <= 1:
            dist += (s_a[i]^s_b[i]).count()*1.0 * gama
        else:
            dist += cutlines[words][max(t_a, t_b) - 1 - 1] - cutlines[words][min(t_a, t_b) - 1]
    return dist


def paa_dist(a, b, win_size):
    dist = 0
    for i, d in enumerate(a):
        dist += (d-b[i])**2
    return (dist*win_size)**0.5

data = numpy.loadtxt('../dataSets/lighting2', delimiter=',')
labels = data[:, 0]
data = data[:, 1:]

rows, cols = data.shape
for i in range(rows):
    data[i] = scale(data[i])

words = 5
win_size = 12

symbol_data = list()
bit_data = list()
paa_data = list()
for d in data:
    tmp = list()
    bit_tmp = list()
    paa_tmp = list()
    for i in range(0, len(d), win_size):
        low = i
        high = min(len(d), i + win_size)
        # b = bitarray()
        # for j in range(low, high-1):
        #     if d[j] < d[j+1]:
        #         b.append(True)
        #     else:
        #         b.append(False)
        # bit_tmp.append(b)
        PAA = sum(d[low: high]) / (high - low)
        paa_tmp.append(PAA)
        b = bitarray()
        for j in range(low, high):
            if d[j] < PAA:
                b.append(False)
            else:
                b.append(True)
        bit_tmp.append(b)
        k = 0
        for k in range(words):
            if PAA < cutlines[words][k]:
                break
        tmp.append(str(k+1))
    symbol_data.append(tmp)
    bit_data.append(bit_tmp)
    paa_data.append(paa_tmp)

paa_data = numpy.array(paa_data)

raw_score = list()
sax_score = list()
bit_score = list()
paa_score = list()
for i in range(rows):
    raw_tmp = float('inf')
    sax_tmp = float('inf')
    bit_tmp = float('inf')
    paa_tmp = float('inf')
    for j in range(rows):
        if i == j:
            continue
        dist = numpy.linalg.norm(data[i] - data[j])
        raw_tmp = min(raw_tmp, dist)
        dist = numpy.linalg.norm(paa_data[i] - paa_data[j])
        paa_tmp = min(paa_tmp, dist)
        for k in range(len(bit_data[i])):
            dist += (bit_data[i][k] ^ bit_data[j][k]).count()*1.0 / win_size
        bit_tmp = min(bit_tmp, dist)
    raw_score.append(raw_tmp)
    paa_score.append(paa_tmp)
    bit_score.append(bit_tmp)


raw_auc = roc_auc_score(labels, raw_score)
paa_auc = roc_auc_score(labels, paa_score)
bit_auc = roc_auc_score(labels, bit_score)

print 'Raw AUC: %f' % raw_auc
print 'PAA AUC: %f' % paa_auc
print 'Bit AUC: %f' % bit_auc
