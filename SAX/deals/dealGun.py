# !/user/bin/env python
# -*-coding:utf-8-*-

import numpy
from sklearn.preprocessing import scale
import matplotlib.pyplot as plt

data = numpy.loadtxt('dataSets/ECG200/ecg200')
data = data[0:8, 1:]
rows, cols = data.shape
print rows, cols

n_data = data.reshape((1, rows*cols))

#
# # print data[:, 0]
# t, o = 0, 0
# n_data = numpy.zeros((rows-20, cols))
# a_c = 0
# j = 0
# for i in range(rows):
#     if data[i, 0] == 2 and a_c < 6:
#         # data[i, 0] = 0
#         n_data[j, 1:] = scale(data[i, 1:])
#         j += 1
#         a_c += 1
#     elif data[i, 0] == 1:
#         n_data[j, 1:] = scale(data[i, 1:])
#         n_data[j, 0] = 1
#         j += 1

# print n_data


# numpy.savetxt('dataSets/gun_1', n_data, fmt='%.5f')

plt.figure(1)
plt.xticks(range(0, rows*cols, 150))
plt.plot(range(0, rows*cols), n_data[0])
# plt.plot(range(cols*28, cols*28+cols), data[29])
plt.show()
