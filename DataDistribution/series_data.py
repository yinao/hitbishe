# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy

data = numpy.loadtxt('../data_series/gun1', delimiter=',')
label = data[:, 0]
data = data[:, 1:]
rows, cols = data.shape

stds = list()
for i in range(rows):
    stds.append(data[i].std())

print stds
