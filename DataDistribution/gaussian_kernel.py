# !/usr/bin/env python
# -*-coding:utf-8-*-


import numpy as np
from matplotlib import pyplot as plt

data = np.loadtxt('../dataSets/hapt511', delimiter=',')
label = data[:, -1]
data = data[:, :-1]
rows, cols = data.shape

data_x = data[:, 1]
data_y = data[:, 2]
data_z = data[:, 3]
data_w = data[:, 4]

n_x, n_y = list(), list()
a_x, a_y = list(), list()

for i in range(rows):
    if label[i] == 1:
        n_x.append(i)
        n_y.append(data_y[i])
    else:
        a_x.append(i)
        a_y.append(data_y[i])

n_g_x, a_g_x = list(), list()
n_g, a_g = list(), list()
for i in range(rows):
    tmp = np.exp(- 0.6*(data_x[i]**2+data_z[i]**2))
    if label[i] == 1:
        n_g_x.append(i)
        n_g.append(tmp)
    else:
        a_g_x.append(i)
        a_g.append(tmp)

plt.figure(1)
plt.subplot(121)
plt.scatter(n_x, n_y)
plt.scatter(a_x, a_y)

plt.subplot(122)
plt.scatter(n_g_x, n_g)
plt.scatter(a_g_x, a_g)

plt.show()

