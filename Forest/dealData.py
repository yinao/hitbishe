# !/usr/bin/env python
# -*-coding:utf-8-*-
from sklearn.model_selection import train_test_split

# reading data
# fileObj = open("dataSets/http.dat", "r")
# dataLines = fileObj.readlines()
# dataSets = []
# labels = []
# for line in dataLines:
#     tmp = line.split(',')
#
#     if tmp[-1][:-2] == 'normal':
#         labels.append(1)
#     else:
#         labels.append(0)
#     tmp = tmp[0:1] + tmp[4:-1]
#     dataSets.append([float(x) for x in tmp])
#
# X_train, X_test, Y_train, Y_test = train_test_split(dataSets, labels, test_size=0.2)

# httpTrain = open("dataSets/httpTrain.dat", "w")
# for i in range(len(X_train)):
#     httpTrain.write(",".join(map(str,X_train[i] + [Y_train[i]])) + '\n')
# httpTrain.close()
#
# httpTest = open("dataSets/httpTest.dat", "w")
# for i in range(len(X_test)):
#     httpTest.write(",".join(map(str, X_test[i] + [Y_test[i]])) + '\n')
# httpTest.close()

# httpTrain = open("dataSets/httpTrain.dat", "r")
# httpTrain3 = open("dataSets/httpTrain3.dat", "w")
# for line in httpTrain.readlines():
#     tmp = line.split(",")
#     httpTrain3.write(tmp[0] + "," + tmp[1] + "," + tmp[2] + "," + tmp[-1])
# httpTrain.close()
# httpTrain3.close()
#
# httpTest = open("dataSets/httpTest.dat", "r")
# httpTest3 = open("dataSets/http", "w")
# for line in httpTest.readlines():
#     tmp = line.split(",")
#     httpTest3.write(tmp[0] + "," + tmp[1] + "," + tmp[2] + "," + tmp[-1])
# httpTest.close()
# httpTest3.close()

# obj = open("dataSets/covtype.dat", 'r')
# wobj = open("dataSets/covertype", 'w')
# lmap = dict()
# for line in obj.readlines():
#     tmp = line[:-1].split(',')
#     if tmp[-1] == '1':
#         s = ','.join(tmp[:10]) + ',' + tmp[-1]
#         wobj.write(s + '\n')
#     if tmp[-1] == '4':
#         s = ','.join(tmp[:10]) + ',' + '0'
#         wobj.write(s + '\n')
#     # lmap[tmp[-1]] = lmap.get(tmp[-1], 0) + 1
# wobj.close()
# obj.close()

# obj = open("dataSets/shuttle.txt", 'r')
# wobj = open("dataSets/shuttle", 'w')
# for line in obj.readlines():
#     tmp = line[:-1].split(" ")
#     if tmp[-1] == '1' or tmp[-1] == '4':
#         wobj.write(','.join(tmp[:-1]) + ",1\n")
#     else:
#         wobj.write(",".join(tmp[:-1]) + ",0\n")
# wobj.close()
# obj.close()

# computae the anomaly rate
obj = open('dataSets/shuttle', 'r')
wordscount = dict()
for line in obj.readlines():
    tmp = line[:-1].split(',')
    print len(tmp)
    wordscount[tmp[-1]] = wordscount.get(tmp[-1], 0) + 1
obj.close()
print wordscount
print 'anomaly rate: ', wordscount.get('0')*1.0/(wordscount.get('0') + wordscount.get('1'))

# test a normal instance and a anomaly instance differences
# d_obj = open('dataSets/shuttle')
# normal = list()
# anormal = list()
# for line in d_obj.readlines():
#     tmp = line[:-1].split(',')
#     if tmp[-1] == '1':
#         normal.append([float(x) for x in tmp[:-1]])
#     if tmp[-1] == '0':
#         anormal.append([float(x) for x in tmp[:-1]])
#
# import matplotlib.pyplot as pyplot
# from random import sample
# pyplot.figure(1)
# x = range(len(normal[0]))
# pyplot.plot(x, sample(normal,1)[0], linestyle='-')
# pyplot.plot(x, sample(anormal,1)[0], linestyle='--')
# pyplot.show()