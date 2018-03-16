import numpy
import time
from sklearn.metrics import roc_auc_score, euclidean_distances
from sklearn.preprocessing import scale
from matplotlib import pyplot as plt

cutlines = dict()
cutlines[2] = [0, float('inf')]
cutlines[3] = [-0.43, 0.43, float('inf')]
cutlines[4] = [-0.67, 0, 0.67, float('inf')]
cutlines[5] = [-0.84, -0.25, 0.25, 0.84, float('inf')]
cutlines[6] = [-0.97, -0.43, 0, 0.43, 0.97, float('inf')]
cutlines[7] = [-1.07, -0.57, -0.18, 0.18, 0.57, 1.07, float('inf')]
cutlines[8] = [-1.15, -0.67, -0.32, 0, 0.32, 0.67, 1.15, float('inf')]
cutlines[9] = [-1.22, -0.76, -0.43, -0.14, 0.14, 0.43, 0.76, 1.22, float('inf')]
cutlines[10] = [-1.28, -0.84, -0.52, -0.25, 0, 0.25, 0.52, 0.84, 1.28, float('inf')]

words = 3


def sax_dist(a, b):
    dist = 0
    for i in range(len(a)):
        t_a = int(a[i])
        t_b = int(b[i])
        if abs(int(t_a) - int(t_b)) <= 1:
            dist += 0
        else:
            # print cutlines[words][max(t_a, t_b)-1-1], cutlines[words][min(t_a, t_b)-1]
            dist += cutlines[words][max(t_a, t_b)-1-1] - cutlines[words][min(t_a, t_b)-1]
    return dist

win_size = 7

data = numpy.loadtxt('dataSets/gun1', delimiter=',')
labels = data[:, 0]
data = data[:, 1:]
rows, cols = data.shape



symbol_data = dict()
for j in range(len(data)):
    d = data[j]
    tmp = ''
    d = scale(d)
    for i in range(0, len(d), win_size):
        PAA = sum(d[i:i+win_size]) / win_size
        for k in range(words):
            if PAA < cutlines[words][k]:
                break
        tmp += (str(k+1))

    symbol_data[tmp] = symbol_data.get(tmp, [])
    symbol_data[tmp].append(j)

keys = symbol_data.keys()
index = symbol_data.values()
index_count = [len(idx) for idx in index]
argindex = numpy.argsort(index_count)

inners = list()
for a_i in argindex:
    inners += symbol_data[keys[a_i]]


begin = time.clock()

dists = dict()
for idx in argindex:
    out_key = keys[idx]
    outliers = index[idx]

    for i in outliers:
        dists[i] = dists.get(i, float('inf'))
        # first counting the dist with same pattern
        for j in outliers:
            if i == j:
                continue
            else:
                dists[i] = min(dists[i], numpy.sqrt(numpy.sum((data[i][k] - data[j][k]) ** 2)))

        # then calculating dist with other pattern
        for jdx in argindex:
            if jdx == idx:
                continue
            in_key = keys[jdx]
            if sax_dist(out_key, in_key) > dists[i]:
                continue
            inners = index[jdx]
            for j in inners:
                dists[i] = min(dists[i], numpy.sqrt(numpy.sum((data[i][k]-data[j][k])**2)))
                # for k in range(len(data[i])):
                #     tmp += (data[i][k] - data[j][k]) ** 2
                # dists[i] = min(tmp ** 0.5, dists[i])

print 'time cost : %f' %(time.clock() - begin)

# print dists
auc = roc_auc_score(labels, dists.values())
if auc < 0.5:
    auc = 1-auc

print auc