# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy

data_set = 'coffee'

data = numpy.loadtxt(data_set, delimiter=',')
labels = data[:, 0]
data = data[:, 1:]

obj = open('data_info.txt', 'w')

