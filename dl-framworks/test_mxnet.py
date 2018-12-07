#!/usr/bin/env python

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


x = nd.array(x0)  # 注意 MXNet 默认即为 float32
y = nd.array(y0)
w1 = nd.array(w1_0)
w2 = nd.array(w2_0)

w1.attach_grad()  # 需要梯度
w2.attach_grad()  # 需要梯度

for t in range(n_epoch):

    with autograd.record():  # 注意 MXNet 默认关闭梯度，在此打开
        y_pred = nd.dot(nd.dot(x, w1).relu(), w2)
        loss = ((y_pred - y) ** 2.0).sum() / N

    loss.backward()

    w1 -= learning_rate * w1.grad
    w2 -= learning_rate * w2.grad

    print('=== EPOCH', t, 'loss', loss, '===')
    print('out', y_pred)
    print('w1_new', w1)
    print('w2_new', w2, '\n')
