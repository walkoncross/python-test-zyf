# -*- coding: utf-8 -*-
"""
Created on Thu May 25 05:28:01 2017

@author: zhaoy
"""

import multiprocessing


def funSquare(num):
    return num ** 2


# Commenting the following 'if'-clause will raise exception on Windows
if __name__ == '__main__':
    pool = multiprocessing.Pool()
    results = pool.map(funSquare, range(10))
    print(results)
