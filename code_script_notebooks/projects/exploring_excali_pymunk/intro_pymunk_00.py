import pygame
import pymunk
import random
from pygame_utils import (
    get_events_game,
    # Ball,
    draw_obj,
    draw_objects, 
    convert_cords
)


space = pymunk.Space()
pygame.init()
clock = pygame.time.Clock()
FPS = 50


def collide(arbiter, space, data):
    print("Hello...")

class Ball:
    def __init__(self, x, y, collision_type, up=1) -> None:
        self.body = pymunk.Body()  # body is invisible
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, 10)  # shape can be made visible
        self.body.velocity = 0, up * 100
        self.shape.elasticity = 1
        self.shape.collision_type = collision_type
        self.shape.density = 1
        space.add(self.body, self.shape)

    def draw(self):
        pygame.draw.circle(display,
                           (255, 0, 0),
                           convert_cords(self.body.position),
                           10)


display = pygame.display.set_mode([800, 800])


def game():
    ball1 = Ball(100, 100, 1, 1)
    ball2 = Ball(100, 500, 2, -1)
    # handling collisions 
    handler = space.add_collision_handler(1, 2)
    handler.separate = collide
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        display.fill((255, 255, 255))
        ball1.draw()
        ball2.draw()
        pygame.display.update()
        clock.tick(FPS)  # this is for rendering 
        space.step(1/FPS)  # simulation requires to move


game()
# get_events_game()
pygame.quit()
