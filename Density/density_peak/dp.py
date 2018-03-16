#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 19:58:23 2017

@author: ao
"""

from numpy import argsort, array, argwhere, argmin, zeros
from distance import fast_dtw
from math import ceil

_n = -1

def _findLocalDensity(distanceMatrix, threshold):
    
    global _n
    
    density = array([0]*_n)
    
    for i in range(_n):
        for j in range(_n):
            if i != j and distanceMatrix[i, j] < threshold:
                density[i] += 1
    
    return density


def _findDistanceVector(distanceMatrix, pSortedIndex):
    
    global _n
    distanceVector = array([0.0]*_n)
    for j in range(0, _n):
        if j == pSortedIndex[0]:
            continue
        
        distanceVector[j] = min(distanceMatrix[j, pSortedIndex[:argwhere(pSortedIndex == j)[0][0]]])
        
    distanceVector[pSortedIndex[0]] = max(distanceVector)
    
    return distanceVector

def _clusterAssignment(clusterCenter, distanceMatrix, pSortedIndex):
    global _n
    
    #print clusterCenter
    clusters = array([-1]*_n)
    for i in range(len(clusterCenter)):
        clusters[clusterCenter[i]] = i
    
    for i in range(_n):
        if clusters[pSortedIndex[i]] == -1:            
            indexList = pSortedIndex[:i]
            clusters[pSortedIndex[i]] = clusters[indexList[argmin(distanceMatrix[pSortedIndex[i], indexList])]]
    
    return clusters
    

def density_peak(data, dist_cutoff=0.03, K=2, band=0.3):
    
    global _n
    _n = len(data)
    if band < 1:
        band = int(ceil(_n*band))
    
    #distanceMatrix = euclidean_distances(data, data)
    distanceMatrix = zeros((_n, _n))
    for i in range(_n):
        for j in range(i):
            if i == j:
                continue
            distanceMatrix[i, j] = fast_dtw(data[i], data[j], band)
            distanceMatrix[j, i] = distanceMatrix[i, j]
    
    pVector = _findLocalDensity(distanceMatrix, dist_cutoff)
    
    pSortedIndex = argsort(-pVector)
    
    distanceVector = _findDistanceVector(distanceMatrix, pSortedIndex)
        
    clusters = _clusterAssignment(argsort(-(pVector*distanceVector))[:K], distanceMatrix, pSortedIndex)
    
    return clusters
    
#import scipy.io as sio
#
#data = sio.loadmat('PulsusData.mat')['PulsusData']
#    
#begin = time.clock()
#clusters = density_peak(data, 5) + 1
#
##print clusters
#
#labels = sio.loadmat('PulsusLabels.mat')['labels'][0]
#
#
#print 'adjusted rand score: %s' %adjusted_rand_score(clusters, labels)
#right, wrong = 0, 0
#for i in range(len(clusters)):
#    if clusters[i] == labels[i]:
#        right += 1
#    else:
#        wrong += 1
#
#print right, wrong
#
#print 'cost time:  %s' % (time.clock() - begin)
