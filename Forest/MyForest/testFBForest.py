# !/usr/bin/env python
# -*-coding:utf-8-*-

import matplotlib.pyplot as plt
from FBForest import FBForest
from sklearn import preprocessing
from sklearn.metrics import roc_auc_score
import time

set_name = 'ionosphere'

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
# dataSets = preprocessing.scale(dataSets)

# test mbforest code
trainBeginTime = time.clock()
forest = FBForest()
forest.setup(tree_num=30, sample_size=256, size_limit=2, height_limit=8, less_height=0.2, much_height=0.96)
forest.build(dataSets)
print "training cost %s s" %(time.clock() - trainBeginTime)
testBeginTime = time.clock()
scores = forest.evaluate(dataSets, hlimit=6)
print "test time %s s" %(time.clock() - testBeginTime)
auc = roc_auc_score(labels, scores)
print "AUC is: %s" % (auc)
#
# plt.figure(1)
# plt.plot(range(len(scores)), scores)
# plt.scatter(range(len(labels)), labels, marker='*', color='r')
# plt.show()
