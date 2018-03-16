# !/usr/bin/env python
# -*-coding:utf-8-*-

import math
from random import uniform, sample
from numpy.random import rand, randn

class treeNode:
    def __init__(self):
        self.size = 0
        self.left = None
        self.right = None
        self.index = []
        self.plane = []
        self.split = 0
        self.external = False


class MAiForest(object):

    def __init__(self):
        self.__hlimit = -1
        self.__treeNum = -1
        self.__attr = -1
        self.__trees = list()
        self.__sattrs = 2
        self.__planes = 1

    def setup(self, attr, tree_num = 25, hlimit = 6, sample_attrs = 2, planes = 2):
        self.__attr = attr
        self.__hlimit = hlimit
        self.__treeNum = tree_num
        self.__sattrs = sample_attrs
        self.__planes = planes

    def build(self):
        assert (self.__attr > 1), 'attributes number is too less'
        assert (self.__hlimit > 1), "tree height limit is too less"
        assert (self.__treeNum >= 1), 'tree nums is too less'

        # lowers = list()
        # uppers = list()
        # for i in range(self.__attr):
        #     sq = rand()
        #     lowers.append(sq - 2*max(sq, 1-sq))
        #     uppers.append(sq + 2*max(sq, 1-sq))

        lowers, uppers = [], []
        size = 1000
        sample = randn(size, self.__attr)
        # print sample
        low = 0.005
        for i in range(self.__attr):
            tmp = sorted(sample[:, i])
            lowers.append(tmp[int(size * low)])
            uppers.append(tmp[int(size * (1 - low))])

        i = 0
        while i < self.__treeNum:
            tree = self.__buildTree(lowers, uppers, 0)
            # self.__initM(sample, tree)
            self.__trees.append(tree)
            i+=1

    def __buildTree(self, lowers, uppers, curH):
        if curH == self.__hlimit:
            node = treeNode()
            node.external = True
            return node
        index = sample(range(0, self.__attr), self.__sattrs)
        values = [(lowers[i] + uppers[i])/2 for i in index]
        # values = [uniform(lowers[i], uppers[i]) for i in index]
        node = treeNode()
        node.index = index
        plane, split = self.__hyperplane(index, lowers, uppers, values)
        node.plane = plane
        node.split = split#-(sum(values) / len(values))
        for i in range(self.__sattrs):
            uppers[index[i]] = values[i]
        node.left = self.__buildTree(lowers, uppers, curH+1)
        for i in range(self.__sattrs):
            lowers[index[i]] = values[i]
        node.right = self.__buildTree(lowers, uppers, curH+1)
        return node

    def __hyperplane(self, index, lowers, uppers, values):
        i = 0
        weight = []
        gain = -float('inf')
        splits = []
        while i < self.__planes:
            weight = [uniform(0,1) for _ in range(self.__attr)]
            tmp = 0
            for j in range(len(values)):
                tmp += values[j]*weight[j]
            splits.append(tmp)
            i += 1
        gain = sum(splits) / len(splits)
        return weight, gain

    def init(self, data, s_size = 256):
        # print data
        for tree in self.__trees:
            for item in sample(data, s_size):
                self.__updateMass(item, tree)

    def __initM(self, data, tree):
        for item in data:
            self.__updateMass(item, tree)

    def __updateMass(self, x, node):
        if node is None:
            return
        node.size += 1
        if node.external is True:
            return
        value = -node.split
        weights = node.plane
        # weights = [uniform(0, 1) for _ in range(self.__sattrs)]
        # print node.index
        for i in range(len(node.index)):
            value += x[node.index[i]] * weights[i]
        # print value, node.index, x
        if value < 0:
            self.__updateMass(x, node.left)
        else:
            self.__updateMass(x, node.right)

    def evaluate(self, data, hlimit=1):
        scores = list()
        for item in data:
            score = 0
            for tree in self.__trees:
                # score += self.__score(tree, item, 0, hlimit)
                score += self.__score(tree, item, 0, hlimit) * 1.0 / tree.size
            scores.append( 1-2 ** (-1.0*score/self.__treeNum))
            # scores.append(score)
        return scores

    def __score(self, node, instance, curH, hlimit):
        if node.external is True or node.size <= hlimit:
            return node.size * (2**curH)
        else:
            value = -node.split
            weights = node.plane
            # weights = [uniform(0, 1) for _ in range(self.__sattrs)]
            for i in range(len(node.index)):
                value += instance[node.index[i]] * weights[i]
            if value < 0:
                return self.__score(node.left, instance, curH+1, hlimit)
            else:
                return self.__score(node.right, instance, curH+1, hlimit)

    def testShow(self):
        self.__show(self.__trees[0])

    def __show(self, node):
        if node is None or node.external is True:
            return
        else:
            print node.size, node.index, node.plane
            self.__show(node.left)
            self.__show(node.right)