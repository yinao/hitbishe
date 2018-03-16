# !/usr/bin/env python
# -*-coding:utf-8-*-
import numpy
import csv
from sklearn import preprocessing

set_name = 'shuttle'
d_obj = open('dataSets/'+set_name)
data_set = list()
labels = list()
a_count = 0
for line in d_obj.readlines():
    tmp = line[:-1].split(',')
    for i in range(len(tmp)-1):
        tmp[i] = float(tmp[i])
    labels.append(int(tmp[len(tmp)-1]))
    if tmp[-1] == '0':
        a_count += 1
    data_set.append(tmp[:-1])
d_obj.close()

data_set2 = numpy.array(data_set)
data_set = preprocessing.MinMaxScaler().fit_transform(data_set)

rows, cols = data_set.shape
c_obj = open('feature_count.txt', 'a')
# c_obj.write('数据集 %s\n' % set_name)
# c_obj.write("总异常数 %d\n" % a_count)
print '总异常数：%d' %a_count
for c in range(cols):
    mean = data_set[:,c].mean()
    std = data_set[:,c].std()
    flag1 = mean-3*std
    flag2 = mean+3*std
    ac_count = 0
    n_count = 0
    for r in range(rows):
        if data_set[r,c] <= flag1 or data_set[r, c] >= flag2:
            if labels[r] == 0:
                ac_count += 1
            else:
                n_count += 1

    print '属性%d, 均值%f, 方差%f, 0.975置信区间之外异常数：%d，正常实例数：%d' %(c, mean, std, ac_count, n_count)

c_obj.close()

# import matplotlib.pyplot as pyplot
# pyplot.figure(1)
# for c in range(cols-1):
#     pyplot.subplot(c+241)
#     x = range(len(data_set[:,c]))
#     pyplot.scatter(x, data_set[:,c])
#     pyplot.xlabel(c)
# pyplot.show()

# pyplot.figure(1)
# pyplot.subplot(211)
# pyplot.plot(range(len(data_set)), data_set2[:, 6])
# pyplot.subplot(212)
# pyplot.plot(range(len(data_set)), data_set[:, 6])
# pyplot.show()
