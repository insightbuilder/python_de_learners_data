import os
from util import get_path

# def get_path(filename):
#     """Return file path or empty string if no path"""
#     head, tail = os.path.split(filename)
#     import pdb; pdb.set_trace()
#     return head
# above function is moved to util.py module 

filename = __file__
# below drops the script into debugger mode
# breakpoint()
print(f"path: {filename}")
# learnt about the n commmand to execute next line of code, 
# use ll to list the source of the code
# use p to print the variable name
# we can use the python script_name.py will run the script and stop at breakpoint()

print(f"path: {get_path(filename)}")

# Note the lines --Call-- and --Return--. This is pdb letting you know why 
# execution was stopped. n (next) and s (step) will stop before a 
# function returns. That’s why you see the --Return-- lines above.

# There is optional 2nd argument to b: condition. This is very powerful.
# Imagine a situation where you wanted to break only if a
# certain condition existed.

# one can disable and enable breakpoint