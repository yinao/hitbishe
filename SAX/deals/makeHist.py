# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy as np
import matplotlib.pyplot as plt

name_list = ['ECG200', 'Wafer', 'Strawberry', 'Lighting2', 'Gun Points', 'ToeSegmentation2']
fmdp_cost = [0.36, 9.326, 1.7, 0.13, 0.27, 0.38]
bf_cost = [4.94, 16.8, 2.58, 2.78, 0.36, 7.75]
hs_cost = [1.38, 12.579, 3.52,  0.733, 0.63, 1.917]
bc_cost = [0.107, 0.89, 0.447, 0.209, 0.1267, 0.245]

x = range(len(name_list))
total_width, n = 0.4, 2
width = total_width / n

fmdp = plt.bar(x, fmdp_cost, width=width, label='FMDP*', fc='#029ED9')

for i in range(len(x)):
    x[i] += width
bf = plt.bar(x, bf_cost, width=width, label='Brute Force', fc='#81ff38')

for i in range(len(x)):
    x[i] += width
hs = plt.bar(x, hs_cost, width=width, label='HOT SAX', fc='#ff7438')

for i in range(len(x)):
    x[i] += width
bc = plt.bar(x, bc_cost, width=width, label='BitCluster', fc='#a3159a')

# fmdp = plt.bar(x, fmdp_cost, width=width, label='FMDP*', fc='#00768f')
#
# for i in range(len(x)):
#     x[i] += width
# bf = plt.bar(x, bf_cost, width=width, label='Brute Force', fc='#fac457')
#
# for i in range(len(x)):
#     x[i] += width
# hs = plt.bar(x, hs_cost, width=width, label='HOT SAX', fc='#ff7438')
#
# for i in range(len(x)):
#     x[i] += width
# bc = plt.bar(x, bc_cost, width=width, label='BitCluster', fc='#a3159a')
#

plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), fancybox=False, ncol=4)

def add_white(rects):
    for rect in rects:
        rect.set_edgecolor('white')

add_white(fmdp)
add_white(bf)
add_white(hs)
add_white(bc)

plt.ylim(0, 7)
plt.ylabel('Time:(seconds)')
plt.xlabel('Data Sets')

plt.xticks(np.array(x) - 2*width, name_list, rotation='15')

# plt.show()
plt.savefig('../results/time_hist2.png', dpi=200)