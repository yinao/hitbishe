# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy
from RandomSubspaceHash import RsHash
from math import log, floor, ceil
from random import sample, uniform, randint
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

data_set = numpy.loadtxt('../dataSets/musk', delimiter=',')
labels = data_set[:, -1]
data_set = numpy.delete(data_set, -1, axis=1)
train_x, text_x, train_y, text_y = train_test_split(data_set, labels, test_size=0.33)

rows, cols = train_x.shape

# 初始化参数
detector_num = 30
hash_table_len = 1000
hash_num = 4
hash_table = numpy.zeros((detector_num, hash_num, hash_table_len), dtype='int')
hash_fun = list()
sample_size = 1000

# 初始化hash函数
for _ in range(hash_num):
    hash_fun.append((randint(101, 999), randint(101, 999)))
    # hash_fun.append(numpy.random.randint(10, 100, size=cols))


def rs_hash(item, h_fun):
    res = 0
    a, b = h_fun
    for x in item:
        res = res * a + x
        a = a * b
    return int(res)


sample_size = min(sample_size, rows)
for d in range(detector_num):
    # 生成局部参数f
    local_f = uniform(1.0/(sample_size**0.5), 1-1.0/(sample_size**0.5))
    # 随机向量
    s_vector = [uniform(0, local_f) for _ in range(cols)]
    # 随机采样属性的数量
    r_attr = randint(int(1+0.5*log(sample_size, max(2, 1.0/local_f))),int(log(sample_size, max(2, 1.0/local_f))))
    s_attr = sample(range(cols), min(r_attr, cols))
    # 采样数据集
    sample_set = numpy.array(sample(data_set, sample_size))
    # 计算属性最小值
    min_attr = sample_set.min(axis=0)
    # 计算属性最大值
    max_attr = sample_set.max(axis=0)
    # 正则化采样到的数据
    n_sm_set = (sample_set-min_attr) / (max_attr-min_attr)
    # 计算hash table
    slot_count = dict()
    for h in range(hash_num):
        for i in range(sample_size):
            item = numpy.floor((n_sm_set[i] + s_vector) / local_f)[s_attr]
            # print item
            slot = rs_hash(item, hash_fun[h]) % hash_table_len
            hash_table[d, h, slot] += 1


text_set = (text_x-min_attr) / (max_attr-min_attr)
scores = list()
for i in range(len(text_set)):
    s_sum = 0
    for d in range(detector_num):
        tmp = float('inf')
        for h in range(hash_num):
            item = numpy.floor((text_set[i] + s_vector) / local_f)[s_attr]
            slot = rs_hash(item, hash_fun[h]) % hash_table_len
            tmp = min(tmp, hash_table[d, h, slot])
        s_sum += log(tmp+1, 2)
    scores.append(s_sum/detector_num)

print 'AUC ', roc_auc_score(text_y, scores)


# for i in range(30):
#     a_right, a_left, right, left = 0, 0, 0, 0
#     for k in range(len(train_x)):
#         x = train_x[k]
#         cols = x.shape[0]
#         s_r = sample(range(cols), 1)
#         weights = [uniform(0, 1) for _ in s_r]
#         ones, zeros = 0, 0
#         for h in range(1):
#             if int((weights[h] * x[s_r[h]]) % 1 * 2) == 1:
#                 ones += 1
#             else:
#                 zeros += 1
#         if ones >= zeros:
#             right += 1
#             if train_y[k] == 0:
#                 a_right += 1
#         else:
#             left += 1
#             if train_y[k] == 0:
#                 a_left += 1
#
#     print float(a_left)/left, float(a_right)/right, float(left)/right
#
#
# exit()

