# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy
import random
from sklearn.preprocessing import scale, StandardScaler
import matplotlib.pyplot as plt

data_set = numpy.loadtxt('../dataSets/hapt57', delimiter=',')
labels = data_set[:, -1]
data_set = data_set[:,:-1]

rows, cols = data_set.shape


# 使用统计图检查每个属性值的分布
# attr = random.sample(range(cols), 8)
attr = random.randint(0, cols-1)

plt.figure(1)

n_x, n_y = list(), list()
a_x, a_y = list(), list()
# data_set[:, attr] = StandardScaler().fit_transform(data_set[:, attr])
for i in range(rows):
    if labels[i] == 1:
        n_x.append(i)
        n_y.append(data_set[i, attr])
    else:
        a_x.append(i)
        a_y.append(data_set[i, attr])

plt.xlim(0, rows)

plt.scatter(n_x, n_y, label='true')
plt.scatter(a_x, a_y, label='false')
plt.title(attr)

plt.legend(loc='upper right')

plt.show()

