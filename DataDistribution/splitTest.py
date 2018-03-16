# !/usr/bin/env python
# -*-coding:utf-8-*-

import random
import numpy
import matplotlib.pyplot as plt

data_set = numpy.loadtxt('../dataSets/hapt511', delimiter=',')
data_set = random.sample(data_set.tolist(), 256)
data_set = numpy.array(data_set)

rows, cols = data_set.shape

plt.figure(1)

s_index = random.randint(0, cols-2)
s_value = random.uniform(min(data_set[:, s_index]), max(data_set[:, s_index]))

plt.subplot(121)
plt.xlim(0, rows)
n_x, n_y = list(), list()
a_x, a_y = list(), list()
for i in range(rows):
    if data_set[i, -1] == 1:
        n_x.append(i)
        n_y.append(data_set[i, s_index])
    else:
        a_x.append(i)
        a_y.append(data_set[i, s_index])

plt.scatter(n_x, n_y, s=20)
plt.scatter(a_x, a_y, marker='*', s=80)
plt.plot(range(0, rows), [s_value for i in range(rows)], c='r', linewidth='3')
plt.title(s_index)

left = numpy.where(data_set[:, s_index] < s_value)

data_set = data_set[left]
rows, cols = data_set.shape
print rows

s_index = random.randint(0, cols-2)
s_value = random.uniform(min(data_set[:, s_index]), max(data_set[:, s_index]))

plt.subplot(122)
plt.xlim(0, rows)
n_x, n_y = list(), list()
a_x, a_y = list(), list()
for i in range(rows):
    if data_set[i, -1] == 1:
        n_x.append(i)
        n_y.append(data_set[i, s_index])
    else:
        a_x.append(i)
        a_y.append(data_set[i, s_index])

plt.scatter(n_x, n_y, s=20)
plt.scatter(a_x, a_y, marker='*', s=80)
plt.plot(range(0, rows), [s_value for i in range(rows)], c='r', linewidth='3')
plt.title(s_index)


plt.show()