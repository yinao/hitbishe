# !/usr/bin/env python
# -*-coding:utf-8-*-

import time
import matplotlib.pyplot as pyplot
from HSTn_WithData import HS_Forest
from sklearn import preprocessing
from sklearn.metrics import roc_auc_score
# from matplotlib import pyplot

# reading training data
begin = time.clock()
fileObj = open("../dataSets/breast", "r")
dataSets, labels = [], []
for line in fileObj.readlines():
    tmp = line.split(',')
    labels.append(int(tmp[-1]))
    dataSets.append([float(x) for x in tmp[:-1]])
fileObj.close()
# dataSets = preprocessing.scale(dataSets)
end = time.clock()
print "reading data cost %s s" %(end-begin)

begin = time.clock()
k = 0
fileObj = open("../dataSets/arrhythmia", "r")
data_test, labels_test = [], []
for line in fileObj.readlines():
    # if k > 100:
    #     break
    # k+=1
    tmp = line.split(",")
    labels_test.append(int(tmp[-1]))
    data_test.append([float(x) for x in tmp[:-1]])
fileObj.close()
# data_test = preprocessing.scale(data_test)
end = time.clock()
print "read test cost %s s" %(end-begin)

begin = time.clock()
forest = HS_Forest()
forest.setup(hlimit=8, tree_num=25, sample_size=256)
forest.build(dataSets)
end = time.clock()
print "building forest cost %s s" %(end-begin)

begin = time.clock()
scores = forest.evaluate(data_test)
end = time.clock()
print "evaluate model cost %s s" %(end-begin)

auc = roc_auc_score(labels_test, scores)

print "AUC score is %s" %(auc)

# pyplot.figure(1)
# pyplot.plot(range(len(scores)), scores, marker=".")
# pyplot.show()

