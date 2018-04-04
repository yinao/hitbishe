# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy
from matplotlib import pyplot as plt

data = numpy.loadtxt('../dataSets/earthquakes', delimiter=',')
labels = data[:, 0].astype('int')
data = data[:, 1:]

rows, cols = data.shape

win_size = 8

paa_data = list()
for d in data:
    paa_tmp = list()
    for i in range(0, len(d), win_size):
        low = i
        high = min(len(d), i + win_size)
        PAA = sum(d[low: high]) / (high - low)
        paa_tmp.append(PAA)
    paa_data.append(paa_tmp)

paa_one = paa_data[0]
data_one = data[1]
data_two = data[2]
#
# print data_one[:win_size]
# print paa_one[0]
# exit()

plt.figure(1)
plt.plot(range(win_size), data_one[0:win_size], marker='*', label='series 1')
plt.plot(range(win_size), [paa_one[0] for _ in range(win_size)], marker='*', label='series 2')

plt.plot(range(win_size), data_two[0:win_size], marker='.', label='series 3')
plt.plot(range(win_size), [paa_data[2][0] for _ in range(win_size)], marker='.', label='series 4')

plt.legend(loc='upper right')
plt.xlabel('Time')
plt.ylabel('Y')
plt.tight_layout()
fig = plt.gcf()
fig.set_size_inches(6, 3.8)
# plt.show()
plt.savefig('results/paa_e.png', dpi=200)


# plt.figure(1)
# plt.plot(range(cols), data[0, :])
# plt.plot(range(cols), data[1, :])
# # plt.plot(range(cols), data[2, :])
# plt.show()
