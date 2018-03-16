import os
import sys
import numpy
import operator
import random
from numpy import array, sum, sqrt
import time
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_predict
from sklearn.preprocessing import scale, StandardScaler
from bitarray import bitarray
from matplotlib import pyplot as plt

data = numpy.loadtxt('../dataSets/strawberry', delimiter=',')
labels = data[:, 0]
data = data[:, 1:]
rows, cols = data.shape

k = 3
trainBeginTime = time.clock()
raw_dist = numpy.zeros((rows, rows))
pred = list()
for i in range(rows):
    for j in range(i+1, rows):
        raw_dist[i, j] = numpy.linalg.norm(data[i] - data[j])
        raw_dist[i, j] **= 0.5
        raw_dist[j, i] = raw_dist[i, j]

    arg_index = numpy.argsort(raw_dist[i])
    tmp = dict()
    if i in arg_index[:k]:
        for l in arg_index[:k+1]:
            if l == i:
                continue
            tmp[labels[l]] = tmp.get(labels[l], 0) + 1
    else:
        for l in arg_index[:k]:
            tmp[labels[l]] = tmp.get(labels[l], 0) + 1

    pre = sorted(tmp.items(), key=operator.itemgetter(1), reverse=True)[0][0]
    pred.append(pre)

for i in range(rows):
    if labels[i] != 1:
        labels[i] = 0

    if pred[i] != 1.0:
        pred[i] = 0

# print labels
# print pred

print 'Precision: %f' % precision_score(labels, pred, average='macro')
print 'Recall   : %f' % recall_score(labels, pred, average='macro')
print 'F1       : %f' % f1_score(labels, pred, average='macro')
print 'AUC      : %f' % roc_auc_score(labels, pred)
print 'COST     : %f' % (time.clock()-trainBeginTime)
