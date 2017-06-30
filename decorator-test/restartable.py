# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 23:06:35 2017

@author: zhaoy
"""

import copy

def generator(i):
    for t in range(i):
        yield t

g = generator(10)
print(list(g))
print(list(g))

class GeneratorRestartHandler(object):
    def __init__(self, gen_func, argv, kwargv):
        self.gen_func = gen_func
        self.argv = copy.copy(argv)
        self.kwargv = copy.copy(kwargv)
        self.local_copy = iter(self)

    def __iter__(self):
        return self.gen_func(*self.argv, **self.kwargv)

    def next(self):
        return next(self.local_copy)

#def restartable(g_func : callable) -> callable:
def restartable(g_func):
    def tmp(*argv, **kwargv):
        return GeneratorRestartHandler(g_func, argv, kwargv)

    return tmp

@restartable
def generator2(i):
    for t in range(i):
        yield t

g = generator2(10)
print(next(g))
print(list(g))
print(list(g))
print(next(g))