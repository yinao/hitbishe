#!/usr/bin/env python
# -*-coding:utf-8-*-
from random import randint, uniform, sample
from math import log


sampleSize = None
heightLimit = 0
sizeLimit = 8


class TreeNode:
    def __init__(self):
        self.SplitValue = None
        self.SplitAttrIndex = None
        # Instances = None
        self.Size = -1
        self.Left = None
        self.Right = None
        self.external = False


def IsolationForest(dataSets, treeNum, size):
    global sampleSize, heightLimit, sizeLimit
    sampleSize = size
    heightLimit = 6
    Forest = []
    i = 0
    while i < treeNum:
        sampleInstances = sample(dataSets, min(size,len(dataSets)))
        tree = IsolationTree(sampleInstances, sizeLimit, 0, heightLimit)
        Forest.append(tree)
        i += 1
    return Forest

def IsolationTree(sets, limit, cuh, hlimit):
    setsLength = len(sets)
    if setsLength <= limit or cuh >= hlimit:
        node = TreeNode();
        node.Size = setsLength
        node.external = True
        return node
    else:
        attrIndex = randint(0, len(sets[0])-1)
        splitValue = selectSplitPoint(sets, attrIndex)
        left,right = filter(sets, attrIndex, splitValue)
        tNode = TreeNode()
        tNode.SplitValue = splitValue
        tNode.SplitAttrIndex = attrIndex
        tNode.Left = IsolationTree(left, limit, cuh+1, hlimit)
        tNode.Right = IsolationTree(right, limit, cuh+1, hlimit)
        tNode.Size = len(left) + len(right)
        return tNode


def selectSplitPoint(sets, spIndex):
    maxValue = max(sets, key=lambda x :x[spIndex])
    minValue = min(sets, key=lambda x :x[spIndex])
    return uniform(minValue[spIndex], maxValue[spIndex])


def filter(dataSets, splitIndex, splitValue):
    left, right = [], []
    for i in range(len(dataSets)):
        if dataSets[i][splitIndex] < splitValue:
            left.append(dataSets[i])
        else:
            right.append(dataSets[i])
    return (left, right)


def Evaluation(instances, trees, hlimit=6):
    scores = []
    treesNum = len(trees)
    heights = [0] * treesNum
    for instance in instances:
        for i in range(treesNum):
            heights[i] = PathLength(instance, trees[i], 0, hlimit)
        scores.append(1-2**(-(float(sum(heights)) / treesNum / Cost(sampleSize))))
        # scores.append(float(sum(heights)) / treesNum)
    return scores


def PathLength(instance, tree, cPathLen, heightLimit):
    if tree.external is True or cPathLen >= heightLimit:
        return cPathLen + Cost(tree.Size)
    sIndex = tree.SplitAttrIndex
    if instance[sIndex] < tree.SplitValue:
        return PathLength(instance, tree.Left, cPathLen + 1, heightLimit)
    else:
        return PathLength(instance, tree.Right, cPathLen + 1, heightLimit)


def Cost(size):
    if size == 2:
        return 1
    elif size < 2:
        return 0
    else:
        return 2*log(size-1) - float(2*(size-1)) / size

def Show(tree):
    if tree is None:
        print 'is None'
        return None
    print tree.Size
    # Show(tree.Left)
    # Show(tree.Right)
