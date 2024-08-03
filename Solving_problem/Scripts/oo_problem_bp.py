# Script contains the Class that encapsulates 
# various problems that can be solved using 
# object oriented programming paradigm
import sys
import turtle as t
from procedural_rectangle import RectangleTurtle


class Challenge(object):
    def __init__(self, description, features, interaction, abilities) -> None:
        self.description = description
        self.features = features
        self.interaction = interaction
        self.abilities = abilities

    def __str__(self) -> str:
        return f"Challenge Description: {self.description}"

    def show_features(self):
        return f"Features are: {','.join(self.features)}"

    def show_interaction(self):
        return f"Interactions are: {','.join(self.interaction)}"

    def show_abilities(self):
        return f"Abilities are: {','.join(self.abilities)}"


class RectangleBP(object):
    def __init__(self, x_c=0.0, y_c=0.0, length=100, breadth=159,
                 name='default'):
        self.x_cord = x_c
        self.y_cord = y_c
        self.length = length
        self.breadth = breadth
        self.name = name
        self.connected_with = []
   
    def connect_with(self, other):
        if isinstance(other, RectangleBP):
            # connect self with other
            self.connected_with.append(other)
            # self becomes part of other's connection
            other.connected_with.append(self)
            print(f"{self.name} is connected with {other.name}")
        else:
            print('Not a Rectangle. Cannot connect')

    def get_other_center(self, other):
        if other in self.connected_with:
            print(other.x_cord, other.y_cord)
        else:
            print("Not connected, cannot get center")


class NewRectangle(RectangleBP):
    def __init__(self, color):
        super().__init__()
        self.color = color
    
    def print_color(self):
        print(self.color)

if __name__ == '__main__':
    rec1 = RectangleBP(x_c=0, y_c=0,
                       length=50, breadth=35,
                       name='rec1')
    rec2 = RectangleBP(x_c=100, y_c=150,
                       length=35, breadth=45,
                       name='rec2')
    rec3 = RectangleBP(x_c=200, y_c=250,
                       length=75, breadth=55,
                       name='rec3')
    rec4 = RectangleBP(x_c=20, y_c=30,
                       length=75, breadth=15,
                       name='rec4')
    
    rec4Kolor = NewRectangle(color='Green')
    
    rec4Kolor.print_color()
    rec4Kolor.connect_with(rec1)
    rec4Kolor.get_other_center(rec1)

    rec1.connect_with(rec2)  # can get other's detail
    rec1.get_other_center(rec2)
    rec1.get_other_center(rec3)

    # build two rectangles
    rect1 = RectangleTurtle(x_cord=0,
                            y_cord=0,
                            length=50,
                            breadth=35,
                            name='rect1')
    rect2 = RectangleTurtle(x_cord=100,
                            y_cord=150,
                            length=35,
                            breadth=45,
                            name='rect2')
    say = input("Press enter to start: ")
    if say == '0':
        sys.exit()
    rect1.draw_self()  # draw self
    rect2.draw_self()  # draw self
    # connect each other
    rect1.connect_centers(rect2)
    t.mainloop()
