#!/usr/bin/env python
# encoding: utf-8

import numpy as np

import mxnet as mx
from mxnet import nd, autograd

# N = 批大小, D_in = 输入维数, H = 中间维数, D_out = 输出维数
N, D_in, H, D_out = 3, 2, 2, 1
x0 = np.array([[-0.5, 1], [0.2, -0.6], [0., 0.5]])  # 输入数据
y0 = np.array([[1], [0.2], [0.5]])                  # 输出数据

w1_0 = np.array([[0.5, 0], [-0.5, 1]])              # 第 1 层初始权重
w2_0 = np.array([[-0.5], [0.5]])                    # 第 2 层初始权重

learning_rate = 0.1                                 # 学习速率
n_epoch = 2                                         # 训练 epoch 数


x = x0.copy()
y = y0.copy()
w1 = w1_0.copy()
w2 = w2_0.copy()


for t in range(n_epoch):
    h = x.dot(w1)
    h_relu = np.maximum(h, 0)

    y_pred = h_relu.dot(w2)

    loss = np.square(y_pred - y).sum() / N

    grad_y_pred = 2.0 * (y_pred - y) / N
    grad_w2 = h_relu.T.dot(grad_y_pred)
    grad_h_relu = grad_y_pred.dot(w2.T)
    grad_h = grad_h_relu.copy()
    grad_h[h < 0] = 0
    grad_w1 = x.T.dot(grad_h)

    w1 -= learning_rate * grad_w1
    w2 -= learning_rate * grad_w2

    print('=== EPOCH', t, 'loss', loss, '===')
    print('out', y_pred)
    print('w1_new', w1)
    print('w2_new', w2, '\n')
