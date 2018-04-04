# !/usr/bin/env python
# -*-coding:utf-8-*-

import matplotlib.pyplot as plt
from MBForest_2 import MBForest
from sklearn import preprocessing
from sklearn.metrics import roc_auc_score
import time

set_name = 'covertype'

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
forest = MBForest()
density_auc = list()
path_auc = list()
density_time = list()
path_time = list()
for i in range(10):
    trainBeginTime = time.clock()
    forest = MBForest()
    forest.setup(tree_num=15, sample_size=256, size_limit=15, height_limit=6, less_height=0.0015, much_height=0.9974)
    forest.build(dataSets)
    print "training cost %s s" %(time.clock() - trainBeginTime)
    # testBeginTime = time.clock()
    # scores = forest.evaluate(dataSets, hlimit=6)
    # auc = roc_auc_score(labels, scores)
    # cost_time = time.clock() - testBeginTime
    # path_auc.append(auc)
    # path_time.append(cost_time)

    testBeginTime = time.clock()
    density = forest.density_evaluate(dataSets, hlimit=6)
    d_auc = roc_auc_score(labels, density)
    cost_time = time.clock() - testBeginTime
    density_auc.append(d_auc)
    density_time.append(cost_time)

# print 'path method auc: %f, cost time: %f' %(sum(path_auc)/len(path_auc), sum(path_time) /len(path_time))
print 'density method auc: %f, cost time: %f' %(sum(density_auc)/len(density_auc), sum(density_time) /len(density_time))

