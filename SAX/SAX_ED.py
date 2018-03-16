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


data = numpy.loadtxt('dataSets/ECG200/ecg200')
labels = data[:, 0]
data = data[:, 1:]

rows, cols = data.shape
words = 4
win_size = 7

symbol_data = list()
trend_data = list()
for d in data:
    tmp = list()
    d = scale(d)
    t_tmp = list()
    for i in range(0, len(d), win_size):
        low = i
        high = min(len(d), i + win_size)
        PAA = sum(d[low: high]) / (high - low)
        k = 0
        while k < words and PAA > cutlines[words][k]:
            k += 1
        tmp.append(k)
        t_tmp.append(d[low] - PAA)
        t_tmp.append(d[high-1] - PAA)
    symbol_data.append(tmp)
    trend_data.append(t_tmp)

print symbol_data[0]

