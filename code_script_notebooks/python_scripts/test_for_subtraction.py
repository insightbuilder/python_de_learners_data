#!/usr/bin/env python
"""This script will check the subtract function"""

import pytest
from calculations import sub_num

def test_sub():
    assert sub_num(15,10) == 5
