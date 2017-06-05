#!/usr/bin/env python
def fibo_generator():
    a,b = 0,1
    while True:
        yield a
        t = b
        b = a + b
        a = t
        
N = 10
        
fibo_gen = fibo_generator()
for j in range(N):
    print fibo_gen.next()