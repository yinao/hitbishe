# !/user/bin/env python
# -*-coding:utf-8-*-

import numpy

data = numpy.loadtxt('../dataSets/egg13.txt')
labels = numpy.loadtxt('../dataSets/label13.txt')
# data = data[:, 1:]
rows, cols = data.shape

zero, one = 0, 0
for l in labels:
    if l == 1:
        one += 1
    else:
        zero += 1

print 'rows=%d, cols=%d, anomaly=%f' % (rows, cols, float(min(zero, one)) / rows)