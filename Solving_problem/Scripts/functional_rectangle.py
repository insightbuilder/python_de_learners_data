# Script will define the function for build rectangles using Turtle
import turtle as t
from turtle import Turtle


def draw_rectangle(myTurtle: Turtle, breadth: int, height: int):
    """Function that draws a rectangle on Turtle Screen."""
    myTurtle.forward(breadth)
    myTurtle.lt(90)
    myTurtle.forward(height)
    myTurtle.lt(90)
    myTurtle.forward(breadth)
    myTurtle.home()


class RectangleMaker():
    def __init__(self, t: Turtle, b: int, h: int, stx: int, sty: int) -> None:
        self.turtle = t
        self.breadth = b
        self.height = h
        self.dist_x = stx
        self.dist_y = sty

    def draw_self(self):
        """Function that draws a rectangle on Turtle Screen."""
        self.turtle.penup()
        self.turtle.goto(self.dist_x, self.dist_y)
        self.turtle.pendown()
        self.turtle.forward(self.breadth)
        self.turtle.lt(90)
        self.turtle.forward(self.height)
        self.turtle.lt(90)
        self.turtle.forward(self.breadth)
        self.turtle.lt(90)
        self.turtle.forward(self.height)
        self.turtle.hideturtle()

if __name__ == "__main__":

    t1 = t.Turtle(shape='classic')
    # breadth = int(input("Provide the breadth of the rectangle: "))
    # height = int(input("Provide the height of the rectangle"))
    #draw_rectangle(myTurtle=t1,
                   #breadth=breadth,
                   #height=height)
    start = input()
    rec1 = RectangleMaker(t1, 50, 100, 10, 10)
    rec2 = RectangleMaker(t1, 70, 200, 50, 50)
    rec3 = RectangleMaker(t1, 90, 150, 100, -120)
    rec1.draw_self()
    rec2.draw_self()
    rec3.draw_self()

    t.mainloop()



