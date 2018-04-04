# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy
import random
import matplotlib.pyplot as plt
from sklearn.preprocessing import minmax_scale
from AutoEncoder import AutoEncoder

data_set = numpy.loadtxt('../dataSets/hapt511', delimiter=',')

s_data = numpy.array(random.sample(data_set.tolist(), 256))
s_data = minmax_scale(s_data)
labels = s_data[:, -1]

_, cols = s_data.shape

s_index = random.sample(range(cols), 3)
s_data = s_data[:, s_index]

rows, cols = s_data.shape

ae = AutoEncoder()
ae.init_tf(fin=cols, fou=1, epochs=10)

results = ae.get_results(s_data)

split = random.uniform(min(results['inters']), max(results['inters']))

# print(results['inters'][numpy.where(results['inters'] > split)])

# print(results['weights'])
# print(results['biases'])
# print(results['inters'])
exit()

# split = (min(results['inters'])+max(results['inters'])) /2

x1, y1 = list(), list()
x2, y2 = list(), list()

for i in range(rows):
    if labels[i] == 1:
        x1.append(i)
        y1.append(results['inters'][i])
    else:
        x2.append(i)
        y2.append(results['inters'][i])

plt.figure(1)
plt.xlim(0, rows)
plt.scatter(x1, y1, s=20)
plt.scatter(x2, y2, marker='*', s=50, c='r')
plt.show()
