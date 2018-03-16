# !/usr/bin/env python
# -*-coding:utf-8-*-


import tensorflow as tf


class AutoEncoder:
    def __init__(self):
        self.learning_rate = 0.01
        self.epochs = 10
        self.inputs = 6
        self.hidden = 1
        self.weights = None
        self.biases = None

    def init_tf(self, fin, fou, epochs=10, l_rate=0.01):
        self.inputs = fin
        self.hidden = fou
        self.epochs = epochs
        self.learning_rate = l_rate
        self.weights = {
            'encoder_h1': tf.Variable(tf.random_normal([self.inputs, self.hidden])),
            'decoder_h2': tf.Variable(tf.random_normal([self.hidden, self.inputs]))
        }
        self.biases = {
            'encoder_b1': tf.Variable(tf.random_normal([self.hidden])),
            'decoder_b2': tf.Variable(tf.random_normal([self.inputs]))
        }
        self.sess = tf.Session()

    def get_results(self, x_data):
        rows, cols = x_data.shape

        X = tf.placeholder('float', [None, self.inputs])
        encoder_op = self.encoder(X)
        decoder_op = self.decoder(encoder_op)
        y_pre = decoder_op
        y_true = X
        cost = tf.reduce_mean(tf.pow(y_true-y_pre, 2))
        optimizer = tf.train.AdadeltaOptimizer(self.learning_rate).minimize(cost)

        init = tf.global_variables_initializer()
        self.sess.run(init)
        for e in range(self.epochs):
            _, c = self.sess.run([optimizer, cost], feed_dict={X: x_data})
            # print(c)

        results = self.sess.run([self.weights, self.biases, encoder_op], feed_dict={X:x_data})
        return {'weights': results[0]['encoder_h1'].reshape(1, cols)[0],
                'biases': results[1]['encoder_b1'][0],
                'inters': results[2].reshape(1, rows)[0]}

    def encoder(self, x):
        return tf.nn.sigmoid(tf.add(tf.matmul(x, self.weights['encoder_h1']), self.biases['encoder_b1']))

    def decoder(self, x):
        return tf.nn.sigmoid(tf.add(tf.matmul(x, self.weights['decoder_h2']), self.biases['decoder_b2']))