# !/usr/bin/env python
# -*-coding:utf-8-*-

import time
from HSTn import HS_Forest
from sklearn import preprocessing
from sklearn.metrics import roc_auc_score
from matplotlib import pyplot

# reading training data
begin = time.clock()
fileObj = open("../dataSets/ann_thyroid", "r")
dataSets, labels = [], []
for line in fileObj.readlines():
    tmp = line.split(',')
    labels.append(int(tmp[-1]))
    tmp = tmp[0:-1]
    dataSets.append([float(x) for x in tmp])
fileObj.close()
dataSets = preprocessing.scale(dataSets)
end = time.clock()
print "reading data cost %s s" %(end-begin)

begin = time.clock()
forest = HS_Forest()
forest.setup(attr=len(dataSets[0]), hlimit=10, treeNum=25)
forest.build()
end = time.clock()
print "building forest cost %s s" %(end-begin)

begin = time.clock()
forest.initModel(dataSets)
end = time.clock()
print "update forest mass cost %s s" %(end-begin)

begin = time.clock()
fileObj = open("../dataSets/ann_thyroid", "r")
data_test, labels_test = [], []
for line in fileObj.readlines():
    tmp = line.split(",")
    labels_test.append(int(tmp[-1]))
    tmp = tmp[0:-1]
    data_test.append([float(x) for x in tmp])
fileObj.close()
data_test = preprocessing.scale(data_test)
end = time.clock()
print "read test cost %s s" %(end-begin)

begin = time.clock()
scores = forest.evaluate(data_test, hlimit=6)
end = time.clock()
print "evaluate model cost %s s" %(end-begin)


print "AUC score is %s" %roc_auc_score(labels_test, scores)

# pyplot.figure(1)
# x = [x for x in range(len(scores))]
# pyplot.scatter(x, scores)
# pyplot.show()
