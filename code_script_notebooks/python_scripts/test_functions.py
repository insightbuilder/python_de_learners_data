#!/usr/bin/env python
'''This test suite will be used on calculations.py module'''

import pytest
from calculations import *

def test_add():
    assert add_num(5,7) == 12

@pytest.mark.parametrize("x, y, result",[
    (50, 30, 1500),
    (15,7,105),
    (7,6,42)
    ])
def test_mul(x,y,result):
    print('testing mul')
    assert mul_num(x,y) == result

def test_mean():
    assert mean_num(5,2,7,10) == 6  

def test_mean2():
    assert mean_num(15,12,71,110) == 6

def test_mul1():
    assert mul_num(5,8) == 40


