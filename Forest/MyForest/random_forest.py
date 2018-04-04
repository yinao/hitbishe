# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.cross_validation import train_test_split

data = np.loadtxt('../dataSets/ionosphere', delimiter=',')
label = data[:, -1]
data = data[:, :-1]
rows, cols = data.shape

train_x, text_x, train_y, text_y = train_test_split(data, label, test_size=0.2, random_state=0)

rf0 = RandomForestClassifier(oob_score=True, random_state=10)
rf0.fit(train_x,train_y)

y_predprob = rf0.predict_proba(text_x)[:,1]
print "AUC Score (Train): %f" % roc_auc_score(text_y, y_predprob)

