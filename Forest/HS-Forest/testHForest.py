# !/usr/bin/env python
# -*-coding:utf-8-*-


import time
import numpy
from sklearn.preprocessing import scale
from sklearn.metrics import roc_auc_score
from HashForest import HashForest

data = numpy.loadtxt('../dataSets/Satellite', delimiter=',')
labels = data[:, -1]
data = data[:, :-1]
# for i in range(len(data)):
#     data[i] = scale(data[i])

forest = HashForest()
forest.setup(sample_size=256, tree_size=10, node_size=15)

trainBeginTime = time.clock()

forest.build(data)

print "training cost %s s" %(time.clock() - trainBeginTime)

testBeginTime = time.clock()
scores = forest.evaluation(data, 6)
print "test time %s s" %(time.clock() - testBeginTime)

# print scores
for i in range(len(labels)):
    if labels[i] != 1 or labels[i] != 1.0:
        labels[i] = 0

print "AUC is: %s" % (roc_auc_score(labels, scores))
