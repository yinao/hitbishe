# !/usr/bin/env python
# -*-coding:utf-8-*-

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


class SCiForest(object):

    def __init__(self):
        self.__hlimit = -1
        self.__treeNum = -1
        self.__attr = -1
        self.__trees = list()
        self.__sattrs = 2

    def setup(self, attr, tree_num = 25, hlimit = 6, sample_attrs = 3):
        self.__attr = attr
        self.__hlimit = hlimit
        self.__treeNum = tree_num
        self.__sattrs = sample_attrs

    def build(self, data):
        i = 0
        while i < self.__treeNum:
            sdata = sample(data, 256)
            tree = self.__build_tree(sdata, 0, self.__hlimit)
            self.__trees.append(tree)
            i += 1

    def __build_tree(self, data, curh, hlimit):
        if len(data) < 2 or curh >= hlimit:
            node = treeNode()
            node.external = True
            node.size = len(data)
            return node
        index = sample(range(len(data[0])), self.__sattrs)
        weight = [uniform(-1,1) for _ in range(self.__sattrs+1)]
        left_data, right_data = self.__filter(data, index, weight)
        node = treeNode()
        node.size = len(data)
        node.index = index
        node.plane = weight
        node.left = self.__build_tree(left_data, curh+1, hlimit)
        node.right = self.__build_tree(right_data, curh+1, hlimit)
        return node

    def __filter(self, data, index, weight):
        left, right = [],[]
        for item in data:
            sf = weight[0]
            for i in range(self.__sattrs+1):
                sf += item[index[i-1]] * weight[i]
            if sf < 0:
                left.append(item)
            else:
                right.append(item)
        return left, right

    def evaluate(self, data, hlimit=6):
        scores = list()
        for item in data:
            score = 0
            for tree in self.__trees:
                score += self.__score(tree, item, 0, hlimit)
                # score += self.__score(tree, item, 0, hlimit) * 1.0 / tree.size
            # scores.append( 1-2 ** (-1.0*score/self.__treeNum))
            scores.append(score)
        return scores

    def __score(self, node, instance, curH, hlimit):
        if node.external is True or curH >= hlimit:
            return node.size * (2**curH)
        else:
            value = node.plane[0]
            for i in range(len(node.index)):
                value += node.index[i] * node.plane[i + 1]
            if value < 0:
                return self.__score(node.left, instance, curH+1, hlimit)
            else:
                return self.__score(node.right, instance, curH+1, hlimit)

    def testShow(self):
        for itree in self.__trees:
            self.__show(itree)

    def __show(self, node):
        if node is None or node.external is True:
            return
        else:
            print node.size, node.index, node.plane
            self.__show(node.left)
            self.__show(node.right)