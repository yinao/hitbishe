# !/usr/bin/env python
# -*-coding:utf-8-*-

import matplotlib.pyplot as plt
from MBForest import MBForest
from sklearn import preprocessing
from sklearn.metrics import roc_auc_score
import time

set_name = 'arrhythmia'

fileObj = open("../dataSets/"+set_name, "r")
dataLines = fileObj.readlines()
dataSets = []
labels = []
for line in dataLines:
    tmp = line.split(',')
    labels.append(int(tmp[-1]))
    tmp = tmp[:-1]
    dataSets.append([float(x) for x in tmp])
fileObj.close()
# dataSets = preprocessing.scale(dataSets)

# test mbforest code
trainBeginTime = time.clock()
forest = MBForest()
forest.setup(tree_num=25, sample_size=256, size_limit=2, height_limit=6, less_height=0.025, much_height=0.95)
forest.build(dataSets)
print "training cost %s s" %(time.clock() - trainBeginTime)
testBeginTime = time.clock()
scores = forest.evaluate(dataSets, hlimit=6)
print "test time %s s" %(time.clock() - testBeginTime)
auc = roc_auc_score(labels, scores)
print "AUC is: %s" % (auc)
exit()

# make score figure code
# plt.figure(1)
# # x = [i for i in range(len(scores))]
# plt.plot(height, aucs)
# plt.xticks(height)
# # plt.ylim((0,1))
# plt.ylabel('AUC--')
# plt.xlabel('height limit h')
# plt.show()

# compare to iforest code
# height = []
# aucs = []
# r_obj = open('results/'+set_name+'/mb_t25_h1-15.txt', 'w')
# for i in range(1, 30, 1):
#     tmp = []
#     k = 5
#     auc_time = float('inf')
#     for j in range(k):
#         forest = MBForest()
#         forest.setup(tree_num=i, sample_size=256, size_limit=2, height_limit=6, less_height=0.0125, much_height=0.975)
#         forest.build(dataSets)
#         testBeginTime = time.clock()
#         scores = forest.evaluate(dataSets, hlimit=4)
#         # print "test time %s s" %(time.clock() - testBeginTime)
#         auc_time = min(auc_time, (time.clock() - testBeginTime))
#         auc = roc_auc_score(labels, scores)
#         print "AUC is: %s" % (auc)
#         tmp.append(auc)
#     r_obj.write(str(i) + '\t' + str(round(max(tmp), 4)) + '\t' +str(auc_time) + '\n')
#     # height.append(i)
#     # aucs.append(round(max(tmp),4))
#
# r_obj.close()

# record change code
mb_size_limit_record = 'mb_size_limit_record.txt'
mb_height_limit_record = 'mb_height_limit_4_record.txt'
r_obj = open('results/'+set_name+'/' + mb_height_limit_record, 'w')
r_obj.write('tree\theight\tauc\ttime\n')
for i in range(1, 50, 2):
    tmp = []
    k = 5
    auc_time = float('inf')
    for j in range(k):
        forest = MBForest()
        forest.setup(tree_num=i, sample_size=256, size_limit=2, height_limit=10, less_height=0.025, much_height=0.95)
        forest.build(dataSets)
        testBeginTime = time.clock()
        scores = forest.evaluate(dataSets, hlimit=4)
        # print "test time %s s" %(time.clock() - testBeginTime)
        auc_time = min(auc_time, (time.clock() - testBeginTime))
        auc = roc_auc_score(labels, scores)
        # print "AUC is: %s" % (auc)
        tmp.append(auc)
    print i, max(tmp), sum(tmp)/k
    r_obj.write(str(i) + '\t' + str(round(sum(tmp)/k,4)) + '\t' + str(round(max(tmp),4)) + '\t' +str(auc_time) + '\n')
    # height.append(i)
    # aucs.append(round(max(tmp),4))

r_obj.close()