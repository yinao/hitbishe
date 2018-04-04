# !/usr/bin/env python
# -*-coding:utf-8-*-

import matplotlib.pyplot as plt

x1 = range(9)
y1 = [-1.28, -0.84, -0.52, -0.25, 0, 0.25, 0.52, 0.84, 1.28]

x2 = range(1, 4)
y2 = [-0.84, -0.52, -0.25]

plt.figure(1)
plt.plot(x1, y1)
plt.plot(x2, y2, c='r', lw='3')
plt.show()
plt.close()