# -*- coding: utf-8 -*-
"""
Created on Wed Jul 05 21:32:25 2017

@author: zhaoy
"""

import math


class Square(object):
    """A square with two properties: a writable area and a read-only perimeter.

    To use:
    >>> sq = Square(3)
    >>> sq.area
    9
    >>> sq.perimeter
    12
    >>> sq.area = 16
    >>> sq.side
    4
    >>> sq.perimeter
    16
    """

    def __init__(self, side):
        self.side = side

    def __get_area(self):
        """Calculates the 'area' property."""
        return self.side ** 2

    def ___get_area(self):
        """Indirect accessor for 'area' property."""
        return self.__get_area()

    def __set_area(self, area):
        """Sets the 'area' property."""
        self.side = math.sqrt(area)

    def ___set_area(self, area):
        """Indirect setter for 'area' property."""
        self.__set_area(area)

    area = property(___get_area, ___set_area,
                    doc="""Gets or sets the area of the square.""")

    @property
    def perimeter(self):
        return self.side * 4


sq_a = Square(5)
print(sq_a.area)
print(sq_a.perimeter)

sq_a.area = 49
print(sq_a.area)
print(sq_a.perimeter)
