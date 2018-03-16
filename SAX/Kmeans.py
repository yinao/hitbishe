# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy
from sklearn.cluster import KMeans
from sklearn.metrics import roc_auc_score

data = numpy.loadtxt('dataSets/handoutlines', delimiter=',')
labels = data[:, 0]
data = data[:, 1:]

# data = numpy.loadtxt('dataSets/egg13.txt')
# labels = numpy.loadtxt('dataSets/label13.txt', dtype='int')
# data = data[100:150]
# labels = labels[100:150]

clf = KMeans(n_clusters=2)

pre = clf.fit(data)

pred = clf.labels_

auc = roc_auc_score(labels, pred)

if auc < 0.5:
    print 1-auc
else:
    print auc

