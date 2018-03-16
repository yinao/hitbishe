# !/usr/bin/env python
# -*-coding:utf-8-*-

from math import log, e
from numpy import array
from random import sample, uniform
from numpy.random import randint


class treeNode:
    def __init__(self):
        self.l_split = 0
        self.m_split = 0
        self.r_split = 0
        self.index = -1
        self.left = None
        self.m_left = None
        self.m_right = None
        self.right = None
        self.height = 0
        self.size = 0
        self.external = False


class FBForest:

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
        node.l_split = mean-2*std
        node.r_split = mean + 2 * std
        node.m_split = uniform(node.l_split, node.r_split)
        left, middle_left, middle_right, right = self.__filter(data, index, node.l_split, node.m_split, node.r_split)
        node.left = self.__build_tree(left, curh+1)
        node.m_left = self.__build_tree(middle_left, curh+1)
        node.m_right = self.__build_tree(middle_right, curh+1)
        node.right = self.__build_tree(right, curh+1)
        return node

    def __filter(self, data, index, left_split, middle_split, right_split):
        left, middle_left, middle_right, right = [], [], [], []
        for i in range(len(data)):
            if data[i][index] < left_split:
                left.append(data[i])
            elif data[i][index] <= middle_split:
                middle_left.append(data[i])
            elif data[i][index] <= right_split:
                middle_right.append(data[i])
            else:
                right.append(data[i])
        return array(left), array(middle_left), array(middle_right), array(right)

    def evaluate(self, data, hlimit=2):
        scores = list()
        for item in data:
            tmp = 0
            for tree in self.__trees:
                tmp += self.__score(item, tree, 0, hlimit)
            scores.append(tmp/self.__tree_num)
            # scores.append( 1-2 ** (-1.0*tmp/self.__tree_num/self.__sample_size))
            # scores.append(1 - 2 ** (-(1.0*tmp / self.__tree_num / self.__cost(self.__sample_size-1))))
        return scores

    def __score(self, instance, tree, curh, hlimit):
        if tree.external is True or curh >= hlimit:
            return tree.size * (2**curh)
            # return curh + self.__cost(tree.size-1)
        if instance[tree.index] < tree.l_split:
            return self.__score(instance, tree.left, curh+self.__less_height, hlimit)
        elif instance[tree.index] <= tree.m_split:
            return self.__score(instance, tree.m_left, curh+self.__much_height, hlimit)
        elif instance[tree.index] <= tree.r_split:
            return self.__score(instance, tree.m_right, curh+self.__much_height, hlimit)
        else:
            return self.__score(instance, tree.right, curh+self.__less_height, hlimit)

    def __cost(self, size):
        if size == 2:
            return 1
        elif size < 2:
            return 0
        else:
            return  3*size - log(size, e)
            # return 3*size + 3.5 - log(size, e) - 0.577215

    def showTreeStructure(self):
        self.__show(self.__trees[0])

    def __show(self, tree):
        if tree is None:
            return
        print tree.size
        self.__show(tree.left)
        self.__show(tree.middle)
        self.__show(tree.right)