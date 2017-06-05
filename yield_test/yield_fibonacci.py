#!/usr/bin/env python
def fibo_generator(n):
    a,b = 0,1
    for i in range(n):
        yield a
        t = b
        b = a + b
        a = t
        
for j in fibo_generator(5):
    print j