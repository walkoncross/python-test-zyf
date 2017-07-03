from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'primes',
  ext_modules = cythonize("primes.pyx"),
)