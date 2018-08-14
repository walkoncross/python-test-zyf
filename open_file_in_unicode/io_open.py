# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 07:41:14 2018

@author: zhaoy
"""
from __future__ import print_function
import io

fn = './data.txt'

text = u'á'
lines = [u'你好', u'Freddy Rodríguez', u'Alexander Skarsgård']
encoding = 'utf-8'

with io.open(fn, 'w', encoding=encoding, newline='\n') as fout:
    print('Writing:', text)
    fout.write(text + '\n')

    for line in lines:
        print('Writing:', line)
        fout.write(line + '\n')

with io.open(fn, 'r', encoding=encoding, newline='\n') as fin:
    text2 = fin.readline().strip()
    print('type(text2):', type(text2))
    print('Line content:', text2)

    while True:
        line = fin.readline()
        if not line:
            break
        print('Line content:', line.strip())

print('Before writing, text is: ', text)
print('After writing and reading, text is: ', text2)
assert(text == text2)

with io.open(fn, 'r', encoding=encoding, newline='\n') as fin:
    lines2 = fin.readlines()
    print('Line content:', lines2)
    for line in lines2:
        print('Line Read:', line)
