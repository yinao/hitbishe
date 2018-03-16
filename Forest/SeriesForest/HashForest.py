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
            weight = list()
            for i in range(self.k):
                weight.append(numpy.random.normal(0, 1, sample_attr_len))
            tree = self.build_tree(data[sample_index, :],
                                   self.k,
                                   sample_attr_len,
                                   numpy.array(weight),
                                   0,
                                   8)
            self.forest.append(tree)

    def build_tree(self, data, k, s_a_l, factor, cur, hlimit):
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
        node.weight = factor
        left_index, right_index = [], []
        for i in range(rows):
            ones, zeros = 0, 0
            for j in range(k):
                if sum(factor[j]*data[i, node.begin:node.begin+node.sub_len]) < 0:
                    zeros += 1
                else:
                    ones += 1
            if zeros > ones:
                left_index.append(i)
            else:
                right_index.append(i)
        node.left = self.build_tree(data[left_index, :], k, s_a_l, factor, cur+1, hlimit)
        node.right = self.build_tree(data[right_index, :], k, s_a_l, factor, cur+1, hlimit)
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
            return math.log(root.size+1, math.e)
        l, r = 0, 0
        for i in range(self.k):
            if sum(instance[root.begin:root.begin+root.sub_len] * root.weight[i]) < 0:
                l += 1
            else:
                r += 1
        if l > r:
            return self.score(root.left, instance, cur+1, hlimit, root.left_weight*prob)
        else:
            return self.score(root.right, instance, cur+1, hlimit, root.right_weight*prob)