# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy
import random
from math import log
from AutoEncoder import AutoEncoder


class Node:
    def __init__(self):
        self.split = None
        self.left = None
        self.right = None
        self.index = None
        self.weights = None
        self.bias = None
        self.size = -1
        self.external = False


class DLForest:
    def __init__(self):
        self.sample_size = 0
        self.height_limit = 0
        self.leaf_size_limit = 10
        self.attr_sample_size = 1
        self.forest_size_limit = 10
        self.forest = list()
        self.ae = None

    def setup(self, sample_size=128, height_limit=6, leaf_size_limit=10, attr_sample_size=2, forest_size_limit=5):
        self.sample_size = sample_size
        self.height_limit = height_limit
        self.leaf_size_limit = leaf_size_limit
        self.attr_sample_size = attr_sample_size
        self.forest_size_limit = forest_size_limit

    def build(self, data):
        i = 0
        self.ae = AutoEncoder()
        self.ae.init_tf(fin=self.attr_sample_size, fou=1, epochs=10, l_rate=0.01)
        while i < self.forest_size_limit:
            sample_data = numpy.array(random.sample(data, self.sample_size))
            tree = self.build_tree(sample_data, 0)
            self.forest.append(tree)
            i += 1

    def build_tree(self, data, curH):
        rows, cols = data.shape
        if rows <= self.leaf_size_limit or curH >= self.height_limit:
            node = Node()
            node.size = rows
            node.external = True
            return node
        else:
            sample_index = random.sample(range(cols), self.attr_sample_size)
            results = self.ae.get_results(data[:, sample_index])
            node = Node()
            node.index = sample_index
            node.size = rows
            node.weights = results['weights']
            node.bias = results['biases']
            node.split = random.uniform(min(results['inters']), max(results['inters']))
            left, right = self.split_data(results['inters'], node.split)
            node.left = self.build_tree(data[left, :], curH+1)
            node.right = self.build_tree(data[right, :], curH+1)
            return node

    def split_data(self, data, split_point):
        left, right = list(), list()
        for i in range(len(data)):
            if data[i] <= split_point:
                left.append(i)
            else:
                right.append(i)
        return left, right

    def evaluate(self, data, hlimit=6):
        scores = list()
        for item in data:
            score = 0
            for tree in self.forest:
                score += self.path(item, tree, curH=0, hlimit=hlimit)
            score /= self.forest_size_limit
            scores.append(score)
        return scores

    def path(self, instance, tree, curH, hlimit):
        if tree.external is True or curH >= hlimit:
            return curH + self.cost(tree.size)
        tag = sum(instance[tree.index]*tree.weights) + tree.bias
        if tag <= tree.split:
            return self.path(instance, tree.left, curH+1, hlimit)
        else:
            return self.path(instance, tree.right, curH+1, hlimit)

    def cost(self, size):
        if size == 2:
            return 1
        elif size < 2:
            return 0
        else:
            return 2*log(size-1, 2) - float(2*(size-1))/size

    def show(self, tree):
        if tree is None:
            print('is None')
            return None
        print(tree.size)
        self.show(tree.left)
        self.show(tree.right)
