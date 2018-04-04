# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy
from matplotlib import pyplot as plt

data = numpy.loadtxt('../data_series/wafer', delimiter=',')
labels = data[:, 0]
data = data[:, 1:]
rows, cols = data.shape

n_cols = 20
begin = numpy.random.randint(0, cols-n_cols)

n_g_x, a_g_x = list(), list()
n_g, a_g = list(), list()
for i in range(rows):
    tmp = numpy.exp(-0.04*numpy.sum(numpy.square(data[i, begin:begin+n_cols])))
    if labels[i] == 1 or labels[i] == 1.0:
        n_g_x.append(i)
        n_g.append(tmp)
    else:
        a_g_x.append(i)
        a_g.append(tmp)

factor = numpy.random.normal(n_cols)
n_x, n_y = list(), list()
a_x, a_y = list(), list()
for i in range(rows):
    tmp = numpy.sum(factor*data[i, begin:begin+n_cols])
    if labels[i] == 1 or labels[i] == 1.0:
        n_x.append(i)
        n_y.append(tmp)
    else:
        a_x.append(i)
        a_y.append(tmp)


plt.figure(1)
plt.subplot(121)
plt.scatter(n_x, n_y)
plt.scatter(a_x, a_y)

plt.subplot(122)
plt.scatter(n_g_x, n_g)
plt.scatter(a_g_x, a_g)

plt.show()

