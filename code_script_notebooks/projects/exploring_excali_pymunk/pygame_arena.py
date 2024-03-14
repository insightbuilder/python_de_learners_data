# practice or warmup script before diving into the code creation

import pygame
import pymunk

WIDTH = 600
HEIGHT = 600
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = 100, 0

white_color = [255, 255, 255]
black_color = [0, 0, 0]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]


def coords(point):
    return int(point[0]), int(HEIGHT - point[1])


pygame.init()


class RealBall:
    def __init__(self, x, y, rad) -> None:
        self.rad = rad
        self.body = pymunk.Body()
        self.body.position = coords([x, y])
        self.shape = pymunk.Circle(self.body,
                                   radius=rad,)
        self.shape.density = 1
        self.shape.mass = 1
        space.add(self.shape, self.body)

    def draw(self):
        pygame.draw.circle(display,
                           green,
                           # white_color,
                           self.body.position,
                           self.rad)
        # mg = pygame.image.load("balls.jpg")
        # mg = pygame.transform.scale(mg, (self.rad * 2,
                                         # self.rad * 2))
        # display.blit(mg, self.body.position)


display = pygame.display.set_mode([WIDTH, HEIGHT])


def game():
    b1 = RealBall(x=250, y=300, rad=30)
    b2 = RealBall(x=250, y=200, rad=30)
    b3 = RealBall(x=250, y=100, rad=30)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        display.fill(white_color)
        b1.draw()
        b2.draw()
        b3.draw()
        # mg = pygame.image.load("balls.jpg")
        # mg = pygame.transform.scale(mg, (b1.rad * 2, b1.rad * 2))
        # display.blit(mg, b1.body.position)

        pygame.display.update()
        clock.tick(40)
        space.step(1/40)


game()