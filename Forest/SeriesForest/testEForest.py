# !/usr/bin/env python
# -*-coding:utf-8-*-


import time
import numpy
import math
from sklearn.preprocessing import scale
from sklearn.metrics import roc_auc_score
from HashErrorForest import ErrorForest

data = numpy.loadtxt('../data_series/wafer', delimiter=',')
labels = data[:, 0]
data = data[:, 1:]
# print data.shape
rows, cols = data.shape
# print cols**0.5, cols/2
# exit()
# print rows, cols
# local_f = numpy.random.uniform(1.0/cols**0.5, 1-1.0/cols**0.5)
# print local_f
# print 1.0 / local_f
# print 1+0.5*math.log(cols, max(2, 1.0/local_f))
# print math.log(cols, max(2,1.0/local_f))
# s_a = numpy.random.uniform(1+0.5*math.log(cols, max(2,1.0/local_f)), math.log(cols, max(2,1.0/local_f)))
# print s_a, int(math.ceil(s_a))

for i in range(len(data)):
    data[i] = scale(data[i])

forest = ErrorForest()
forest.setup(sample_size=100, tree_size=20, node_size=15, k=15)

trainBeginTime = time.clock()

forest.build(data)

print "training cost %s s" %(time.clock() - trainBeginTime)

testBeginTime = time.clock()
scores = forest.evaluation(data, 5)
print "test time %s s" %(time.clock() - testBeginTime)

# print scores
for i in range(len(labels)):
    if labels[i] != 1 or labels[i] != 1.0:
        labels[i] = 0

print "AUC is: %s" % max(roc_auc_score(labels, scores), 1-roc_auc_score(labels, scores))
