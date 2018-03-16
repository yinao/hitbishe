# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy
import random
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA

data_set = numpy.loadtxt('../dataSets/epileptic', delimiter=',')
labels = data_set[:, -1]
data_set = data_set[:,:-1]

# data_set = scale(data_set)

rows, cols = data_set. shape

# 使用散点图查看两个属性值的分布对异常属性的影响

attr = random.sample(range(cols), 2)

n_x, n_y = list(), list()
a_x, a_y = list(), list()

for i in range(rows):
    if labels[i] == 1:
        n_x.append(data_set[i, attr[0]])
        n_y.append(data_set[i, attr[1]])
    else:
        a_x.append(data_set[i, attr[0]])
        a_y.append(data_set[i, attr[1]])


plt.figure(1)

ax = plt.subplot()

plt.scatter(n_x, n_y, label='true', marker='*')
plt.scatter(a_x, a_y, label='false')

plt.legend(loc='upper right')

plt.show()
