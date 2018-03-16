# !/usr/bin/env python
# -*-coding:utf-8-*-


import time
import numpy
from sklearn.preprocessing import scale
from sklearn.metrics import roc_auc_score
from HashForest_withAllWeight import HashForest
from matplotlib import pyplot as plt

data = numpy.loadtxt('../data_series/wafer', delimiter=',')
labels = data[:, 0]
data = data[:, 1:]
for i in range(len(data)):
    data[i] = scale(data[i])

# factor = numpy.random.randn(50) / numpy.sqrt(50)
begin = numpy.random.randint(0, data.shape[1]-50)
z_lst = numpy.empty(data.shape[0])
for i in range(len(z_lst)):
    factor = numpy.random.randn(50) / numpy.sqrt(50)
    z = numpy.sum(factor*data[i][begin:begin+50])
    z_lst[i] = z

print z_lst
print '均值', numpy.mean(z_lst)
print '方差', numpy.var(z_lst)
plt.hist(z_lst, 100)
plt.show()


# forest = HashForest()
# forest.setup(sample_size=256, tree_size=15, node_size=15, h=7)
#
# trainBeginTime = time.clock()
#
# forest.build(data)
#
# print "training cost %s s" %(time.clock() - trainBeginTime)
#
# testBeginTime = time.clock()
# scores = forest.evaluation(data, 3)
# print "test time %s s" %(time.clock() - testBeginTime)
#
# # print scores
# for i in range(len(labels)):
#     if labels[i] != 1 or labels[i] != 1.0:
#         labels[i] = 0
#
# print "AUC is: %s" % (roc_auc_score(labels, scores))
