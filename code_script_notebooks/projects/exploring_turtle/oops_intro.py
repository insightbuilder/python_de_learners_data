from turtle import Turtle, mainloop


# Class for creating rectangle
class RectangleTurtle(Turtle):
    def __init__(self, length, breadth, stx, sty):
        super().__init__()
        self.length = length
        self.breadth = breadth
        self.startx = stx
        self.starty = sty

    def draw(self):
        self.penup()
        self.goto(self.startx, self.starty)
        self.pendown()
        self.forward(self.length)
        self.right(90)
        self.forward(self.breadth)
        self.right(90)
        self.forward(self.length)
        self.right(90)
        self.forward(self.breadth)
        self.hideturtle()


# Class for creating triangle
class TriangleTurtle(Turtle):
    def __init__(self, height, breadth, stx, sty):
        super().__init__()
        self.height = height
        self.breadth = breadth
        self.startx = stx
        self.starty = sty

    def draw(self):

        self.penup()
        self.goto(self.startx, self.starty)
        self.pendown()
        self.forward(self.breadth)
        cen_x = self.startx + self.breadth / 2
        self.goto(cen_x, self.height)
        self.goto(self.startx, self.starty)
        self.hideturtle()


if __name__ == '__main__':
    rect1 = RectangleTurtle(50, 50, 100, -100)
    rect2 = RectangleTurtle(70, 150, 150, -50)
    rect1.draw()
    rect2.draw()
    tri1 = TriangleTurtle(50, 150, 100, -100)
    tri2 = TriangleTurtle(40, 250, 150, -50)
    tri1.draw()
    tri2.draw()
    mainloop()
