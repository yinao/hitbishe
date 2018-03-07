# !/usr/bin/env python
# -*-coding:utf-8-*-


from random import randint
data = [0, 0, 0, 0, 0, 0, 1, 0, 0]

a = 3
b = 9
res = 0
for d in data:
    res = res*a + d
    a *= b
print res