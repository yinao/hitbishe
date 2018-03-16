# !/usr/bin/env python
# -*-coding:utf-8-*-

import matplotlib.pyplot as plt

# if_obj = open('results/http/if_t1-25_h6.txt')
# if_y = list()
# for line in if_obj.readlines():
#     tmp = line[:-1].split('\t')
#     if_y.append(float(tmp[1]))
# if_obj.close()
#
# mb_obj = open('results/http/mb_t25_h1-15.txt')
# mb_y = list()
# for line in mb_obj.readlines():
#     tmp = line[:-1].split('\t')
#     mb_y.append(float(tmp[1]))
# mb_obj.close()
#
# plt.figure(1)
# x = [x+1 for x in range(len(if_y))]
# plt.plot(x, if_y, color='blue', linestyle='-', label='iForest')
# plt.plot(x, mb_y, color='green', linestyle='--', label='MBForest')
# # plt.xticks(x)
# plt.ylim((0.5, 1))
# # plt.xlabel('Tree Height number h With Tree number=25')
# plt.xlabel('Tree number t With Height=6')
# plt.ylabel('AUC----')
# plt.legend(loc=(0.75,0.8))
# plt.show()


# make mb height change rate
h_obj = open('results/shuttle/mb_height_limit_2_record.txt')
heights2 = []
auc_rs2 = []
h_obj.readline()
for line in h_obj.readlines():
    tmp = line[:-1].split('\t')
    heights2.append(int(tmp[0]))
    auc_rs2.append(float(tmp[1]))
h_obj.close()

h_obj = open('results/shuttle/mb_height_limit_4_record.txt')
heights4 = []
auc_rs4 = []
h_obj.readline()
for line in h_obj.readlines():
    tmp = line[:-1].split('\t')
    heights4.append(int(tmp[0]))
    auc_rs4.append(float(tmp[1]))
h_obj.close()

plt.figure(2)
plt.plot(heights2, auc_rs2, marker='*')
plt.plot(heights4, auc_rs4)
plt.ylim((0.7, 1))
plt.show()

