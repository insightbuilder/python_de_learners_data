#!/usr/bin/env python
"""This program prints Integers, Floats, Strings separately and together!!!"""

#Creating variables is done by assigning values to letters/words/sentences

x = 26
y = 57

print(x, y)

print('Using sep keyword')

print(x, y, sep=',')

print('using end keyword with \n')

print(x, y, sep =',', end ='\n')

print('using end keyword with \t')

print(x, y, sep =',', end ='\t')

print('mixing strings and numbers')

print('X is =', x, 'Y is =', y, sep =',')

print('There are 2 other ways to mix string with other variable types')

print('Using Format')

print("Sum of {} of {} is {}".format(x,y, x+y))

print('Using f')

print(f"Sum of {x} and {y} is {x+y}")

