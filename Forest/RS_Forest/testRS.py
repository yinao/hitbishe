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

fileObj = open("../dataSets/pima", "r")
dataSets, labels = [], []
for line in fileObj.readlines():
    tmp = line.split(',')
    labels.append(int(tmp[-1]))
    dataSets.append([float(x) for x in tmp[:-1]])
fileObj.close()

# exit()
dataSets = preprocessing.scale(dataSets)
end = time.clock()
print "reading data cost %s s" %(end-begin)

obj = open('../MyForest/results/pima/rs_t1-25_h6.txt', 'w')
obj.write('height\tauc\t test_time\n')

for i in range(1, 26):

    begin = time.clock()
    forest = RS_Forest()
    forest.setup(hlimit=6, treeNum=i, attr=len(dataSets[0]))
    forest.buildModel()
    end = time.clock()
    print "building forest cost %s s" %(end-begin)

    # begin = time.clock()
    # forest.initModel(dataSets)
    # end = time.clock()
    # print "update forest mass cost %s s" %(end-begin)

    # forest.testTreeStructure()


    begin = time.clock()
    scores = forest.evaluate(dataSets, hlimit=6)
    end = time.clock()
    print "evaluate model cost %s s" %(end-begin)

    auc = roc_auc_score(labels, scores)

    print "AUC score is %s" %auc

    obj.write('%d \t %f \t %f \n' % (i, auc, (end - begin)))

obj.close()

# pyplot.figure(1)
# pyplot.scatter(range(len(scores)), scores)
# pyplot.show()

