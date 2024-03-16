import pygame
from typing import List, Any

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont('calibri', 18)
FPS = 3
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)


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


display = pygame.display.set_mode([600, 600])


def game(ylist):
    # x = 25
    # y = 25
    frame = 0
    # ref = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        # circles have to be created every frame loop
        # crs = [Circ(display, x + ind * 25, y, 3, 12.5) for ind, val in enumerate(ylist)]
        crs = CircList(data=ylist, x=100, y=75)
        display.fill(white)
        # depending on the frame if we need to update the 
        # position of the circles. Then their positions 
        # have to modified
        # if frame % 5 == 0 and get_frame == 0:  # for all every 10 frames
            # crs[ref].position[1] += 25
            # # take the frame reference
            # get_frame = frame

        # if frame == get_frame + 15:
            # crs[ref].position[1] -= 25
            # ref += 1
            # if ref > len(ylist) - 1:
                # ref = 0
            # get_frame = 0

        # [cr.draw() for cr in crs]  # draw the updated circles
        crs.draw()
        pygame.display.update()
        clock.tick(FPS)
        frame += 1
        print(frame)


nlist = [5, 2, 3, 9, 8, 1]

game(nlist)


# user gives a list with values to be placed inside the circles
# that needs to be rendered on the pygame canvas.
# > Need individual circles that populate the circle_list
# > Need a circle list class or function, better to be a class
# > Class takes the list, and renders first