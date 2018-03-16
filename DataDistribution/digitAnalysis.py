# !/usr/bin/env python
# -*-coding:utf-8-*-

import numpy
import tensorflow as tf
import random
import matplotlib.pyplot as plt

data_set = numpy.loadtxt('../dataSets/ann_thyroid', delimiter=',')
labels = data_set[:, -1]
data_set = data_set[:,:-1]
#
# rows, cols = data_set.shape
#
# print(rows, cols)

s_data = numpy.array(random.sample(data_set.tolist(), 256))

learning_rate = 0.01
training_epochs = 10
display_step = 1
n_input = 6
n_hidden = 1

# init weights
weights = {
    'encoder_h1': tf.Variable(tf.random_normal([n_input, n_hidden])),
    'decoder_h2': tf.Variable(tf.random_normal([n_hidden, n_input])),
}
biases = {
    'encoder_b1': tf.Variable(tf.random_normal([n_hidden])),
    'decoder_b2': tf.Variable(tf.random_normal([n_input])),
}


def encoder(x):
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['encoder_h1']),
                                   biases['encoder_b1']))
    return layer_1


# 构建解码器
def decoder(x):
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['decoder_h2']),
                                   biases['decoder_b2']))
    return layer_1


# 构建模型

X = tf.placeholder("float", [None, n_input])

encoder_op = encoder(X)
decoder_op = decoder(encoder_op)

# 预测
y_pred = decoder_op
y_true = X

# 定义代价函数和优化器
cost = tf.reduce_mean(tf.pow(y_true - y_pred, 2))  # 最小二乘法
optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)

with tf.Session() as sess:
    init = tf.global_variables_initializer()
    sess.run(init)
    for epoch in range(training_epochs):
        y, c = sess.run([optimizer, cost], feed_dict={X: s_data})

        if epoch % display_step == 0:
            print("Epoch:", '%04d' % (epoch + 1), "cost=", "{:.9f}".format(c))

    print("Optimization Finished!")

    results = sess.run([weights, biases, encoder_op], feed_dict={X: s_data})

    res_weights = results[0]['encoder_h1']
    res_bias = results[1]['encoder_b1']
    h_data = results[2]

    print(res_weights.reshape(1,6)[0])
    print(res_bias)
    print(h_data.reshape(1,256)[0])







