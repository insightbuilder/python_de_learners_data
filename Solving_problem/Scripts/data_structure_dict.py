"""
Fast Lookup:
Problem: Efficiently look up values associated with specific keys.
Solution: Use a dictionary where keys are associated with corresponding values, allowing O(1) average time complexity for lookups.

Counting Occurrences:
Problem: Count the occurrences of elements in a collection.
Solution: Use a dictionary to store elements as keys and their counts as values.

text = "example text"
char_count = {}
for char in text:
    char_count[char] = char_count.get(char, 0) + 1
Grouping Data:
Problem: Group data based on a common attribute.
Solution: Use a dictionary with the common attribute as keys and lists of corresponding items as values.

data = [{"category": "A", "value": 10}, {"category": "B", "value": 20}]
grouped_data = {}
for item in data:
    category = item["category"]
    if category not in grouped_data:
        grouped_data[category] = []
    grouped_data[category].append(item)

Storing Configuration Settings:
Problem: Store and retrieve configuration settings.
Solution: Use a dictionary to map configuration keys to their corresponding values.
config = {"debug": True, "max_connections": 100}

Caching Results:
Problem: Cache expensive function or computation results.
Solution: Use a dictionary to store results with input parameters as keys.
cache = {}

def expensive_function(x):
    if x not in cache:
        # Perform expensive computation
        result = x * x
        cache[x] = result
    return cache[x]

Mapping Unique Identifiers:
Problem: Map unique identifiers to corresponding objects.
Solution: Use a dictionary with identifiers as keys and corresponding objects as values.
user_mapping = {"user1": user_object1, "user2": user_object2}

Default Values and Settings:
Problem: Set default values or configurations.
Solution: Use a dictionary with default settings and update as needed.
default_settings = {"debug": False, "log_level": "info"}
user_settings = {}
user_settings.update(default_settings)
user_settings["debug"] = True

Bi-Directional Mapping:
Problem: Map both keys to values and values to keys.
Solution: Use a dictionary for the primary mapping and create a reversed dictionary for the inverse mapping.
mapping = {"key1": "value1", "key2": "value2"}
reverse_mapping = {v: k for k, v in mapping.items()}
"""

from enum import Enum
import turtle as t
from turtle import Turtle

# Script contains the supporting code introducing Dictionaries

empty_dict = {}
# empty_dict = dict({})
student = {"name": "John", "age": 20, "grade": 85}

person = {"name": "Alice", "age": 30, "is_student": False}

contact = {"name": "Bob", "address": {"city": "New York", "zipcode": "10001"}}

fruits = {"name": "Apple", "colors": ["red", "green"], "taste": "sweet"}

coordinates = {(1, 2): "point A", (3, 4): "point B"}

squares = {1: 1, 2: 4, 3: 9, 4: 16}

prices = {"apple": 1.99, "banana": 0.99, "orange": 2.49}

flags = {"is_active": True, "has_permission": False}

squares = {x: x**2 for x in range(5)}

data = {"name": "Sam", "age": 25, "grades": [90, 85, 88], "is_student": True}

info = {"name": "Alex", "address": None, "phone": "123-456-7890"}

symbols = {"$": "Dollar", "@": "At", "&": "Ampersand"}

operations = {"add": lambda x, y: x + y, "multiply": lambda x, y: x * y}

age_mapping = {18: "Adult", 12: "Child", 65: "Senior"}

names = {"John": 25, "Alice": 30, "Bob": 22}

coordinates = {(1, 2): "Point A", (3, 4): "Point B"}

data = {None: "No value", "key": "Some value"}

mixed_keys = {("John", 25): "Person", "Apple": 1.99, 42: "Answer"}

frozen_set_keys = {frozenset([1, 2]): "Set A", frozenset([3, 4]): "Set B"}


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


points = {Point(1, 2): "Point A", Point(3, 4): "Point B"}


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


colors = {Color.RED: "R", Color.GREEN: "G", Color.BLUE: "B"}

binary_data = {b'key1': "Value 1", b'key2': "Value 2"}

hashable_functions = {hash: "Hash Function", len: "Length Function"}


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


t1 = t.Turtle('turtle')  # we have to initialize
t.setup(900, 600)
# What is a Dict? Its a collection of things mapped with each other. 
coord_dict = {"uno": [0, 0],
              "Duo": [50, 50],
              "Trio": [100, 100],
              "Quatro": [150, 150],
              "Penta": [200, 200]
              }
# What problem it solves? Collecting stuff & providing ways to accessing stuff 
# x_list.append()
rec_dict = {}
key_list = list(coord_dict.keys())
print(key_list)
for ind, x in enumerate(key_list):
    # print(ind, x)
    # enumerate the list of co-ordinates & append to rec_list
    rec_dict[key_list[ind]] = (RectangleTurtle(breadth=200, length=300,
                                               x_cord=coord_dict[key_list[ind]][0],
                                               y_cord=coord_dict[key_list[ind]][1],
                                               name=f'rect_{key_list[ind]}'))
