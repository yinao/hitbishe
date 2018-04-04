# !/usr/bin/env python
# -*-coding:utf-8-*-

import math
from Queue import Queue
from random import randint, uniform
from numpy.random import randn

class treeNode:
    def __init__(self):
        self.left = None
        self.right = None
        self.parent = None
        self.ratio = 0
        self.profile = 0
        self.leaf = False
        self.index = 0
        self.value = 0


class RS_Forest(object):
    def __init__(self):
        self.__attr = -1
        self.__treeNum = -1
        self.__hlimit = -1
        self.__trees = list()
        self.__instances = 1200

    def setup(self, attr, treeNum = 25, hlimit = 6):
        self.__attr = attr
        self.__treeNum = treeNum
        self.__hlimit = hlimit

    def obtainRange(self, size = 1000):
        ## 百分之90的置信区间
        lowers, uppers = [], []
        sample = randn(size, self.__attr)
        low = 0.005
        for i in range(self.__attr):
            tmp = sorted(sample[:,i])
            lowers.append(tmp[int(size*low)])
            uppers.append(tmp[int(size*(1-low))])
        return sample, lowers, uppers


    def buildModel(self):
        assert (self.__attr > 2), "attributes number is too less"
        assert (self.__treeNum > 0), "tree number is too less"
        assert (self.__hlimit > 0), "tree height limit is too less"

        sample, lowers, uppers = self.obtainRange(self.__instances)
        i = 0
        while i < self.__treeNum:
            tree = self.__buildTree(lowers, uppers, 0, self.__hlimit)
            self.__computeNodeVol(tree)
            self.__initTreeProfile(sample, tree)
            self.__trees.append(tree)
            i += 1


    def __buildTree(self, lowers, uppers, curH, hlimit):
        if curH >= hlimit:
            node = treeNode()
            node.leaf = True
            return node
        node = treeNode()
        splitIndex = randint(0, self.__attr-1)
        randomRatio = uniform(0, 1)
        splitValue = lowers[splitIndex] + randomRatio*(uppers[splitIndex] - lowers[splitIndex])

        tmp = uppers[splitIndex]
        uppers[splitIndex] = splitValue
        left = self.__buildTree(lowers, uppers, curH+1, hlimit)
        left.ratio = randomRatio
        left.parent = node

        uppers[splitIndex] = tmp
        lowers[splitIndex] = splitValue
        right = self.__buildTree(lowers, uppers, curH+1, hlimit)
        right.ratio = 1 - randomRatio
        right.parent = node

        node.index = splitIndex
        node.value = splitValue
        node.left = left
        node.right = right
        return node

    def __computeNodeVol(self, root):
        queue = Queue()
        queue.put(root)
        while queue.empty() is False:
            curNode = queue.get()
            parentNode = curNode.parent
            if parentNode is None:
                curNode.ratio = 0
            else:
                curNode.ratio = parentNode.ratio + math.log(curNode.ratio)

            if curNode.leaf is False:
                queue.put(curNode.left)
                queue.put(curNode.right)

    def __initTreeProfile(self, data, tree):
        for item in data:
            self.__updateProfile(tree, item)

    def __updateProfile(self, node, instance):
        if node.leaf is True:
            node.profile += 1
            return
        node.profile += 1
        if node.value < instance[node.index]:
            return self.__updateProfile(node.left, instance)
        else:
            return self.__updateProfile(node.right, instance)

    def initModel(self, data):
        for item in data:
            for tree in self.__trees:
                self.__initProfile(tree, item)

    def __initProfile(self, node, instance):
        if node is None:
            return
        node.profile += 1
        if node.value < instance[node.index]:
            return self.__initProfile(node.left, instance)
        else:
            return self.__initProfile(node.right, instance)

    def evaluate(self, data, hlimit = 6):
        scores = []
        for item in data:
            tmp = 0
            for tree in self.__trees:
                tmp += self.score(item, tree, 0, hlimit)
            scores.append(tmp / self.__treeNum)
        return scores

    def score(self, instance, tree, h, hlimit):
        if tree.leaf is True:
            if tree.profile <= 0:
                return math.e ** (-tree.ratio-math.log(self.__instances))
            else:
                return math.e ** (math.log(tree.profile) - tree.ratio- math.log(self.__instances))
        if tree.value < instance[tree.index]:
            return self.score(instance, tree.left, h+1, hlimit)
        else:
            return self.score(instance, tree.right, h+1, hlimit)

    def testTreeStructure(self):
        self.__show(self.__trees[0])

    def __show(self, root):
        if root is None or root.leaf is True:
            return
        else:
            print root.profile
            self.__show(root.left)
            self.__show(root.right)
