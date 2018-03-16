# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

data_set = numpy.loadtxt('../dataSets/arrhythmia', delimiter=',')
labels = data_set[:, -1]
data_set = data_set[:,:-1]

rows, cols = data_set.shape

# 使用散点图查看两个属性值的分布对异常属性的影响

# attr = [0, 2]
attr = random.sample(range(cols), 3)
print attr

n_x = list()
n_y = list()
n_z = list()
a_x = list()
a_y = list()
a_z = list()

for i in range(rows):
    if labels[i] == 1:
        n_x.append(data_set[i, attr[0]])
        n_y.append(data_set[i, attr[1]])
        n_z.append(data_set[i, attr[2]])
    else:
        a_x.append(data_set[i, attr[0]])
        a_y.append(data_set[i, attr[1]])
        a_z.append(data_set[i, attr[2]])


fig = plt.figure()
ax = fig.gca(projection='3d')

#将数据点分成三部分画，在颜色上有区分度
ax.scatter(n_x, n_y, n_z)
ax.scatter(a_x, a_y, a_z)
# ax.plot_trisurf(n_x, n_y, n_z, linewidth=0.2)
# ax.plot_trisurf(a_x, a_y, a_z, linewidth=0.2)

ax.set_zlabel('Z') #坐标轴
ax.set_ylabel('Y')
ax.set_xlabel('X')

plt.legend(loc='upper right')

plt.show()
