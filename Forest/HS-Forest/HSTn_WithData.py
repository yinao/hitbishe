# !/usr/bin/env python
# -*-coding:utf-8-*-

from random import sample, randint

class treeNode:
    def __init__(self):
        self.size = 0
        self.left = None
        self.right = None
        self.height = 0
        self.splitIndex = -1
        self.splitValue = 0
        self.external = False

class HS_Forest(object):

    def __init__(self):
        self.__hlimit = -1
        self.__treeNum = -1
        self.__sampleSize = -1
        self.__trees = list()
        self.__attr = -1

    def setup(self, sample_size = 128, tree_num = 25, hlimit = 8):
        self.__sampleSize = sample_size
        self.__hlimit = hlimit
        self.__treeNum = tree_num

    def build(self, data):
        assert (self.__sampleSize > 1), 'attributes number is too less'
        assert (self.__hlimit > 1), "tree height limit is too less"
        assert (self.__treeNum >= 1), 'tree nums is too less'
        assert (len(data) >= self.__sampleSize), 'train data less sample number'

        self.__attr = len(data[0])
        i = 0
        while (i < self.__treeNum):
            tree = self.__buildTree(sample(data, self.__sampleSize), 0)
            self.__trees.append(tree)
            i+=1

    def __buildTree(self, data, curH):
        if curH == self.__hlimit or len(data) < 1:
            node = treeNode()
            node.external = True
            node.size = len(data)
            return node
        node = treeNode()
        node.splitIndex = randint(0, self.__attr-1)
        node.splitValue = self.__split(data, node.splitIndex)
        left, right = self.__filter(data, node.splitIndex, node.splitValue)
        node.left = self.__buildTree(left, curH+1)
        node.right = self.__buildTree(right, curH+1)
        node.size = node.left.size + node.right.size
        return node

    def __split(self, sets, index):
        maxValue = max(sets, key=lambda x: x[index])
        minValue = min(sets, key=lambda x: x[index])
        return (maxValue[index]+minValue[index]) / 2

    def __filter(self, data, index, value):
        left, right = [], []
        for i in range(len(data)):
            if data[i][index] < value:
                left.append(data[i])
            else:
                right.append(data[i])
        return left, right

    def evaluate(self, data, hlimit = 8):
        scores = list()
        i = 0
        for item in data:
            score = 0
            for tree in self.__trees:
                score+= self.__score(tree, item, 0 , hlimit)
            scores.append(score)
            # print score
            # scores.append(1-2**(-score/self.__treeNum))
            # scores.append(2**(-(float(score)/self.__treeNum/self.__sampleSize)))
        return scores

    def __score(self, node, instance, curh, hlimit):
        if node.external is True or curh >= hlimit:
            # return self.__normalization(curh, node.size)
            return node.size * (2**curh)
        else:
            if instance[node.splitIndex] < node.splitValue:
                return self.__score(node.left, instance, curh+1, hlimit)
            else:
                return self.__score(node.right, instance, curh+1, hlimit)

    def __normalization(self, curh, size):
        # print size, self.__sampleSize*(2**-curh)
        return ((size) / (self.__sampleSize*(2**-curh)))