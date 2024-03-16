# Basic rendering 
# Physics space creation
# Interaction between two moving bodies

import pymunk
import pygame

HEIGHT, WIDTH = 500, 600
space = pymunk.Space()
display = pygame.display.set_mode([HEIGHT, WIDTH])
FPS = 30
stp = 1/30
white = [255, 255, 255]
black = [0, 0, 0]
clk = pygame.time.Clock()

def update_coords(point):
    return int(point[0]), int(HEIGHT - point[1])


class RawBall:
    def __init__(self, x, y, radius, velocity, col_type) -> None:
        self.body = pymunk.Body()
        self.body.position = x, y
        self.body.velocity = velocity 
        self.radius = radius
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.density = 1
        self.shape.elasticity = 1
        self.shape.collision_type = col_type
        space.add(self.shape, self.body)

    def draw(self):
        return pygame.draw.circle(display, color=black,
                                  center=update_coords(self.body.position),
                                  radius=self.radius)


class Platform:
    def __init__(self, y, color, col_type) -> None:
        self.color = color
        self.y = y
        self.body = pymunk.Body(pymunk.Body.STATIC)
        self.body.position = 0, y
        self.shape = pymunk.Segment(self.body, [0, 0], [WIDTH, 0], 5)
        self.shape.density = 1
        self.shape.elasticity = 1
        self.shape.collision_type = col_type
        space.add(self.shape, self.body)
  
    def draw(self):
        st = update_coords(self.body.local_to_world(self.shape.a))
        ed = update_coords(self.body.local_to_world(self.shape.b))
        pygame.draw.line(display, self.color, st, ed, 5)


def collide(arbiter, space, data):
    print("Things collide...")


def game():
    b1 = RawBall(100, 50, 30, [0, 100], 1)
    b2 = RawBall(100, 350, 30, [0, -100], 2)
    # plat = Platform(y=70, color=black, col_type=3)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        display.fill(white)
        b1.draw()
        b2.draw()
        # plat.draw()
        pygame.display.update()
        clk.tick(FPS)
        space.step(stp)


game()
