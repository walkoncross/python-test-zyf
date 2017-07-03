from libc.math cimport sin

cdef double f(double x):
    return sin(x)

def cfunc_sin(x):
    return f(x)