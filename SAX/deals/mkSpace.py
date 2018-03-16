# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import scale, StandardScaler
from matplotlib import pyplot as plt
import scipy.io as sio

cutlines = dict()
cutlines[2] = [0, float('inf')]
cutlines[3] = [-0.43, 0.43, float('inf')]
cutlines[4] = [-0.67, 0, 0.67, float('inf')]
cutlines[5] = [-0.84, -0.25, 0.25, 0.84, float('inf')]
cutlines[6] = [-0.97, -0.43, 0, 0.43, 0.97, float('inf')]
cutlines[7] = [-1.07, -0.57, -0.18, 0.18, 0.57, 1.07, float('inf')]
cutlines[8] = [-1.15, -0.67, -0.32, 0, 0.32, 0.67, 1.15, float('inf')]
cutlines[9] = [-1.22, -0.76, -0.43, -0.14, 0.14, 0.43, 0.76, 1.22, float('inf')]
cutlines[10] = [-1.28, -0.84, -0.52, -0.25, 0, 0.25, 0.52, 0.84, 1.28, float('inf')]


data = numpy.loadtxt('../dataSets/tek16.txt')
n_data = data
n_data[0: 1000] = n_data[2000:3000]
n_data[1000: 2000] = n_data[3000:4000]

rows,  = n_data.shape

slide_win = 128
data = numpy.zeros((rows / slide_win, slide_win))

for i in range(len(data)):
    data[i] = n_data[i*slide_win: i*slide_win+slide_win]

rows, cols = data.shape

print rows

# plt.figure(1)
# plt.plot(range(len(data[2])), data[2], c='b')
# plt.annotate('Energizing', xy=(0, 3.3), fontsize=14)
# plt.annotate('Phase', xytext=(0, 3.1), xy=(100, 2), fontsize=14,arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
# plt.annotate('De-Energizing Phase', xy=(570, 1), xytext=(500, 1.5), fontsize=14, arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
# plt.tight_layout()
# fig = plt.gcf()
# fig.set_size_inches(10, 4)
# plt.savefig('results/space_cycle.png', dpi=100)
#
# plt.xticks([0, 5000, 10000, 15000])
# n_data[0: cols] = data[3]
# n_data[cols: 2*cols] = data[2]
# plt.plot(range(rows*cols), n_data[: rows*cols], c='b')
# plt.plot(range(4*cols, (4+1)*cols), data[4], c='r', linewidth=2)
# plt.annotate('discord', xy=(4450, 3), xytext=(4500, 3.5), fontsize=12, arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
# plt.tight_layout()
# fig = plt.gcf()
# fig.set_size_inches(10, 4)
# plt.savefig('results/space.png', dpi=100)


index = 32
plt.plot(range(rows*cols), n_data[: rows*cols], c='b')
plt.plot(range(index*cols, (index+1)*cols), data[index], c='r', linewidth=2)
plt.plot(range((index+1)*cols, (index+2)*cols), data[index+1], c='g', linewidth=2)
plt.annotate('first discord', xy=(4300, 3), xytext=(4500, 3.3), fontsize=12, arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
plt.annotate('second discord', xy=(4100, 3), xytext=(3400, 4.3), fontsize=12, arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
plt.tight_layout()
fig = plt.gcf()
fig.set_size_inches(10, 4)
# plt.show()
plt.savefig('../results/space_ep.png', dpi=100)


