# !/usr/bin/env python
# -*-coding:utf-8-*-

from math import log, e
from numpy import array
from random import sample
from numpy.random import randint


class treeNode:
    def __init__(self):
        self.lsplit = 0
        self.rsplit = 0
        self.index = -1
        self.left = None
        self.right = None
        self.middle = None
        self.height = -1
        self.size = 0
        self.external = False


class MBForest:

    def __init__(self):
        self.__tree_num = 1
        self.__size_limit = 1
        self.__sample_size = 128
        self.__trees = list()
        self.__height_limit = 8
        self.__less_height = 0.8
        self.__much_height = 1

    def setup(self, tree_num, size_limit = 1, sample_size = 64, height_limit = 8, less_height=0.8, much_height=1):
        self.__tree_num = tree_num
        self.__size_limit = size_limit
        self.__sample_size = sample_size
        self.__height_limit = height_limit
        self.__less_height = less_height
        self.__much_height = much_height

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
        index = randint(cols)
        mean = data[:, index].mean()
        std = data[:, index].std()
        node = treeNode()
        node.index = index
        node.size = rows
        node.lsplit = mean-1.645*std
        node.rsplit = mean+1.645*std
        left, middle, right = self.__filter(data, index, node.lsplit, node.rsplit)
        node.left = self.__build_tree(left, curh+1)
        node.middle = self.__build_tree(middle, curh+1)
        node.right = self.__build_tree(right, curh+1)
        return node

    def __filter(self, data, index, left_split, right_split):
        left, middle, right = [], [], []
        for i in range(len(data)):
            if data[i][index] < left_split:
                left.append(data[i])
            elif data[i][index] > right_split:
                right.append(data[i])
            else:
                middle.append(data[i])
        return array(left), array(middle), array(right)

    def evaluate(self, data, hlimit=4):
        scores = list()
        for item in data:
            tmp = 0
            for tree in self.__trees:
                tmp += self.__score(item, tree, 0, hlimit)
                # tmp += self.__score(item, tree, 0, hlimit)
            # scores.append(tmp/self.__tree_num)
            # scores.append( 1-2 ** (-1.0*tmp/self.__tree_num/self.__sample_size))
            scores.append(1 - 2 ** (-(1.0*tmp / self.__tree_num / self.__cost(self.__sample_size-1))))
        return scores

    def __score(self, instance, tree, curh, hlimit):
        if tree.external is True or curh >= hlimit:
            # return tree.size * (2**curh)
            return curh + self.__cost(tree.size-1)
        if instance[tree.index] < tree.lsplit:
            return self.__score(instance, tree.left, curh+self.__less_height, hlimit)
        elif instance[tree.index] > tree.rsplit:
            return self.__score(instance, tree.right, curh+self.__much_height, hlimit)
        else:
            return self.__score(instance, tree.middle, curh+self.__less_height, hlimit)

    def __cost(self, size):
        if size == 2:
            return 1
        elif size < 2:
            return 0
        else:
            return  3*size - log(size, e)
            # return 3*size + 3.5 - log(size, e) - 0.577215
            #return 2 * log(size - 1) - float(2 * (size - 1)) / size

    def density_evaluate(self, data, hlimit=4):
        scores = list()
        for item in data:
            tmp = 0
            for tree in self.__trees:
                tmp += self.__score(item, tree, 0, hlimit)
            # scores.append(tmp/self.__tree_num)
            # scores.append( 1-2 ** (-1.0*tmp/self.__tree_num/self.__sample_size))
            scores.append(tmp)
        return scores

    def __score(self, instance, tree, curh, hlimit):
        if tree.external is True or curh >= hlimit:
            return tree.size * (2**curh)
        if instance[tree.index] < tree.lsplit:
            return self.__score(instance, tree.left, curh+self.__less_height, hlimit)
        elif instance[tree.index] > tree.rsplit:
            return self.__score(instance, tree.right, curh+self.__much_height, hlimit)
        else:
            return self.__score(instance, tree.middle, curh+self.__less_height, hlimit)

    def showTreeStructure(self):
        self.__show(self.__trees[0])

    def __show(self, tree):
        if tree is None:
            return
        print tree.size
        self.__show(tree.left)
        self.__show(tree.middle)
        self.__show(tree.right)