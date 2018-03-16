# !/usr/bin/env python
# -*-coding:utf-8-*-

import time
import numpy
import random
from matplotlib import pyplot as plt
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import scale

# x = np.arange(0, 40*np.pi, 0.1)
# y = np.sin(x) / 2
# y1 = np.sin(x*0.5) / 2
# y2 = (y + y1) / 3
#
# low = len(np.arange(0, 2*np.pi, 0.1))
# high = low+len(np.arange(2*np.pi, 2.2*np.pi, 0.1))
#
# for i in range(low, high, 1):
#     y2[i] += random.uniform(-0.1, 0.2)
#
# x2 = np.arange(0, 4*np.pi, 0.1)
#
# plt.figure(1)
# # plt.ylim(-0.6, 1)
# plt.plot(x, scale(y2), label='y2')
# plt.show()

data = numpy.loadtxt('../dataSets/chfdbchf15.txt')
n_data = data[:15000, 1]

rows,  = n_data.shape

slide_win = 275
data = numpy.zeros((rows / slide_win, slide_win))

for i in range(len(data)):
    data[i] = n_data[i*slide_win: i*slide_win+slide_win]


rows, cols = data.shape

print rows, cols

# plt.ylim(-2.5, 10)

plt.plot(range(13*cols), n_data[: 13*cols], c='b')
plt.plot(range(13*cols, 53*cols), n_data[13*cols: 53*cols], c='g')
plt.plot(range(8*cols, (8+1)*cols), data[8], c='r', linewidth=2)

plt.annotate('data from B', xytext=(52*cols-500, -1.5),
             xy=(52*cols-150, -0),
             arrowprops=dict(arrowstyle='->'),
             rotation='10',
             fontsize=15)

plt.annotate('data from A', xytext=(0, -1.5),
             xy=(1000, -0.8),
             arrowprops=dict(arrowstyle='->'),
             rotation='-10',
             fontsize=15)

# table_vals = [['22233311', 1],
#               ['23111111', 1],
#               ['11111222', 1],
#               ['22112221', 1]]
# row_colors = ['red','gold','green']
# my_table = plt.table(cellText=table_vals, colWidths=[0.05, 0.03],
#                      loc=(100, 222), fontsize=20)

plt.tight_layout()
fig = plt.gcf()

fig.set_size_inches(14.5, 5)

plt.show()

# plt.savefig('../results/ecg_dis2.png', dpi=500)