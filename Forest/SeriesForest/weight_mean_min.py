# !/usr/bin/env python
# -*-coding:utf-8-*-


import numpy
import math
from sklearn import metrics, preprocessing
from matplotlib import pyplot as plt

data = numpy.loadtxt('../../data_series/lighting', delimiter=',')
labels = data[:, 0]
data = data[:, 1:]
rows, cols = data.shape

# data_one = preprocessing.scale(data[0])

s_cols = numpy.random.randint(int(cols**0.25), int(cols**0.75))
begin = numpy.random.randint(0, cols-s_cols)

k = 5
factor = numpy.zeros((k, cols))
for i in range(k):
    factor[i] = numpy.random.randn(cols)

min_error = float('inf')
error = list()
for j in range(k):
    tmp = list()
    for i in range(rows):
        result = (factor[j]*preprocessing.scale(data[i])).mean()
        tmp.append(abs(result - preprocessing.scale(data[i]).mean()*factor[j].mean()))
    if min_error > sum(tmp)/k:
        min_error = sum(tmp)/k
        print min_error
        error = tmp

split = numpy.random.uniform(min(error), max(error))
l_e, r_e = 0, 0
for i in range(rows):
    if error[i] < split and labels[i] != 1:
        l_e += 1
    if error[i] > split and labels[i] != 1:
        r_e += 1

print l_e, r_e

n_x = list()
a_x = list()
for i in range(rows):
    if labels[i] == 1 or labels[i] == 1.0:
        n_x.append(i)
    else:
        a_x.append(i)

plt.scatter(a_x, [error[k] for k in a_x], c='r', label='abnormal')
plt.scatter(n_x, [error[k] for k in n_x], c='b', label='normal')
# plt.plot(range(rows), error)
plt.plot(range(rows), [split for _ in range(rows)], c='g')
plt.legend(loc='upper right')
plt.show()
