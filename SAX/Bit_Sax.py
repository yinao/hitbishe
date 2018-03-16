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

data = numpy.loadtxt('dataSets/wafer', delimiter=',')
labels = data[:, 0]
data = data[:, 1:]

rows, cols = data.shape
for i in range(rows):
    data[i] = scale(data[i])

print cols
words = 5
win_size = 7

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
        b = bitarray()
        for j in range(low, high-1):
            if d[j] < d[j+1]:
                b.append(True)
            else:
                b.append(False)
        bit_tmp.append(b)
        PAA = sum(d[low: high]) / (high - low)
        paa_tmp.append(PAA)
        k = 0
        for k in range(words):
            if PAA < cutlines[words][k]:
                break
        tmp.append(str(k+1))
    symbol_data.append(tmp)
    bit_data.append(bit_tmp)
    paa_data.append(paa_tmp)

s_index = random.randint(0, rows-2)

raw_dist = list()
p_dist = list()
hot_dist = list()
bit_dist = list()

sample_index_list = random.sample(range(0, rows), min(rows/3, 40))

for i in sample_index_list:
    if i == s_index:
        continue
    tmp = 0
    for k in range(cols):
        tmp += (data[i][k] - data[s_index][k])**2
    raw_dist.append(tmp**0.5)
    b_dist = sax_dist(symbol_data[i], symbol_data[s_index], words, win_size)
    hot_dist.append(b_dist)
    b_dist = bit_sax_dist(symbol_data[i], symbol_data[s_index], bit_data[i], bit_data[s_index], words, win_size)
    bit_dist.append(b_dist)
    p_dist.append(paa_dist(paa_data[i], paa_data[s_index], win_size))


plt.figure(1)
plt.xticks(range(0, len(raw_dist), 1))
plt.plot(range(len(raw_dist)), raw_dist, marker='.', c='b', label='raw dist')
plt.plot(range(len(hot_dist)), hot_dist, marker='*', c='g', label='hot sax')
plt.plot(range(len(p_dist)), p_dist, marker='v', c='y', label='paa')
# plt.plot(range(len(bit_dist)), bit_dist, marker='v', c='r', label='bit sax')
plt.legend(loc='upper right')
plt.grid(True, linestyle = "-.", color = "#3d3d3d", linewidth = ".1")
plt.show()
