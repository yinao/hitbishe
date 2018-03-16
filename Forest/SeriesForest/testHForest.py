# !/usr/bin/env python
# -*-coding:utf-8-*-


import time
import numpy
from sklearn.preprocessing import scale
from sklearn.metrics import roc_auc_score
from HashForest import HashForest

data = numpy.loadtxt('../data_series/strawberry', delimiter=',')
labels = data[:, 0]
data = data[:, 1:]
# print data.shape
for i in range(len(data)):
    data[i] = scale(data[i])

forest = HashForest()
forest.setup(sample_size=100, tree_size=40, node_size=15, k=17)

trainBeginTime = time.clock()

forest.build(data)

print "training cost %s s" %(time.clock() - trainBeginTime)

testBeginTime = time.clock()
scores = forest.evaluation(data, 4)
print "test time %s s" %(time.clock() - testBeginTime)

# print scores
for i in range(len(labels)):
    if labels[i] != 1 or labels[i] != 1.0:
        labels[i] = 0

print "AUC is: %s" % max(roc_auc_score(labels, scores), 1-roc_auc_score(labels, scores))
