# !/usr/bin/env python
# -*-coding:utf-8-*-

import random
import numpy
from sklearn.preprocessing import scale


class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.size = 0
        self.external = False
        self.begin = 0
        self.sub_len = 0
        self.left_weight = 0
        self.right_weight = 0


class SeriesForest:
    def __init__(self):
        self.begin_point = 0
        self.sub_series_len = 20
        self.sample_size = 150
        self.node_size = 15
        self.tree_size = 10
        self.forest = list()

    def setup(self):
        pass

    def build(self, data):
        rows, cols = data.shape
        rows_array = [i for i in range(rows)]
        # s_size = self.sample_size
        for _ in range(self.tree_size):
            # 获得采样大小，随机选取属性长度，
            sample_rows = random.sample(rows_array, self.sample_size)
            sub_len = 15  # random.randint(0, cols-)
            # begin_point = random.randint(0, cols-sub_len-1)
            root = self.build_tree(data[sample_rows, :], sub_len)
            self.forest.append(root)

    def build_tree(self, data, sub_len):
        rows, cols = data.shape
        if rows < self.node_size:
            node = Node()
            node.external = True
            node.size = rows
            return node
        begin_point = random.randint(0, cols-sub_len-1)
        node = Node()
        node.size = rows
        node.begin = begin_point
        node.sub_len = sub_len
        node.left_weight = 0
        node.right_weight = 0
        left_data, right_data = list(), list()
        for i in range(rows):
            d = data[i, :]
            d = scale(d)
            u = d.mean()
            l, r = 0, 0
            for j in range(begin_point, begin_point+sub_len):
                if d[j] < u:
                    l += 1
                else:
                    r += 1
            if l < r:
                left_data.append(i)
            else:
                right_data.append(i)
            node.left_weight += l*1.0 / (l+r)
        node.left_weight /= rows
        node.right_weight = 1 - node.left_weight
        node.left = self.build_tree(data[left_data, :], sub_len)
        node.right = self.build_tree(data[right_data, :], sub_len)
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
        if root.external is True:# or cur >= hlimit:
            return root.size * prob
        l, r = 0, 0
        u = instance.mean()
        for i in range(root.begin, root.begin+root.sub_len):
            if instance[i] < u:
                l += 1
            else:
                r += 1
        if l > r:
            return self.score(root.left, instance, cur+1, hlimit, root.left_weight*prob)
        else:
            return self.score(root.right, instance, cur+1, hlimit, root.right_weight*prob)
