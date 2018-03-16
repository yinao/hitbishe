# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy


data = numpy.loadtxt('dataSets/ECG200/ecg200')
labels = data[:, 0]
data = data[:, 1:]
rows, cols = data.shape
# print rows, cols

n_data = data.reshape(rows*cols)

numpy.savetxt('dataSets/series/ecg200', n_data, delimiter=',', fmt='%f')