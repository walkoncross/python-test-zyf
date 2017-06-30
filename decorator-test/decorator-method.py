# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 23:06:35 2017

@author: zhaoy
"""

# first format
#def p_decorate(func):
#   def func_wrapper(self):
#       return "<p>{0}</p>".format(func(self))
#   return func_wrapper


# second format, could decorate both functions and class methods
def p_decorate(func):
   def func_wrapper(*args, **kwargs):
       return "<p>{0}</p>".format(func(*args, **kwargs))
   return func_wrapper

class Person(object):
    def __init__(self):
        self.name = "John"
        self.family = "Doe"

    @p_decorate
    def get_fullname(self):
        return self.name+" "+self.family


my_person = Person()
print my_person.get_fullname()