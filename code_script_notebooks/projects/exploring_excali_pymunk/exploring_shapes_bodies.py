# The script explores the shapes and bodies inside PyMunk
# How it is placed on the Pygame canvas
import pygame


def convert_coords(point, height):
    return int(point[0]), int(height - point[1])


pygame.init()
clock = pygame.time.Clock()
FPS = 60
black_color = [0, 0, 0]
white_color = [255, 255, 255]
HEIGHT = 600
WIDTH = 600

class Square:
    def __init__(self, side, value, x, y) -> None:
        self.side = side
        self.value = value
        self.position = (x, y)
    
    def draw(self):
        left = self.position[0]
        top = self.position[1]
        pygame.draw.rect(display,
                         black_color,
                         [left, top,self.side, self.side],
                         2)

class Circle:
    def __init__(self, radius, value, x, y) -> None:
        self.radius = radius 
        self.value = value
        self.position = (x, y)
    
    def draw(self):
        left = self.position[0]
        top = self.position[1]
        pygame.draw.circle(display,
                         black_color,
                         self.position,
                         self.radius,
                         3)

display = pygame.display.set_mode([WIDTH, HEIGHT])


def game():
    sq1 = Square(side=25, value=50, x=25, y=25)
    sq2 = Square(side=25, value=7, x=50, y=25)
    circ1 = Circle(25, value=6, x=50, y=75)
    # sq3 = Square(side=25, value=7, x=75, y=25)
    x = 25
    y = 25
    l_test = [5, 2, 7, 3, 4]
    sqrs = [Square(25, val, x + ind * 25, y) for ind, val in enumerate(l_test)]
    sqrs_v = [Square(25, val, x , y + ind * 25) for ind, val in enumerate(l_test)]
    circ1.draw()
    cx = 100
    cy = 100
    crcls = [Circle(25, val, cx + ind * 25, cy) for ind, val in enumerate(l_test)]
    crc_vs = [Circle(25, val, cx,  cy + ind * 25) for ind, val in enumerate(l_test)]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        display.fill(white_color)
        [sq.draw() for sq in sqrs]
        [sq.draw() for sq in sqrs_v]
        [cr.draw() for cr in crc_vs]
        [cr.draw() for cr in crcls]
        pygame.display.update()
        clock.tick(FPS)


game()
