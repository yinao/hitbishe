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


sample_one = 4  # numpy.random.randint(0, rows-1)
data_one = preprocessing.scale(data[sample_one])
# mean = data_one.mean()
# std = data_one.std()

sample_len = numpy.random.randint(10, cols / 3)
begin_point = numpy.random.randint(0, cols - sample_len)
for _ in range(10):

    k = 100
    results = list()

    for _ in range(k):

        factor = numpy.random.normal(0, 1, sample_len)

        width = numpy.random.randint(5, 20)
        b = numpy.random.randint(0, width)

        # result = numpy.floor((sum(factor * data_one[begin_point:begin_point+sample_len])+b)/width)
        result = sum(factor * data_one[begin_point:begin_point+sample_len])

        results.append(result)

    factor = numpy.random.normal(0, 1, k)
    result = sum(factor*numpy.array(results))
    if result < 0:
        print 0
    else:
        print 1


# probs = list()
# for i in range(cols):
#     tmp = (1.0/(std*(2*math.pi)**0.5)) * math.e**-(0.5*((data_one[i] - mean)/std)**2)
#     probs.append(tmp)
#
# plt.figure(1)
# plt.scatter(data_one, probs)
# plt.show()

# plt.figure(1)
# plt.plot(range(cols), data_one)
# plt.plot(range(cols), [mean for _ in range(cols)])
# plt.show()

