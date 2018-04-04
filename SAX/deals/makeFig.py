# !/usr/bin/env python
# -*-coding:utf-8-*-


import numpy
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale

data = numpy.loadtxt('../dataSets/ECG200/ecg200')
labels = data[:,  0]
data = data[:, 1:]
rows, cols = data.shape



plt.figure(1)
# plt.xlim(0, cols)
plt.yticks((-0.43, 0.43))

# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)
# ax.spines['left'].set_visible(False)
# ax.yaxis.set_ticks_position('left')
# ax.spines['left'].set_position(('data',0))

# 原始数据集
x = range(5, cols+5)
y = scale(data[0])
plt.plot(x, y, color='#808080', linewidth='2')
plt.tight_layout()

# 两条分割线
x = range(0, cols+5)
y1 = [-0.43 for _ in x]
y2 = [0.43 for _ in x]
plt.plot(x, y1, linestyle='--', color='#C0C0C0')
plt.plot(x, y2, linestyle='--', color='#C0C0C0')

# 离散化的数据折线图, 做平均的数据点为12
w = 3
a = 8
m = 3
d_y = numpy.zeros(cols)
for i in range(0, cols, a):
    tmp = sum(y[i:i+a]) / a
    for k in range(a):
        d_y[i+k] = tmp

plt.plot(range(5, cols+5), d_y, color='#A0A0A0', linewidth='3.5')

# 添加离散化后的符号显示
for i in range(0, cols, a):
    # print i
    # print d_y[i:i+a]
    if d_y[i] < -0.43:
        # 蓝色
        plt.plot(range(5 + i, i + a +5), d_y[i:i+a], linewidth='4', color='b')
        plt.annotate('a', xy=(i+8, d_y[i]-0.18), fontsize=14)
    elif d_y[i] < 0.43:
        # 绿色
        plt.plot(range(5 + i, i + a + 5), d_y[i:i + a], linewidth='4', color='g')
        plt.annotate('b', xy=(i+8, d_y[i]-0.18), fontsize=14)
    else:
        # 红色
        plt.plot(range(5 + i, i + a + 5), d_y[i:i + a], linewidth='4', color='r')
        plt.annotate('c', xy=(i+8, d_y[i]-0.18), fontsize=14)

fig = plt.gcf()
fig.set_size_inches(6, 3.5)
# plt.show()
plt.savefig('../results/sax_ins3.png', dip=300)