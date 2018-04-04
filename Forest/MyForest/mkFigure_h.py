# !/usr/bin/env python
# -*-coding:utf-8-*-

import matplotlib.pyplot as plt

if_obj = open('./results/pima/if_t25_h1-14.txt')
if_y = list()
for line in if_obj.readlines():
    tmp = line[:-1].split('\t')
    if_y.append(float(tmp[1]))
if_obj.close()

mb_obj = open('./results/pima/mb_t25_h1-14.txt2')
# mb_obj.readline()
mb_y = list()
for line in mb_obj.readlines():
    tmp = line[:-1].split('\t')
    if float(tmp[1]) < 0.5:
        tmp[1] = 1 - float(tmp[1])
    mb_y.append(float(tmp[1]))
mb_obj.close()

hs_obj = open('./results/pima/hs_t25_h1-15.txt')
hs_obj.readline()
hs_y = list()
for line in hs_obj.readlines():
    tmp = line[:-1].split('\t')
    hs_y.append(float(tmp[1]))
    if hs_y[-1] < 0.5:
        hs_y[-1] = 1 - hs_y[-1]
hs_obj.close()

rs_obj = open('./results/pima/rs_t25_h1-15.txt')
rs_obj.readline()
rs_y = list()
for line in rs_obj.readlines():
    tmp = line[:-1].split('\t')
    rs_y.append(float(tmp[1]))
    if rs_y[-1] < 0.5:
        rs_y[-1] = 1 - rs_y[-1]
rs_obj.close()

plt.figure(1)

x = [x+1 for x in range(0, len(if_y))]
plt.plot(x, mb_y, color='r', marker='D', label='TB-Forest')
plt.plot(x, if_y, color='#029ED9', marker='*', label='iForest')
plt.plot(x, hs_y, color='g', marker='^', label='HS-Forest')
plt.plot(x, rs_y[:-1], color='#a3159a', marker='4', label='RS-Forest')
# plt.xticks(x)
# plt.ylim((0.6, 1))
# plt.xlabel('Tree Height number h With Tree number=25')
plt.xlabel('Tree height h With Tree_Size=25')
plt.ylabel('AUC')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), fancybox=False, ncol=4)
fig = plt.gcf()
fig.set_size_inches(6, 5)
plt.show()
#
# plt.savefig('./results/http/f_h_t25_2.png', dpi=300)

# make mb height change rate
# h_obj = open('results/shuttle/mb_height_limit_2_record.txt')
# heights2 = []
# auc_rs2 = []
# h_obj.readline()
# for line in h_obj.readlines():
#     tmp = line[:-1].split('\t')
#     heights2.append(int(tmp[0]))
#     auc_rs2.append(float(tmp[1]))
# h_obj.close()
#
# h_obj = open('results/shuttle/mb_height_limit_4_record.txt')
# heights4 = []
# auc_rs4 = []
# h_obj.readline()
# for line in h_obj.readlines():
#     tmp = line[:-1].split('\t')
#     heights4.append(int(tmp[0]))
#     auc_rs4.append(float(tmp[1]))
# h_obj.close()
#
# plt.figure(2)
# plt.plot(heights2, auc_rs2, marker='*')
# plt.plot(heights4, auc_rs4)
# plt.ylim((0.7, 1))
# plt.show()

