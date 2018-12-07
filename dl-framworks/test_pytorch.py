#!/usr/bin/env python

import numpy as np
import torch

# N = 批大小, D_in = 输入维数, H = 中间维数, D_out = 输出维数
N, D_in, H, D_out = 3, 2, 2, 1
x0 = np.array([[-0.5, 1], [0.2, -0.6], [0., 0.5]])  # 输入数据
y0 = np.array([[1], [0.2], [0.5]])                  # 输出数据

w1_0 = np.array([[0.5, 0], [-0.5, 1]])              # 第 1 层初始权重
w2_0 = np.array([[-0.5], [0.5]])                    # 第 2 层初始权重

learning_rate = 0.1                                 # 学习速率
n_epoch = 2                                         # 训练 epoch 数

dtype = torch.float32

x = torch.tensor(x0, dtype=dtype)  # 注意 pytorch 默认即为 float64, 在此设为float32
y = torch.tensor(y0, dtype=dtype)
w1 = torch.tensor(w1_0, dtype=dtype, requires_grad=True)  # 需要梯度
w2 = torch.tensor(w2_0, dtype=dtype, requires_grad=True)  # 需要梯度

w1.attach_grad()  # 需要梯度
w2.attach_grad()  # 需要梯度

for t in range(n_epoch):
    y_pred = x.mm(w1).clamp(min=0).mm(w2)
    loss = (y_pred - y).pow(2.0).sum() / N

    loss.backward()

    with torch.no_grad():  # 注意pytorch默认打开梯度，在此关闭
        w1 -= learning_rate * w1.grad
        w2 -= learning_rate * w2.grad

        w1.grad.zero_()  # 注意pytorch默认累加梯度，在此复位
        w2.grad.zero_()  # 注意pytorch默认累加梯度，在此复位

    print('=== EPOCH', t, 'loss', loss, '===')
    print('out', y_pred)
    print('w1_new', w1)
    print('w2_new', w2, '\n')
