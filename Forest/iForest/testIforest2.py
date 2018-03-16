# !/usr/bin/env python
# -*-coding:utf-8-*-

import matplotlib.pyplot as plt
from iForest import IsolationForest
from iForest import Evaluation
from iForest import Show
from sklearn.metrics import roc_auc_score
import time


fileObj = open("../data_series/ToeSegmentation2", "r")
dataLines = fileObj.readlines()
dataSets = []
labels = []
for line in dataLines:
    tmp = line.split(',')
    labels.append(int(tmp[0]))
    tmp = tmp[1:]
    dataSets.append([float(x) for x in tmp])

fileObj.close()

trainBeginTime = time.clock()

Forest = IsolationForest(dataSets, 25, 150)

print "training cost %s s" %(time.clock() - trainBeginTime)


testBeginTime = time.clock()
scores = Evaluation(dataSets, Forest, hlimit=6)
print "test time %s s" %(time.clock() - testBeginTime)

for i in range(len(labels)):
    if labels[i] != 1 or labels[i] != 1.0:
        labels[i] = 0

print "AUC is: %s" % (roc_auc_score(labels, scores))
