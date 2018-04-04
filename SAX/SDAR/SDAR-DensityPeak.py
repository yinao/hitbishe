# !/usr/bin/env python
# -*-coding:utf-8-*-


import numpy
import time
from math import log
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import scale, StandardScaler
from bitarray import bitarray
from matplotlib import pyplot as plt


def enc_dist(vec1, vec2):
    return numpy.linalg.norm(vec1 - vec2)


def sdar_dist(vec1, vec2, bit1, bit2, w):
    dist = numpy.linalg.norm(vec1 - vec2) * (w**0.5)
    # for k, b in enumerate(bit1):
    #     dist += (b ^ bit2[k]).count()*1.0 / w
    return dist

data = numpy.loadtxt('../dataSets/lighting2', delimiter=',')
labels = data[:, 0].astype('int')
data = data[:, 1:]

rows, cols = data.shape

win_size = 9
k = 2

bit_data = list()
paa_data = list()
for d in data:
    tmp = list()
    bit_tmp = list()
    paa_tmp = list()
    for i in range(0, len(d), win_size):
        low = i
        high = min(len(d), i + win_size)
        PAA = sum(d[low: high]) / (high - low)
        paa_tmp.append(PAA)
        b = bitarray()
        for j in range(low, high):
            if d[j] < PAA:
                b.append(False)
            else:
                b.append(True)
        bit_tmp.append(b)
    bit_data.append(bit_tmp)
    paa_data.append(paa_tmp)

# exit()
paa_data = numpy.array(paa_data)
_, p_cols = paa_data.shape

begin = time.clock()
dist_matrix = numpy.zeros((rows, rows))

# find local density
densityVector = numpy.zeros(rows)
dist_cutoff = 8
for i in range(rows):
    for j in range(rows):
        if i == j:
            continue
        # dist_matrix[i, j] = enc_dist(data[i], data[j])
        dist_matrix[i, j] = sdar_dist(paa_data[i], paa_data[j], bit_data[i], bit_data[j], win_size)
        densityVector[i] += numpy.e ** (-(dist_matrix[i, j] / dist_cutoff)**2)

sortedIndex = numpy.argsort(-densityVector)

# find the nn distance of higher local density
distanceVector = numpy.array([float('inf')] * rows)
nnVector = numpy.array([0] * rows)
for i in range(1, rows):
    for j in sortedIndex[:i]:
        if distanceVector[sortedIndex[i]] > dist_matrix[sortedIndex[i], j]:
            distanceVector[sortedIndex[i]] = dist_matrix[sortedIndex[i], j]
            nnVector[sortedIndex[i]] = j

distanceVector[sortedIndex[0]] = max(distanceVector)

# calculating the multiply of the local density and nn distance
density_dist = numpy.argsort(-(densityVector * distanceVector))

clusters = numpy.array([-1] * rows)
for i in range(k):
    clusters[density_dist[i]] = i
# print clusters

for i in range(rows):
    if clusters[sortedIndex[i]] == -1:
        clusters[sortedIndex[i]] = clusters[nnVector[sortedIndex[i]]]


for i in range(rows):
    if labels[i] == 1:
        labels[i] = 0
    else:
        labels[i] = 1
print labels
print clusters
print 'Precision: %f' % precision_score(labels, clusters, average='macro')
print 'Recall: %f' % recall_score(labels, clusters, average='macro')
print 'F1: %f' % f1_score(labels, clusters, average='macro')
print 'AUC: %f' % roc_auc_score(labels, clusters)
print 'Cost: %f' % (time.clock() - begin)

# f_obj = open('cluster.txt', 'w')
# f_obj.write('density-peak')
# f_obj.write('Precision: %f\n' % precision_score(labels, clusters))
# f_obj.write('Recall: %f\n' % recall_score(labels, clusters))
# f_obj.write('F1: %f\n\n\n\n' % f1_score(labels, clusters))
