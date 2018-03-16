# !/usr/bin/env python
# -*-coding:utf-8-*-

import matplotlib.pyplot as plt
from Forest.iForest.iForest import IsolationForest
from Forest.iForest.iForest import Evaluation
from Forest.iForest.iForest import Show
from sklearn.metrics import roc_auc_score
import time
import Queue
import numpy


fileObj = open("../dataSets/breast", "r")
dataLines = fileObj.readlines()
dataSets = []
labels = []
for line in dataLines:
    tmp = line.split(',')
    labels.append(int(tmp[-1]))
    tmp = tmp[:-1]
    dataSets.append([float(x) for x in tmp])

fileObj.close()

trainBeginTime = time.clock()

Forest = IsolationForest(dataSets, 1, 256)

print "training cost %s s" %(time.clock() - trainBeginTime)


testBeginTime = time.clock()
scores = Evaluation(dataSets, Forest, hlimit=6)
print "test time %s s" %(time.clock() - testBeginTime)

print "AUC is: %s" % (roc_auc_score(labels, scores))


def level_travel(tree):
    queue = Queue.Queue()
    queue.put(tree)
    attrs = list()
    values = list()
    while not queue.empty():
        tree = queue.get()
        if tree.external is not True:
            attrs.append(tree.SplitAttrIndex)
            values.append(tree.SplitValue)
        if tree.Left is not None:
            queue.put(tree.Left)
        if tree.Right is not None:
            queue.put(tree.Right)
    return attrs, values

attributes, values = level_travel(Forest[0])

print 'selected attributes: ', attributes
print 'selected attributes values', [round(x, 4) for x in values]


