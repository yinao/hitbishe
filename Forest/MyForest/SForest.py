# !/usr/bin/env python
# -*-coding:utf-8-*-

from math import log, e
from numpy import array, median
from random import sample, uniform
from numpy.random import randint


class treeNode:
    def __init__(self):
        self.split = 0
        self.index = None
        self.weight = None
        self.left = None
        self.right = None
        self.height = -1
        self.size = 0
        self.external = False


class SForest:

    def __init__(self):
        self.__tree_num = 1
        self.__size_limit = 1
        self.__sample_size = 128
        self.__trees = list()
        self.__height_limit = 8
        self.__sample_attr = 1

    def setup(self, tree_num, size_limit = 1, sample_size = 64, height_limit = 8, sample_attr = 2):
        self.__tree_num = tree_num
        self.__size_limit = size_limit
        self.__sample_size = sample_size
        self.__height_limit = height_limit
        self.__sample_attr = sample_attr

    def build(self, data):
        i = 0
        while i < self.__tree_num:
            tree = self.__build_tree(array(sample(data, self.__sample_size)), 0)
            self.__trees.append(tree)
            i += 1

    def __build_tree(self, data, curh):
        if len(data) <= self.__size_limit or curh >= self.__height_limit:
            node = treeNode()
            node.size = len(data)
            node.external = True
            return node
        rows, cols = data.shape
        node = treeNode()
        node.index = sample(range(cols), self.__sample_attr)
        node.weight = list()
        values = list()
        for i in node.index:
            node.weight.append(data[:, i].std())
            values.append((min(data[:,i])+max(data[:, i]))/2)
        node.split = 0 #sum(node.weight*array(values))
        # print node.split
        node.size = rows
        left, right = self.__filter(data, node.index, node.weight, node.split)
        node.left = self.__build_tree(left, curh+1)
        node.right = self.__build_tree(right, curh+1)
        return node

    def __filter(self, data, index, weight, split):
        left, right = [], []
        for i in range(len(data)):
            if sum(data[i, index] * weight) < split:
                left.append(data[i,:])
            else:
                right.append(data[i,:])
        return array(left), array(right)

    def evaluate(self, data, hlimit=4):
        scores = list()
        for item in data:
            tmp = 0
            for tree in self.__trees:
                tmp += self.__score(item, tree, 0, hlimit)
                # tmp += self.__score(item, tree, 0, hlimit)
            scores.append(tmp/self.__tree_num)
            # scores.append( 1-2 ** (-1.0*tmp/self.__tree_num/self.__sample_size))
            # scores.append(1 - 2 ** (-(1.0*tmp / self.__tree_num / self.__cost(self.__sample_size-1))))
        return scores

    def __score(self, instance, tree, curh, hlimit):
        if tree.external is True or curh >= hlimit:
            return tree.size * (2**curh)
            # return curh + self.__cost(tree.size-1)
        if sum(instance[tree.index] * tree.weight) < tree.split:
            return self.__score(instance, tree.left, curh+1, hlimit)
        else:
            return self.__score(instance, tree.right, curh+1, hlimit)

    def __cost(self, size):
        if size == 2:
            return 1
        elif size < 2:
            return 0
        else:
            # return  3*size - log(size, e)
            # return 3*size + 3.5 - log(size, e) - 0.577215
            return 2 * log(size - 1) - float(2 * (size - 1)) / size

    def showTreeStructure(self):
        self.__show(self.__trees[0])

    def __show(self, tree):
        if tree is None:
            return
        print tree.size
        self.__show(tree.left)
        self.__show(tree.middle)
        self.__show(tree.right)