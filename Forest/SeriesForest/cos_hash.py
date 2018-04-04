# !/usr/bin/env python
# -*-coding:utf-8-*-


import time
import numpy
from sklearn.preprocessing import scale
from sklearn.metrics import roc_auc_score
from HashForest_withAllWeight import HashForest
from matplotlib import pyplot as plt

data = numpy.loadtxt('../../data_series/forest/folda', delimiter=',')
labels = data[:, 0]
data = data[:, 1:]
rows, cols = data.shape

for i in range(rows):
    data[i] = scale(data[i])

factor = numpy.random.randn(50) / numpy.sqrt(50)
begin = numpy.random.randint(0, cols-50)
z_lst = numpy.empty(rows)
y_list = numpy.empty(rows)
for i in range(len(z_lst)):
    # factor = numpy.random.randn(50) /(50**0.2)
    z = numpy.sum(factor*data[i][begin:begin+50])
    z_lst[i] = z
    # z_lst[i] = 1.0/(1+numpy.e**-z)
    # z_lst[i] = numpy.cos(z)
    y_list[i] =numpy.exp(-0.05*sum(data[i][begin:begin+50]**2))

n_x, n_y = list(), list()
a_x, a_y = list(), list()
for i in range(rows):
    if labels[i] == 1 or labels[i] == 1.0:
        n_y.append(y_list[i])
        n_x.append(i)
    else:
        a_y.append(y_list[i])
        a_x.append(i)

plt.figure(1)
plt.scatter(n_x, n_y)
plt.scatter(a_x, a_y)
plt.show()

# print z_lst
# print '均值', numpy.mean(z_lst)
# print '方差', numpy.var(z_lst)
# plt.hist(z_lst, 100)
# plt.show()
