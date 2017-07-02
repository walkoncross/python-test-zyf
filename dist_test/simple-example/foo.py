'''
    An example module for distutil test
'''


__all__ = ['say_hello', 'add', 'fibo_generator']
__version__ = '1.0'
__author__ = 'zhaoyafei'

def say_hello():
    print("Hello!")

def add(x, y):
    return x+y

def fibo_generator(n):
    a = 0
    b = 1

    for i in range(n):
        t = b
        b = b + a
        yield a

        a = t

if __name__=='__main__':
    print('Call say_hello():')
    say_hello()
    a = 2
    b = 3
    print('add({},{})={}'.format(a, b, add(a,b)))

    n = 10
    fibo_gen = fibo_generator(n)
    print('generating a fibonacci list with length of {}:'.format(n))
    for i in fibo_gen:
        print('\t{}'.format(i))