# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy as np
from matplotlib import pyplot as plt

data = np.loadtxt('../dataSets/pima', delimiter=',')
label = data[:, -1]
data = data[:, :-1]
rows, cols = data.shape

one_data = data[:, 1]

arr = list()
nrr = list()
for i in range(rows):
    if label[i] == 1:
        arr.append(one_data[i])
    else:
        nrr.append(one_data[i])

plt.figure(1)
plt.hist(arr, bins=20)
plt.hist(nrr, bins=20, alpha=0.5)
plt.show()
