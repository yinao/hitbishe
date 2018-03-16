import numpy
import matplotlib.pyplot as plt
from sklearn.preprocessing import minmax_scale
from sklearn.metrics import roc_auc_score
from DLForest import DLForest

data_set = numpy.loadtxt('../dataSets/arrhythmia', delimiter=',')

labels = data_set[:, -1]
data_set = data_set[:, :-1]
data_set = minmax_scale(data_set)

forest = DLForest()
forest.setup(sample_size=128, height_limit=6, leaf_size_limit=10, attr_sample_size=3, forest_size_limit=15)

forest.build(data_set.tolist())

scores = forest.evaluate(data_set, hlimit=6)

# print(scores)
# #
auc = roc_auc_score(labels, scores)

if auc < 0.5:
    auc = 1 - auc

print(auc)

# forest.show(forest.forest[0])
