# !/usr/bin/env python
# -*-coding:utf-8-*-

import random
import numpy
import math
from sklearn.preprocessing import scale


class TreeNode:
    def __init__(self):
        self.weight = []


class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.size = 0
        self.external = False
        self.begin = 0
        self.sub_len = 0
        self.weight = None
        self.merge = None
        self.left_weight = 0
        self.right_weight = 0


class HashForest:
    def __init__(self):
        self.begin_point = 0          # 每个节点的选取的序列的开始点
        self.sub_series_len = 20      # 每个节点的选取的子序列的长度
        self.sample_size = 150        # 每棵模型树的采样大小
        self.node_size = 15           # 每个节点的大小限制
        self.tree_size = 1           # 集成模型中共有多少个模型树
        self.forest = list()
        self.k = 5

    def setup(self, sample_size, node_size=15, tree_size=5, k=5):
        self.sample_size = sample_size
        self.node_size = node_size
        self.tree_size = tree_size
        self.k = 5

    def build(self, data):
        rows, cols = data.shape
        rows_index = [i for i in range(rows)]
        for _ in range(self.tree_size):
            sample_index = random.sample(rows_index, min(rows, self.sample_size))
            sample_attr_len = random.randint(10, cols/3)
            tree = self.build_tree(data[sample_index, :],
                                   self.k,
                                   sample_attr_len,
                                   0, 8)
            self.forest.append(tree)

    def build_tree(self, data, k, s_a_l, cur, hlimit):
        rows, cols = data.shape
        if rows <= self.node_size or cur >= hlimit:
            node = Node()
            node.external = True
            node.size = rows
            return node
        node = Node()
        node.size = rows
        node.sub_len = s_a_l
        node.begin = random.randint(0, cols-s_a_l-1)
        node.weight = numpy.empty((k, s_a_l))
        for i in range(k):
            node.weight[i] = numpy.random.normal(0, 1.0/s_a_l**0.5, s_a_l)
        node.merge = numpy.random.normal(0, 1.0/k**.5, k)
        left_index, right_index = [], []
        result = numpy.zeros(k)
        for i in range(rows):
            for j in range(k):
                result[j] = sum(node.weight[j]*data[i, node.begin:node.begin+node.sub_len])
            if sum(result*node.merge) < 0:
                left_index.append(i)
            else:
                right_index.append(i)
        node.left = self.build_tree(data[left_index, :], k, s_a_l, cur+1, hlimit)
        node.right = self.build_tree(data[right_index, :], k, s_a_l, cur+1, hlimit)
        return node

    def evaluation(self, data, hlimit):
        rows, cols = data.shape
        scores = list()
        for i in range(rows):
            score = 0
            for root in self.forest:
                score += self.score(root, scale(data[i, :]), 0, hlimit, 1)
            scores.append(score)
        return scores

    def score(self, root, instance, cur, hlimit, prob):
        if root.external is True or cur >= hlimit:
            return math.log(root.size+1, 2)-math.log(self.sample_size, 2)
        result = list()
        for i in range(self.k):
            result.append(sum(instance[root.begin:root.begin+root.sub_len] * root.weight[i]))
        if sum(root.merge*numpy.array(result)) < 0:
            return self.score(root.left, instance, cur+1, hlimit, root.left_weight*prob)
        else:
            return self.score(root.right, instance, cur+1, hlimit, root.right_weight*prob)
