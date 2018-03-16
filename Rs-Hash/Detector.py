# !/usr/bin/env python
# -*-coding:utf-8-*-


from random import randint


class Detector:
    def __init__(self):
        self.hash_num = 4
        self.hash_table = None
        self.local_f = 0
        self.sample_attr = None
        self.shifts = None
        self.min_attr = None
        self.max_attr = None
        self.hash_fun = list()