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
    return True

class Ball:
    def __init__(self, x, y, collision_type, up=1) -> None:
        self.body = pymunk.Body()  # body is invisible
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, 10)  # shape can be made visible
        self.body.velocity = random.uniform(-100, 100), random.uniform(-100,
                                                                        100)
        # self.body.velocity = 0, up * 100
        self.shape.elasticity = 1
        self.shape.collision_type = collision_type
        self.shape.density = 1
        space.add(self.body, self.shape)

    def draw(self):
        if self.shape.collision_type != 2:
            pygame.draw.circle(display,
                            (255, 0, 0),
                            convert_cords(self.body.position),
                            10)
        else:
            pygame.draw.circle(
                display,
                (0, 255, 0),
                convert_cords(self.body.position),
                15
            )
    
    def change_to_blue(self, arbiter, space, data):
        print("hit shot...")
        self.shape.collision_type = 2


display = pygame.display.set_mode([800, 800])


def game():
    ball_list = [Ball(random.randint(0, 600),
                      random.randint(0, 600), ct+3) for ct in range(100)]
    ball_list.append(Ball(300, 300, 2))
    handlers = [space.add_collision_handler(2, i+3) for i in range(100)]
    for i, hand in enumerate(handlers):
        hand.separate = ball_list[i].change_to_blue

    # handler = space.add_collision_handler(1, 2)
    # handler.begin = collide
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        display.fill((255, 255, 255))
        [ball.draw() for ball in ball_list]
        pygame.display.update()
        clock.tick(FPS)  # this is for rendering 
        space.step(1/FPS)  # simulation requires to move


game()
# get_events_game()
pygame.quit()
