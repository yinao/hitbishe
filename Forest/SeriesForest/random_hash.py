# !/usr/bin/env python
# -*-coding:utf-8-*-


import numpy
import math
from sklearn import metrics, preprocessing
from matplotlib import pyplot as plt
from Forest import generalized_ir

data = numpy.loadtxt('../data_series/gun1', delimiter=',')
labels = data[:, 0]
data = data[:, 1:]
rows, cols = data.shape

for i in range(rows):
    if labels[i] != 1 or labels[i] != 1.0:
        labels[i] = -1
# print labels

# data_one = preprocessing.scale(data[0])

n_col = 1

new_data = numpy.zeros((rows, n_col))
s_cols = numpy.random.randint(int(cols**0.25), int(cols**0.75))
factor = numpy.random.randn(s_cols)
w = 16
b = numpy.random.randint(0, w)

for k in range(n_col):
    begin = numpy.random.randint(0, cols-s_cols)
    result = []
    for i in range(rows):
        tmp = numpy.sum(factor*data[i, begin:begin+s_cols])
        result.append(tmp)
        # result.append(numpy.ceil((tmp+b)/w))
    # result = numpy.ceil((numpy.sum(factor*)))

    new_data[:,k] = numpy.array(result)

print generalized_ir.generalized_ir([new_data, labels])

# numpy.savetxt('text.txt', new_data, fmt='%d')

# n_y, a_y = list(), list()
# for i in range(rows):
#     if labels[i] == 1 or labels[i] == 1.0:
#         n_y.append(i)
#     else:
#         a_y.append(i)
#
# plt.figure(1)
# plt.scatter(n_y, [result[i] for i in n_y])
# plt.scatter(a_y, [result[i] for i in a_y])
# plt.show()
