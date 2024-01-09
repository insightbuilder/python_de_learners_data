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
    rec_list = []
    for ind, x in enumerate(x_list):
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
    t.exitonclick()
    t.mainloop()
