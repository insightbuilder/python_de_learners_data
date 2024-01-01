# Script explores using Turtle along with OOP

from turtle import Turtle, mainloop


if __name__ == '__main__':
    a = Turtle(shape='classic')
    b = Turtle(shape='square')

    a.shapesize(1, 2)
    b.shapesize(1, 1, 1)

    a.penup()
    b.penup()

    a.goto(100, 100)
    b.goto(100, -100)

    a.pendown()
    b.pendown()

    a.circle(50)
    b.circle(200)

    a.write("This is turtle 1")
    b.write("This is turtle b")
    mainloop()

