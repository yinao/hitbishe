# !/usr/bin/env python
# -*-coding:utf-8-*-


import numpy
from sklearn.metrics import roc_auc_score
from SeriesForest import SeriesForest

data = numpy.loadtxt('../data_series/strawberry', delimiter=',')
labels = data[:, 0]
data = data[:, 1:]

forest = SeriesForest()

forest.build(data)

scores = forest.evaluation(data, 10)

print scores
for i in range(len(labels)):
    if labels[i] != 1 or labels[i] != 1.0:
        labels[i] = 0

print roc_auc_score(labels, scores)
