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


data = numpy.loadtxt('dataSets/tek16.txt')
n_data = data

# n_data = StandardScaler().fit_transform(n_data)

rows,  = n_data.shape

slide_win = 1000
data = numpy.zeros((rows / slide_win, slide_win))

for i in range(len(data)):
    data[i] = n_data[i*slide_win: i*slide_win+slide_win]


plt.figure(1)
plt.plot(range(len(data[2])), data[2], c='b')
plt.annotate('Energizing', xy=(0, 3.3), fontsize=14)
plt.annotate('Phase', xytext=(0, 3.1), xy=(100, 2), fontsize=14,arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
plt.annotate('De-Energizing Phase', xy=(570, 1), xytext=(500, 1.5), fontsize=14, arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
plt.tight_layout()
fig = plt.gcf()
fig.set_size_inches(10, 4)
plt.savefig('results/space_cycle.png', dpi=100)

exit()
for a in range(2, 3):
    for w in range(1, 3):
        for c in range(1, 3):
            words = 3
            win_size = 1
            sub_len = 4

            symbol_data = list()
            for d in data:
                tmp = list()
                for i in range(0, len(d), win_size):
                    low = i
                    high = min(len(d), i + win_size)
                    PAA = sum(d[low: high]) / (high - low)
                    for k in range(words):
                        if PAA < cutlines[words][k]:
                            break
                    tmp.append(str(k+1))
                sub_dict = dict()
                for t in range(0, len(tmp), sub_len):
                    s = ''.join(tmp[t:t+sub_len])
                    sub_dict[s] = sub_dict.get(s, 0) + 1

                symbol_data.append(sub_dict)

            # 正则化每个子模式的次数
            # for i in range(len(symbol_data)):
            #     max_c = max(symbol_data[i].values())
            #     for k in symbol_data[i].keys():
            #         symbol_data[i][k] = 1.0*symbol_data[i][k] / max_c

            # print symbol_data

            scores = list()
            for i in range(len(symbol_data)):
                min_dist = float('inf')
                for j in range(len(symbol_data)):
                    if i == j:
                        continue
                    dist = 0
                    a_keys = symbol_data[i].keys()
                    b_keys = symbol_data[j].keys()
                    keys = list(set(a_keys).union(set(b_keys)))
                    for k in keys:
                        dist += (symbol_data[i].get(k, 0) - symbol_data[j].get(k, 0))**2
                    dist **= 0.5
                    min_dist = min(dist, min_dist)
                scores.append(min_dist)

            index = numpy.argsort(-numpy.array(scores))
            # print index

            # auc = roc_auc_score(labels, scores)
            #
            # if auc < 0.5:
            #     auc = 1 - auc
            if index[0] == 4:
                print 'words=%d, win_size=%d, sub_len=%d, discord=%d' %(words, win_size, sub_len, index[0])

            print symbol_data[4]
            print symbol_data[1]

            # rows, cols = data.shape
            #
            # print rows, cols
            # # #
            # # index[0] = 18
            # # index[1] = 17
            # # index[2] = 7
            # plt.xticks([0, 5000, 10000, 15000])
            # n_data[0: cols] = data[3]
            # n_data[cols: 2*cols] = data[2]
            # plt.plot(range(rows*cols), n_data[: rows*cols], c='b')
            # plt.plot(range(index[0]*cols, (index[0]+1)*cols), data[index[0]], c='r', linewidth=2)
            # # plt.plot(range(index[1]*cols, (index[1]+1)*cols), data[index[1]], c='g', linewidth=2)
            # # plt.plot(range(index[2] * cols, (index[2] + 1) * cols), data[index[2]], linewidth=2)
            # # plt.plot(range(0, 370), data[0][0:370])
            # # plt.plot(range(360, 600), data[0][360:600])
            # plt.annotate('discord', xy=(4450, 3), xytext=(4500, 3.5), fontsize=12, arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
            # plt.tight_layout()
            # fig = plt.gcf()
            # fig.set_size_inches(10, 4)
            # # plt.show()
            # plt.savefig('results/space.png', dpi=100)
            # #
            # plt.close()
            #
