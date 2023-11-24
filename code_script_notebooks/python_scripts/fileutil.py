def get_path(fname):
    """Return file's path or empty string if no path."""
    import os
    import pdb; pdb.set_trace()
    head, tail = os.path.split(fname)
    return head

    # testing the display commands along with 
    # You can use the two commands u (up) and d (down) to change the current frame. Combined with p, this allows you to inspect variables and state in your application at any point along the call stack in any frame.
    # h followed by w / p / c etc to get the 
"""
Command	Description
p	Print the value of an expression.
pp	Pretty-print the value of an expression.
n	Continue execution until the next line in the current function is reached or it returns.
s	Execute the current line and stop at the first possible occasion (either in a function that is called or in the current function).
c	Continue execution and only stop when a breakpoint is encountered.
unt	Continue execution until the line with a number greater than the current one is reached. With a line number argument, continue execution until a line with a number greater or equal to that is reached.
l	List source code for the current file. Without arguments, list 11 lines around the current line or continue the previous listing.
ll	List the whole source code for the current function or frame.
b	With no arguments, list all breaks. With a line number argument, set a breakpoint at this line in the current file.
w	Print a stack trace, with the most recent frame at the bottom. An arrow indicates the current frame, which determines the context of most commands.
u	Move the current frame count (default one) levels up in the stack trace (to an older frame).
d	Move the current frame count (default one) levels down in the stack trace (to a newer frame).
h	See a list of available commands.
h <topic>	Show help for a command or topic.
h pdb	Show the full pdb documentation.
q	Quit the debugger and exit.   
"""