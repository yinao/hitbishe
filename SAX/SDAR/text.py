# !/usr/bin/env python
# -*-coding:utf-8-*-

import time
from bitarray import bitarray

a = bitarray('0101')
b = bitarray('0111')

a1 = int(a.to01(), 2)
b1 = int(b.to01(), 2)

begin = time.clock()

c = (a^b).count()

print time.clock() - begin

begin = time.clock()
c = a1^b1
c_x = 0
while c:
    c_x += 1
    c &= (c-1)

print time.clock() - begin