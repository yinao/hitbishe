# !/usr/bin/env python
# -*-coding:utf-8-*-


import numpy
import math
from sklearn import metrics, preprocessing
from matplotlib import pyplot as plt

data = numpy.loadtxt('../../data_series/forest/folda', delimiter=',')
labels = data[:, 0]
data = data[:, 1:]
rows, cols = data.shape

sample_one = 4#numpy.random.randint(0, rows-1)

data_one = preprocessing.scale(data[sample_one])

k = 15
results = list()
for i in range(rows):
    sample_len = cols
    begin_point = 0#numpy.random.randint(0, cols - sample_len)
    result = 0
    for _ in range(k):

        # mean = data_one.mean()
        # std = data_one.std()

        factor = numpy.random.normal(0, 1, sample_len)

        width = 8
        b = numpy.random.randint(0, width)

        # result += numpy.floor((sum(factor * data_one[begin_point:begin_point+sample_len])+b)/width)
        result += sum(factor*data_one[begin_point:begin_point+sample_len])

        # if result < 0:
        #     results += '0'
        # else:
        #     results += '1'

    # print results, int(results, 2),
    # print labels[i], result
    results.append(result/k)

print metrics.roc_auc_score(labels, results)
# print len(labels), len(results), rows

