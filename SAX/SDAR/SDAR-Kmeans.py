# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy
import random
import time
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score, classification_report
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale, StandardScaler
from bitarray import bitarray
from matplotlib import pyplot as plt

data = numpy.loadtxt('cluster/medical_images', delimiter=',')
labels = data[:, 0].astype('int')
data = data[:, 1:]

clf = KMeans(n_clusters=10)

pre = clf.fit(data)

pred = clf.labels_


# print 'Precision: %f' % precision_score(labels, pred, average='macro')
# print 'Recall: %f' % recall_score(labels, pred, average='macro')
# print 'F1: %f' % f1_score(labels, pred, average='macro')