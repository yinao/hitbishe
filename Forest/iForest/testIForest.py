# !/usr/bin/env python
# -*-coding:utf-8-*-

import matplotlib.pyplot as plt
from iForest import IsolationForest
from iForest import Evaluation
from iForest import Show
from sklearn.metrics import roc_auc_score
import time
import Queue


fileObj = open("../dataSets/hapt57", "r")
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

Forest = IsolationForest(dataSets, 5, 256)

print "training cost %s s" %(time.clock() - trainBeginTime)


testBeginTime = time.clock()
scores = Evaluation(dataSets, Forest, hlimit=6)
print "test time %s s" %(time.clock() - testBeginTime)

print "AUC is: %s" % (roc_auc_score(labels, scores))


# def level_travel(tree):
#     queue = Queue.Queue()
#     queue.put(tree)
#     attrs = list()
#     while not queue.empty():
#         tree = queue.get()
#         if tree.external is not True:
#             attrs.append(tree.SplitAttrIndex)
#         if tree.Left is not None:
#             queue.put(tree.Left)
#         if tree.Right is not None:
#             queue.put(tree.Right)
#     return attrs
#
# attributes = level_travel(Forest[0])
#
# print attributes