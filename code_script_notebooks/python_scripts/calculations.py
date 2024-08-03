#!/usr/bin/env python

def add_num(a, b):
    return a + b

def mul_num(a, b):
    return a * b

def mean_num(*a):
    length = len(a)
    print(sum(a)/length)
    return sum(a)/length

def sub_num(a,b):
    return a - b
