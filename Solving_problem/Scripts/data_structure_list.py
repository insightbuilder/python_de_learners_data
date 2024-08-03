"""
Sequence Storage:

Problem: Need to store an ordered sequence of elements.
Solution: Lists provide an ordered and mutable collection of elements.
sequence = [1, 2, 3, 4, 5]

Dynamic Size:

Problem: Handling a collection of items with a dynamic size.
Solution: Lists can grow or shrink dynamically.
dynamic_list = [10, 20, 30]
dynamic_list.append(40)

Iteration and Indexing:

Problem: Iterating over elements and accessing them by index.
Solution: Lists support iteration and indexing.
for item in my_list:
    print(item)

Sorting:

Problem: Need to sort a collection of elements.
Solution: Lists have built-in sorting capabilities.
sorted_list = sorted(my_list)

Filtering and Selection:

Problem: Selecting elements based on certain criteria.
Solution: Lists can be filtered using list comprehensions.
selected_items = [item for item in my_list if item > 10]

Stack and Queue Operations:

Problem: Need to perform stack (last-in, first-out) or queue (first-in, first-out) operations.
Solution: Lists can be used as stacks or queues.

stack = []
stack.append(1)
stack.pop()

queue = []
queue.append(1)
queue.pop(0)

Combining Lists:

Problem: Combining multiple lists into one.
Solution: Lists can be concatenated.
combined_list = list1 + list2

Searching:

Problem: Finding the index of a specific element.
Solution: Lists support the index() method.
index = my_list.index(42)

Duplicating Elements:

Problem: Need to duplicate elements in a list.
Solution: Lists can be replicated.
duplicated_list = [0] * 5

Slicing:

Problem: Extracting a portion of a list.
Solution: Lists support slicing.
sub_list = my_list[2:5]

Counting Occurrences:

Problem: Counting occurrences of specific elements.
Solution: Lists have the count() method.
count = my_list.count(42)

Removing Elements:

Problem: Removing specific elements from a list.
Solution: Lists provide methods like remove() and pop().
my_list.remove(42)
"""

import turtle as t
from turtle import Turtle


class RectangleTurtle():
    def __init__(self,
                 x_cord: int,
                 y_cord: int,
                 length: int,
                 breadth: int,
                 name: str):
        self.turtle = Turtle()
        self.length = length
        self.breadth = breadth
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.name = name

    def draw_self(self):
        self.turtle.pencolor('red')   # color of the border (const)
        self.turtle.pensize(2)   # pensize  (const)
        self.turtle.penup()
        self.turtle.goto(self.x_cord, self.y_cord)
        self.turtle.pendown()
        self.turtle.forward(self.length)  # length of rect
        self.turtle.rt(90)
        self.turtle.forward(self.breadth)  # breadth of rect
        self.turtle.rt(90)
        self.turtle.forward(self.length)
        self.turtle.goto(self.x_cord, self.y_cord)
        self.turtle.hideturtle()

    def destroy_self(self):
        self.turtle.clear()
        self.turtle.hideturtle()

    def give_dims(self):
        self.turtle.penup()
        x_text = self.x_cord + (self.length / 2)
        y_text = self.y_cord - (self.breadth / 2)
        self.turtle.goto(x_text, y_text)
        self.turtle.pendown()
        self.turtle.write(f"""The length of {self.name} rectangle 
                        is {self.length} & breadth is {self.breadth}""")

    def locate_home(self):
        self.turtle.penup()
        x_text = self.x_cord + 15
        y_text = self.y_cord + 15 
        self.turtle.pendown()
        self.turtle.goto(x_text, y_text)
        self.turtle.write(f"""The x_ord of {self.name} rectangle 
                          is {self.x_cord} & y_ord is {self.y_cord}""")


if __name__ == '__main__':
    t1 = t.Turtle('turtle')  # we have to initialize
    wait = input('Bring turtle window to view and press enter.')
    t.setup(900, 600)
    # What is a List? Its a collection of things. 
    x_list = [10, 55, -115, -210]
    y_list = [20, 60, 125, 210]
    # What problem it solves? Collecting stuff & providing ways to accessing stuff 
    # x_list.append()
    rec_list = []
    for ind, x in enumerate(x_list):
        # print(ind, x)
        # enumerate the list of co-ordinates & append to rec_list
        rec_list.append(RectangleTurtle(breadth=200,
                                        length=300,
                                        x_cord=x,
                                        y_cord=y_list[ind],
                                        name=f'rect_{ind}'))
        # enumerate on the rectangle objects and draw them
        rec_list[ind].draw_self()
        # enumerate on the rectangle objects and get their dims
        rec_list[ind].give_dims()
        rec_list[ind].destroy_self()
        rec_list[ind].draw_self()
    t.exitonclick()
    t.mainloop()
