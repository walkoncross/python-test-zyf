#!/usr/bin/env python
# encoding: utf-8

import numpy as np

import tensorflow as tf
import tensorflow.contrib.eager as tfe

tfe.enable_eager_execution()  # 打开eager模式

# N = 批大小, D_in = 输入维数, H = 中间维数, D_out = 输出维数
N, D_in, H, D_out = 3, 2, 2, 1
x0 = np.array([[-0.5, 1], [0.2, -0.6], [0., 0.5]])  # 输入数据
y0 = np.array([[1], [0.2], [0.5]])                  # 输出数据

w1_0 = np.array([[0.5, 0], [-0.5, 1]])              # 第 1 层初始权重
w2_0 = np.array([[-0.5], [0.5]])                    # 第 2 层初始权重

learning_rate = 0.1                                 # 学习速率
n_epoch = 2                                         # 训练 epoch 数

dtype = tf.float32

x = tf.Variable(x0, dtype=dtype)
y = tf.Variable(y0, dtype=dtype)
w1 = tf.Variable(w1_0, dtype=dtype)
w2 = tf.Variable(w2_0, dtype=dtype)

for t in range(n_epoch):
    with tf.GradientTape() as tape:  # 记录梯度
        h = tf.matmul(x, w1)
        h_relu = tf.maximum(h, 0)
        y_pred = tf.matmul(h_relu, w2)

        loss = tf.reduce_sum((y - y_pred)**2.0) / N

        grad_w1, grad_w2 = tape.gradients(loss, [w1, w2])

        # 注意 assign_sub会改w1和w2
        w1_new = w1.assign_sub(learning_rate * grad_w1)
        w2_new = w2.assign_sub(learning_rate * grad_w2)
