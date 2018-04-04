# !/usr/bin/env python
# -*-coding:utf-8-*-


import numpy as np
import math
from bitarray import bitarray
from matplotlib import pyplot as plt
from sklearn.metrics import roc_auc_score, hamming_loss
from sklearn.metrics.pairwise import pairwise_distances

path = '../../Forest/data_series/lighting2'
data = np.loadtxt(path)
label = data[:, 0]
data = data[:, 1:]
rows, cols = data.shape

s_cols = cols#np.random.randint(int(cols**0.25), int(cols**0.75))

k = 32
hash_family = np.zeros((k, s_cols))
for i in range(k):
    hash_family[i] = np.random.randn(s_cols)

# begin = np.random.randint(0, cols)
b_data = list()
for i in range(rows):
    tmp = list()
    for h in hash_family:
        res = math.cos(np.sum(h*data[i]) + np.random.uniform(0, math.pi*2))
        res += np.random.uniform(-1, 1)
        if res < 0:
            tmp.append('0')
        else:
            tmp.append('1')
    b_data.append(tmp)
print 'completed calculating hash map......'
top_k = 5
hm_dist = np.zeros((rows, rows))
result = list()
for i in range(rows):
    for j in range(i+1, rows):
        if i == j:
            continue
        hm_dist[i, j] = hamming_loss(b_data[i], b_data[j])
        hm_dist[j, i] = hm_dist[i, j]

    result.append(sum(sorted(np.concatenate((hm_dist[i, :i], hm_dist[i, i+1:]), axis=0))[:top_k])*1.0/top_k)

print roc_auc_score(label, result)

# n_b_d, a_b_d = list(), list()
# for i in range(rows):
#     if label[i] == 1.0:
#         n_b_d.append(i)
#     else:
#         a_b_d.append(i)
#
# plt.figure(1)
# plt.scatter(n_b_d, [hm_dist[i] for i in n_b_d])
# plt.scatter(a_b_d, [hm_dist[i] for i in a_b_d])
# plt.show()

