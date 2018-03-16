# !/usr/bin/env python
# -*-coding:utf-8-*-

import matplotlib.pyplot as plt
from SForest import SForest
from sklearn import preprocessing
from sklearn.metrics import roc_auc_score
import time
import numpy

set_name = 'pima'

fileObj = open("../dataSets/"+set_name, "r")
dataLines = fileObj.readlines()
dataSets = []
labels = []
for line in dataLines:
    tmp = line.split(',')
    labels.append(int(tmp[-1]))
    tmp = tmp[:-1]
    dataSets.append([float(x) for x in tmp])
fileObj.close()
dataSets = numpy.array(dataSets)
# dataSets = preprocessing.scale(dataSets)
# dataSets = preprocessing.minmax_scale(dataSets)

# test mbforest code
trainBeginTime = time.clock()
forest = SForest()
forest.setup(tree_num=5, sample_size=256, size_limit=5, height_limit=6, sample_attr=3)
forest.build(dataSets)
print "training cost %s s" %(time.clock() - trainBeginTime)
testBeginTime = time.clock()
scores = forest.evaluate(dataSets, hlimit=6)
print "test time %s s" %(time.clock() - testBeginTime)
auc = roc_auc_score(labels, scores)
print "AUC is: %s" % (auc)