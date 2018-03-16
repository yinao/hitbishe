# !/usr/bin/env python
# -*-coding:utf-8-*-


import numpy
import math
from sklearn import metrics, preprocessing
from matplotlib import pyplot as plt

data = numpy.loadtxt('../data_series/gun1', delimiter=',')
labels = data[:, 0]
data = data[:, 1:]
rows, cols = data.shape

sample_one = 4#numpy.random.randint(0, rows-1)

data_one = preprocessing.scale(data[sample_one])

k = 5
results = ''
for _ in range(10):
    sample_len = 10
    begin_point = 1#numpy.random.randint(0, cols - sample_len)
    for _ in range(k):

        # mean = data_one.mean()
        # std = data_one.std()

        factor = numpy.random.normal(0, 1, sample_len)

        width = numpy.random.randint(5, 20)
        b = numpy.random.randint(0, width)

        result = numpy.floor((sum(factor * data_one[begin_point:begin_point+sample_len])+b)/width)
        # result = sum(factor*data_one[begin_point:begin_point+sample_len])

        if result < 0:
            results += '0'
        else:
            results += '1'

    # print results, int(results, 2),
    print (int(results, 2)*k+numpy.random.randint(1,k)) % 2


