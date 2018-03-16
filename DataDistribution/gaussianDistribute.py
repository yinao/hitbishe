import numpy
import math
import random
from sklearn.preprocessing import scale
import matplotlib.pyplot as plt

data_set = numpy.loadtxt('../dataSets/Satellite', delimiter=',')

rows, cols = data_set.shape

# sample_data = random.sample(data_set.tolist(), min(rows, 128))
sample_data = numpy.array(data_set)

labels = sample_data[:, -1]
sample_data = sample_data[:, :-1]

s_index = random.randint(0, cols-2)

print s_index

attr_data = scale(sample_data[:, s_index])

mean = attr_data.mean()
std = attr_data.std()

upper = mean + 3*std
lower = mean - 3*std

# print mean, std

scores = list()
upper_count = 0
lower_count = 0
for i in range(rows):
    tmp = (1.0/(std*(2*math.pi)**0.5)) * math.e**-(0.5*((attr_data[i] - mean)/std)**2)
    if attr_data[i] >= upper:
        upper_count += 1
    if attr_data[i] <= lower:
        lower_count += 1
    scores.append(tmp)

print "lower: ", lower_count
print "upper: ", upper_count

n_x, n_y = list(), list()
a_x, a_y = list(), list()
for i in range(rows):
    if labels[i] == 1:
        n_x.append(attr_data[i])
        n_y.append(scores[i] + 0.08)
    else:
        a_x.append(attr_data[i])
        a_y.append(scores[i])

# plt.xlim(0, rows)

plt.scatter(n_x, n_y, label='true')
plt.scatter(a_x, a_y, label='false')

plt.legend(loc='upper right')

plt.show()
