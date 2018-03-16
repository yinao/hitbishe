# !/usr/bin/env python
# -*-coding:utf-8-*-

import time
import numpy
from RS_Forest import RS_Forest
from sklearn import preprocessing
from sklearn.metrics import roc_auc_score
from matplotlib import pyplot

# reading training data
begin = time.clock()
# fileObj = open("../dataSets/epileptic", "r")
# dataSets, labels = [], []
# for line in fileObj.readlines():
#     tmp = line.split(',')
#     labels.append(int(tmp[-1]))
#     dataSets.append([float(x) for x in tmp[:-1]])
# fileObj.close()

fileObj = open("../data_series/ToeSegmentation2", "r")
dataSets, labels = [], []
for line in fileObj.readlines():
    tmp = line.split(',')
    labels.append(int(tmp[0]))
    dataSets.append([float(x) for x in tmp[1:]])
fileObj.close()

# exit()
dataSets = preprocessing.scale(dataSets)
end = time.clock()
print "reading data cost %s s" %(end-begin)


begin = time.clock()
forest = RS_Forest()
forest.setup(hlimit=10, treeNum=30, attr=len(dataSets[0]))
forest.buildModel()
end = time.clock()
print "building forest cost %s s" %(end-begin)

# begin = time.clock()
# forest.initModel(dataSets)
# end = time.clock()
# print "update forest mass cost %s s" %(end-begin)

# forest.testTreeStructure()


begin = time.clock()
scores = forest.evaluate(dataSets, hlimit=5)
end = time.clock()
print "evaluate model cost %s s" %(end-begin)

auc = roc_auc_score(labels, scores)

print "AUC score is %s" %auc

# pyplot.figure(1)
# pyplot.scatter(range(len(scores)), scores)
# pyplot.show()

