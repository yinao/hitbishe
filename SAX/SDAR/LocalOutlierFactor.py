# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics import roc_auc_score


def find_kdist(d_matrix, k=5):
    rows, cols = d_matrix.shape
    d_ndist = numpy.arange(rows)
    d_n = numpy.zeros((rows, k), dtype='int')
    for r in range(rows):
        if r > k:
            d_n[r] = numpy.arange(k)
        else:
            d_n[r] = numpy.append(numpy.arange(r), numpy.arange(r+1, k+1))
        tmp = sorted(d_matrix[r, d_n[r]])
        for c in range(cols):
            if r == c:
                continue
            i = k-2
            while i >= 0 and d_matrix[r, c] < tmp[i]:
                tmp[i+1] = tmp[i]
                d_n[r, i+1] = d_n[r, i]
                i -= 1
            if i != k-2:
                d_n[r, i + 1] = c
                tmp[i+1] = d_matrix[r, c]
        d_ndist[r] = tmp[-1]
    return d_ndist, d_n


def reach_distance(d_nlist, d_matrix):
    rows = d_nlist.shape[0]
    rd_matrix = numpy.zeros((rows, rows))
    for i in range(rows):
        for j in range(rows):
            if i == j:
                continue
            else:
                rd_matrix[i, j] = max(d_nlist[j], d_matrix[i, j])
    return rd_matrix


def lr_density(d_n, rd_matrix):
    rows = d_n.shape[0]
    lrd = numpy.zeros(rows)
    for i in range(rows):
        lrd[i] = len(d_n[i])*1.0 / sum(rd_matrix[i, d_n[i]])
    return lrd


def lo_factor(d_n, lr_vector):
    rows, cols = d_n.shape
    lof = numpy.zeros(rows)
    for i in range(rows):
        lof[i] = sum(lr_vector[d_n[i]])*1.0 / (cols*lr_vector[i])
    return lof

if __name__ == '__main__':
    data_file = '../dataSets/wine'
    data_set = numpy.loadtxt(data_file, delimiter=',')
    labels = numpy.array(data_set[:, 0], dtype='int')
    data_set = numpy.delete(data_set[:, 1:], 0, axis=1)

    # data_set = numpy.loadtxt('../SAX/dataSets/egg13.txt')
    # labels = numpy.loadtxt('../SAX/dataSets/label13.txt', dtype='int')
    # data_set = data_set[100:150]
    # labels = labels[100:150]

    data = numpy.loadtxt('../dataSets/handoutlines', delimiter=',')
    labels = data[:, 0]
    data = data[:, 1:]

    dist_matrix = euclidean_distances(data[:, 1:])
    print dist_matrix
    exit()

    d_nlist, d_n = find_kdist(dist_matrix)
    rd_matrix = reach_distance(d_nlist, dist_matrix)
    lr_vector = lr_density(d_n, rd_matrix)
    lof = lo_factor(d_n, lr_vector)

    auc = roc_auc_score(labels, lof)

    if auc < 0.5:
        print 1-auc
    else:
        print auc


