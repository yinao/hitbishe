# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy

data = numpy.loadtxt('../dataSets/ToeSegmentation2', delimiter=',')

dist = numpy.loadtxt('ToeSegmentation2')

labels = data[:,0]

from sklearn.metrics import roc_auc_score

print roc_auc_score(labels, dist)