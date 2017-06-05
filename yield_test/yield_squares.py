#!/usr/bin/env python
def squares_generator(n):
    for i in range(n):
        yield i*i
        
for j in squares_generator(5):
    print j