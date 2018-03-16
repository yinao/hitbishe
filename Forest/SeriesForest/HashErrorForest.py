# !/usr/bin/env python
# -*-coding:utf-8-*-


import numpy
import random
import math


class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.begin = 0
        self.len = 0
        self.size = 0
        self.error_point = 0
        self.weight = None
        self.external = False


class ErrorForest:
    def __init__(self):
        self.h = 5
        self.sample_size = 50
        self.tree_size = 5
        self.node_size = 10
        self.forest = list()

    def setup(self, sample_size=100, tree_size=40, node_size=15, k=35):
        self.sample_size = sample_size
        self.tree_size = tree_size
        self.node_size = node_size
        self.h = k

    def build(self, data):
        rows, cols = data.shape
        row_index = [i for i in range(rows)]
        for _ in range(self.tree_size):
            s_len = numpy.random.randint(int(cols**0.25), int(cols**0.75))
            begin_point = numpy.random.randint(0, cols-s_len)
            s_index = random.sample(row_index, self.sample_size)
            tree = self.build_tree(data[s_index, :], begin_point, s_len, 0, 15)
            self.forest.append(tree)

    def build_tree(self, data, b_p, s_l, cur, hlimit):
        rows, cols = data.shape
        if rows < self.node_size or cur >= hlimit:
            node = Node()
            node.size = rows
            node.external = True
            return node
        node = Node()
        node.begin = b_p
        node.len = s_l
        node.size = rows
        node.weight = numpy.zeros((self.h, s_l))
        for i in range(self.h):
            node.weight[i] = numpy.random.randn(s_l)

        error = list()
        for i in range(rows):
            diff = 0
            r_mean = data[i, b_p:b_p+s_l].mean()
            for k in range(self.h):
                diff += abs((data[i, b_p:b_p+s_l]*node.weight[k]).mean()-r_mean*node.weight[k].mean())
            error.append(diff/self.h)

        node.split = (max(error)+min(error))/2
        l_index, r_index = list(), list()
        for i in range(rows):
            if error[i] < node.split:
                l_index.append(i)
            else:
                r_index.append(i)
        node.left = self.build_tree(data[l_index, :], b_p, s_l, cur+1, hlimit)
        node.right = self.build_tree(data[r_index, :], b_p, s_l, cur+1, hlimit)
        return node

    def evaluation(self, data, hlimit):
        rows, cols = data.shape
        scores = list()
        for i in range(rows):
            score = 0
            for root in self.forest:
                score += self.score(root, data[i, :], 0, hlimit)
            scores.append(score)
        return scores

    def score(self, root, instance, cur, hlimit):
        if root.external is True or cur >= hlimit:
            return math.log(root.size+1, 2)
        diff = 0
        r_mean = instance[root.begin:root.begin+root.len].mean()
        for k in range(self.h):
            diff += abs((instance[root.begin:root.begin+root.len] * root.weight[k]).mean() - r_mean * root.weight[k].mean())
        if diff/self.h < root.split:
            return self.score(root.left, instance, cur+1, hlimit)
        else:
            return self.score(root.right, instance, cur+1, hlimit)
