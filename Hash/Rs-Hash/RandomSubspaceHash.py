# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy
from Detector import Detector
from math import log, floor
from random import sample, uniform, randint


class RsHash:
    def __init__(self):
        self.d_num = 1
        self.hash_num = 4
        self.hash_mod = 9997
        self.hash_table_len = 10000
        self.sample_size = 1000
        self.detectors = list()

    def setup(self, de_num = 4, hash_num = 4, hash_t_len = 100, hash_mod = 97, s_size = 1000):
        self.d_num = de_num
        self.hash_num = hash_num
        self.hash_table_len = hash_t_len
        self.hash_mod = hash_mod
        self.sample_size = s_size

    def train(self, data_set):
        rows, cols = data_set.shape
        self.sample_size = min(rows, self.sample_size)
        for i in range(self.d_num):
            detector = Detector()
            detector.hash_num = self.hash_num
            detector.local_f = uniform(1.0/(self.sample_size**.5), 1 - 1.0/(self.sample_size**.5))
            detector.sample_attr = sample(range(cols),
                                          int(uniform(1+0.5*(log(self.sample_size, max(2, 1.0/self.sample_size)))
                                                  , log(self.sample_size, max(2, 1.0/self.sample_size)))))
            sample_set = numpy.array(sample(data_set, self.sample_size))
            shift = [uniform(0, detector.local_f) for _ in range(cols)]
            detector.shifts = shift
            mins, maxs, sample_set = self.normalize(sample_set)
            detector.min_attr = mins
            detector.max_attr = maxs
            detector.hash_table = numpy.zeros((self.hash_num, self.hash_table_len))
            for item in sample_set:
                for h in range(self.hash_num):
                    fun = self.gen_hash(cols)
                    detector.hash_fun.append(fun)
                    key = sum(fun * self.tran_item(item, shift, detector.sample_attr, detector.local_f))
                    # slot = self.insert_table(detector.hash_table[h], key)
                    detector.hash_table[h] = self.insert_table(detector.hash_table[h], key)
            print list(detector.hash_table[0])
            print list(detector.hash_table[1])

            self.detectors.append(detector)

    def evaluate(self, data_set):
        scores = list()
        for item in data_set:
            score = 0
            for detector in self.detectors:
                n_vector = self.tran_item(item, detector.shifts, detector.sample_attr, detector.local_f)
                s_tmp = float('inf')
                for i in range(detector.hash_num):
                    h_c = detector.hash_table[i, int(sum(detector.hash_fun[i] * n_vector) % self.hash_mod)]
                    if h_c < s_tmp:
                        s_tmp = h_c
                score += log(s_tmp+1, 2)
            scores.append(score / self.d_num)
        return scores


    def tran_item(self, item, weights, s_attr, p_f):
        for i in range(len(item)):
            if i in s_attr:
                item[i] = floor((item[i] + weights[i]) / p_f)
            else:
                item[i] = 1
        return item

    def gen_hash(self, cols):
        return numpy.array([randint(1, 100) for _ in range(cols)])

    def insert_table(self, table, key):
        i = int(key % self.hash_mod)
        slot = i
        if table[slot] != 0:
            # table[slot] += 1
            slot = int((slot+1) % self.hash_table_len)
            while table[slot] > 0 and slot != i:
                # table[slot] += 1
                slot = (slot+1) % self.hash_table_len
            table[slot] += 1
        else:
            table[slot] = 1
        return table


    def normalize(self, data_set):
        mins = data_set.min(axis=0)
        maxs = data_set.max(axis=0)
        return mins, maxs, (data_set-mins) / (maxs-mins)

