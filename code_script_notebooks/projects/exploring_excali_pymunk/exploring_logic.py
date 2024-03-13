import pygame

pygame.init()
clock = pygame.time.Clock()
FPS = 3

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


display = pygame.display.set_mode([600, 600])


def game(ylist):
    x = 25
    y = 25
    frame = 0
    ref = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        # circles have to be created every frame loop
        crs = [Circ(display, x + ind * 25, y, 3, 12.5) for ind, val in enumerate(ylist)]
        display.fill((0, 0, 255))
        # depending on the frame if we need to update the 
        # position of the circles. Then their positions 
        # have to modified
        if frame % 5 == 0 and get_frame == 0: # for all every 10 frames
            crs[ref].position[1] += 25
            # take the frame reference
            get_frame = frame

        if frame == get_frame + 15:
            crs[ref].position[1] -= 25
            ref += 1
            if ref > len(ylist) - 1:
                ref = 0
            get_frame = 0

        [cr.draw() for cr in crs]  # draw the updated circles
        pygame.display.update()
        clock.tick(FPS)
        frame += 1
        print(frame)

nlist = [5, 2, 3, 9, 8, 1]

game(nlist)