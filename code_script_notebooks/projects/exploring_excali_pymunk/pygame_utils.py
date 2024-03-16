import pygame
import pymunk
import random
from typing import List, Any


clock = pygame.time.Clock()
FPS = 50
space = pymunk.Space()
display = pygame.display.set_mode([100, 100])


def get_events_game():
    while True:
        for event in pygame.event.get():
            print('start event: ', event)
            print("Mouse Related Events: ")
            try:
                print('M_pos', event.dict['pos'])
                print('M_relm', event.dict['rel'])
                print('M_button', event.dict['buttons'])
                print('touches', event.dict['touch'])
                print('window', event.dict['window'])
            except Exception as e:
                print('Wait for the event...', e)
            print("KB Related Events: ")
            try:
                print("Unicode press", event.dict['unicode'])
                print("key press", event.dict['key'])
                print("Scancode", event.dict['scancode'])
                if 'mod' in event.dict:
                    print("mod", event.dict['mod'])
            except Exception as e:
                print('Await KB event: ', e)
            if event.type == pygame.QUIT:
                return

        pygame.display.update()

        clock.tick(FPS)


def draw_obj(pyg_obj):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        pyg_obj.display.fill((255, 255, 255))
        pyg_obj.draw()
        pygame.display.update()

        clock.tick(FPS)


def draw_objects(pyg_list):
    if len(pyg_list) == 1:
        print('Use draw_obj function')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        pyg_list[0].display.fill((255, 255, 255))
        for ind, pyg in enumerate(pyg_list):
            print(f'Rendering {ind} obj')
            pyg.draw()

        pygame.display.update()

        clock.tick(FPS)


def convert_cords(point):
    return int(point[0]), 600 - int(point[1])


class Ball:
    def __init__(self, x, y, display) -> None:
        self.body = pymunk.Body()  # body is invisible
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, 10)  # shape can be made visible
        self.body.velocity = random.uniform(-100, 100), random.uniform(-100, 100)
        self.shape.elasticity = 1
        self.shape.density = 1
        self.display = display
        space.add(self.body, self.shape)

    def draw(self):
        pygame.draw.circle(self.display,
                           (255, 0, 0),
                           convert_cords(self.body.position),
                           10)


class Circ:
    def __init__(self, val, x, y, thick, rad) -> None:
        self.position = [x, y]
        self.val = val
        self.thick = thick
        self.rad = rad
    
    def draw(self):
        pygame.draw.circle(display,
                           (255, 255, 255),
                           self.position,
                           self.rad,
                           self.thick)


class CircList:
    def __init__(self, data: List[Any], x, y) -> None:
        self.start_position = x, y
        self.data = data
        self.circles = [Circ(v, x + ind * 2 * 25, y, 3, 25) for ind,
                        v in enumerate(self.data)]
        # create the text and render it as images list
        self.val_text = [font.render(str(val),
                                     True,
                                     blue) for val in self.data]

    def draw(self):
        [pygame.draw.circle(display,
                            black,
                            circle.position,
                            circle.rad,
                            circle.thick) for circle in self.circles]
        x, y = self.start_position  # get the start position
        # blit the text on to the center of the circles
        [display.blit(img, (x + ind * 2 * 25, y)) for ind,
         img in enumerate(self.val_text)]