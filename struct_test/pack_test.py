# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 16:44:29 2017

@author: zhaoy
"""

import os
import struct

a = [1,2,3,4,5]
pack_fmt='>5i'

print a
print pack_fmt

pack_a = struct.pack(pack_fmt, *a)
print pack_a

unpack_a = struct.unpack(pack_fmt, pack_a)
print unpack_a