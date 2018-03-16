# !/usr/bin/env python
# -*-coding:utf-8-*-

import time
from MAiForest import MAiForest
from sklearn import preprocessing
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from matplotlib import pyplot

# record = open('record.txt', 'a')
# record.write("one random hyperplane")
data_set = '../dataSets/Satellite'
cur_time = time.strftime('%Y-%m-%d %H:%M:%S')
train_height_limit = 8
tree_num = 25
sample_size = 512
sample_attribute = 3
random_plane = 25
test_size_limit = 1

# record.write("time: %s\n" % cur_time)
# record.write("data set: %s \n" % data_set)
# record.write("train height limit: %d\n" % train_height_limit)
# record.write("train tree num: %d\n" % tree_num)
# record.write("test height limit: %d\n" % test_height_limit)
# record.write("update tree profile with sample size: %d\n" % sample_size)
# record.write("train tree with sample attributes randomly: %d\n" % sample_attribute)

# reading training data
begin = time.clock()
fileObj = open(data_set, "r")
dataSets, labels = [], []
for line in fileObj.readlines():
    tmp = line.split(',')
    labels.append(int(tmp[-1]))
    dataSets.append([float(x) for x in tmp[:-1]])
fileObj.close()
dataSets = preprocessing.scale(dataSets)
end = time.clock()
print "reading data cost %s s" %(end-begin)

# X_train, X_test, Y_train, Y_test = train_test_split(dataSets, labels, test_size=0.2)
X_train, Y_train = dataSets, labels
begin = time.clock()
forest = MAiForest()
forest.setup(attr=len(X_train[0]), hlimit=train_height_limit, tree_num=tree_num, sample_attrs=sample_attribute, planes=random_plane)
forest.build()
end = time.clock()
print "building forest cost %s s" %(end-begin)

begin = time.clock()
scores = forest.init(X_train, s_size=sample_size)
end = time.clock()
print "init model size cost %s s" %(end-begin)

begin = time.clock()
scores = forest.evaluate(X_train, hlimit=test_size_limit)
end = time.clock()
print "evaluate model cost %s s" %(end-begin)
#
auc = roc_auc_score(Y_train, scores)
#
print "AUC score is %s" % (auc)
# record.write("AUC score: %s\n" % auc)
# record.write("====================================\n\n")
# record.close()
#
# pyplot.figure(1)
# pyplot.scatter(range(len(scores)), scores, marker=".")
# pyplot.show()

