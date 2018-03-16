# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy
import time
import random
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics import roc_auc_score

class BitCluster:
    def __init__(self):
        self.center = 1
        self.radius = 1
        self.num_members = 0
        self.members = list()
        self.actual = list()


def bit_cluster(bit_db, k):
    bCluster = list()
    centers = random.sample(range(len(bit_db)), k)

    for i in range(k):
        b = BitCluster()
        b.center = centers[i]
        b.num_members = 1
        bCluster.append(b)

    patternCtag = [0] * len(bit_db)
    for i in range(len(bit_db)):
        if i in centers:
            continue

        p = 1
        for j in range(k):
            if bit_dist(bit_db[i], bit_db[j]) < bit_dist(bit_db[i], bit_db[bCluster[p].center]):
                p = j


        patternCtag[i] = p
        # bCluster[p].members[bCluster[p].num_members] = j
        # bCluster[p].num_members += 1
        if i not in bCluster[p].members:
            bCluster[p].members.append(i)


    for i in range(k):
        bCluster[i].radius = calClusterRadius(bCluster[i])

    return bCluster, patternCtag


def calClusterRadius(cluster):
    index = cluster.members
    radius = 0
    for i in index:
        dist = 0
        for j in range(len(data[i])):
            dist += (data[i][j] - data[cluster.center][j])**2
        dist **= 0.5
        radius = max(radius, dist)
    return radius

def bit_dist(bit_a, bit_b):
    dist, bit_len = 0, len(bit_a)
    for i in range(bit_len):
        if bit_a[i] == bit_b[i]:
             dist += 0
        else:
            dist += 2**(bit_len-i-1)
    return dist*1.0 / bit_len


win_size = 7
k = 2
data = numpy.loadtxt('dataSets/ToeSegmentation2', delimiter=',')
labels = data[:, 0]
data = data[:, 1:]
# data = numpy.loadtxt('dataSets/egg13.txt')
# labels = numpy.loadtxt('dataSets/label13.txt', dtype='int')
# data = data[100:150]
# labels = labels[100:150]
rows, cols = data.shape

begin = time.clock()

bit_db = list()
for i in range(rows):
    d = data[i]
    tmp = list()
    for j in range(0, len(d), win_size):
        low = j
        high = min(len(d), j+win_size)
        t = sum(d[low: high])*(high-low) / len(d)
        # tmp.append(sum(d[j:min(j+win_size, len(d))] / min(win_size, len(d)-j)))
        tmp.append(t)

    bit_tmp = list()
    for i in range(len(tmp)-1):
        if tmp[i] < tmp[i+1]:
            bit_tmp.append(1)
        else:
            bit_tmp.append(0)
    bit_db.append(bit_tmp)

bCluster, tags = bit_cluster(bit_db, 2)
outers = list()
inners = list()
for cluster in bCluster:
    outers.append(len(cluster.members))

index = [0, 1]
if outers[1] < outers[0]:
    index = [1, 0]

for i in index:
    inners += bCluster[i].members

dists = dict()
for i in index:
    p = data[bCluster[i].center]
    min_dist = float('inf')
    for j in inners:
        dist = 0
        q = data[j]
        for k in range(len(p)):
            dist += (p[k]-q[k])**2
        min_dist = min(min_dist, dist**0.5)
    dists[i] = min_dist

# print tags
pred = list()
for t in range(len(tags)):
    pred.append(dists[tags[t]])

print 'time cost : %f' %(time.clock() - begin)

auc = roc_auc_score(labels, pred)
if auc < 0.5:
    auc = 1-auc
