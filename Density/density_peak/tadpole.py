#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 10:53:00 2017

@author: ao
"""

from numpy import zeros, array, argsort
from distance import fast_dtw
from distance import lb_keogh
from math import ceil


def tadpole(data, dist_cutoff = 8, K = 2, band = 3):
    
    n = len(data)
    
    if band < 1:
        band = int(ceil(band*n))

    lb_matrix = zeros((n, n))
    up_matrix = zeros((n, n))
    dist_matrix = zeros((n, n))
    
    # find lower matrix
    for i in range(n):
        for j in range(i):
            lb_matrix[i, j] = max(lb_keogh(data[i], data[j]), lb_keogh(data[i], data[j]))
            lb_matrix[j ,i] = lb_matrix[i, j]
    
    
    # find upper matrix
    for i in range(n):
        for j in range(i):
            up_matrix[i, j] = (sum((data[i]-data[j])**2))**0.5
            up_matrix[j, i] = up_matrix[i, j]
            
    
    #find local density
    densityVector = array([0]*n)
    for i in range(n):
        for j in range(n):
            if i == j: # identical node
                continue
            
            if lb_matrix[i, j] > dist_cutoff:
                continue
            
            if up_matrix[i, j] < dist_cutoff:
                densityVector[i] += 1
                continue
            
            if lb_matrix[i, j] <= dist_cutoff and lb_matrix[i, j] > dist_cutoff:
                dist_matrix[i, j] = fast_dtw(data[i], data[j], band)
                if dist_matrix[i, j] < dist_cutoff:
                    densityVector[i] += 1
    
    sortedIndex = argsort(-densityVector)
    
    #find the up bounds the nn distance of higher local density
    up_bounds = array([float('inf')]*n)
    up_bounds[sortedIndex[0]] = 0.0
    densityList = {}
    for i in range(1, n):
        densityList[sortedIndex[i]] = sortedIndex[:i]
        for j in densityList[sortedIndex[i]]:
            if lb_matrix[sortedIndex[i], j] > up_bounds[sortedIndex[i]]:
                continue
            if dist_matrix[sortedIndex[i], j] != 0:
                if dist_matrix[sortedIndex[i], j] < up_bounds[sortedIndex[i]]:
                    up_bounds[sortedIndex[i]] = dist_matrix[sortedIndex[i], j]
            else:
                if up_matrix[sortedIndex[i], j] < up_bounds[sortedIndex[i]]:
                    up_bounds[sortedIndex[i]] = up_matrix[sortedIndex[i], j]
    
    #up_bounds[sortedIndex[0]] = max(up_bounds)
    
    
    #find the nn distance of higher local density
    distanceVector = array([0.0]*n)
    nnVector = array([0]*n)
    for i in range(1, n):
        min_dist, min_index = float('inf'), -1
        for j in densityList[sortedIndex[i]]:
            if lb_matrix[sortedIndex[i], j] > up_bounds[sortedIndex[i]]:
                continue
            if dist_matrix[sortedIndex[i], j] != 0:
                if dist_matrix[sortedIndex[i], j] < min_dist:
                    min_dist = dist_matrix[sortedIndex[i], j]
                    min_index = j
            else:
                dist_matrix[sortedIndex[i], j] = fast_dtw(data[sortedIndex[i]], data[j], band)
                if dist_matrix[sortedIndex[i], j] < min_dist:
                    min_dist = dist_matrix[sortedIndex[i], j]
                    min_index = j
        
        distanceVector[sortedIndex[i]] = min_dist
        nnVector[sortedIndex[i]] = min_index
                    
    distanceVector[sortedIndex[0]] = max(distanceVector)
    
    #calculating the multiply of the local density and nn distance
    density_dist = argsort(-(densityVector*distanceVector))
    
    clusters = array([-1]*n)
    for i in range(K):
        clusters[density_dist[i]] = i
    
    for i in range(n):
        if clusters[sortedIndex[i]] == -1:
            clusters[sortedIndex[i]] = clusters[nnVector[sortedIndex[i]]]

    return clusters

#import time
#import scipy.io as sio
#begin = time.clock()
#
#data = sio.loadmat('PulsusData.mat')['PulsusData'][:20]
#labels = sio.loadmat('PulsusLabels.mat')['labels'][0]
#
#clusters = tadpole(data)