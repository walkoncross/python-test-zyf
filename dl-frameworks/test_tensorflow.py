#!/usr/bin/env python
# encoding: utf-8

import numpy as np

import tensorflow as tf

# N = 批大小, D_in = 输入维数, H = 中间维数, D_out = 输出维数
N, D_in, H, D_out = 3, 2, 2, 1
x0 = np.array([[-0.5, 1], [0.2, -0.6], [0., 0.5]])  # 输入数据
y0 = np.array([[1], [0.2], [0.5]])                  # 输出数据

w1_0 = np.array([[0.5, 0], [-0.5, 1]])              # 第 1 层初始权重
w2_0 = np.array([[-0.5], [0.5]])                    # 第 2 层初始权重

learning_rate = 0.1                                 # 学习速率
n_epoch = 2                                         # 训练 epoch 数

dtype = tf.float32

x = tf.placeholder(dtype, shape=x0.shape)  # 稍后初始化
y = tf.placeholder(dtype, shape=y0.shape)  # 稍后初始化
w1 = tf.Variable(w1_0, dtype=dtype)
w2 = tf.Variable(w2_0, dtype=dtype)

# 定义TensorFlow静态图
h = tf.matmul(x, w1)
h_relu = tf.maximum(h, 0)
y_pred = tf.matmul(h_relu, w2)

loss = tf.reduce_sum((y - y_pred)**2.0) / N

grad_w1, grad_w2 = tf.gradients(loss, [w1, w2])

# 注意 assign_sub会改w1和w2
w1_new = w1.assign_sub(learning_rate * grad_w1)
w2_new = w2.assign_sub(learning_rate * grad_w2)

# 运行TensorFlow静态图

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for t in range(n_epoch):
        loss_, y_pred_, w1_, w2_ = sess.run(
            [loss, y_pred, w1_new, w2_new],
            feed_dict={x: x0, y: y0})

        print('=== EPOCH', t, 'loss', loss_, '===')
        print('out', y_pred_)
        print('w1_new', w1_)
        print('w2_new', w2_, '\n')
