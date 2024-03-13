import pygame
import pymunk

pygame.init()

display = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
space = pymunk.Space()
FPS = 100


def convert_coords(point):
    return int(point[0]), int(600 - point[1])


class Ball:
    def __init__(self, x, color, group, velocity) -> None:
        self.color = color
        self.body = pymunk.Body()
        self.body.position = x, 500
        self.body.velocity = velocity 
        self.shape = pymunk.Circle(self.body, 15)
        self.shape.density = 1
        self.shape.elasticity = 1
        # groups are way of ignoring collisions
        self.shape.filter = pymunk.ShapeFilter(group=group)
        space.add(self.body, self.shape)

    def draw(self):
        pos = self.body.position
        pygame.draw.circle(display, self.color,
                           convert_coords(pos), 15)


class Platform:
    def __init__(self, y, color, group) -> None:
        self.color = color
        self.y = y
        self.body = pymunk.Body(pymunk.Body.STATIC)
        self.body.position = 0, y
        self.shape = pymunk.Segment(self.body, [0, 0], [600, 0], 10)
        self.shape.density = 1
        self.shape.elasticity = 1
        self.shape.filter = pymunk.ShapeFilter(group=group)
        space.add(self.body, self.shape)
    
    def draw(self):
        a = convert_coords(self.body.local_to_world(self.shape.a))
        b = convert_coords(self.body.local_to_world(self.shape.b))
        pygame.draw.line(display, self.color, a, b, 10)

# There are other ways to control the interactions between the 
# various objects. Need to understand the 
# bitmask applied on them in the csv file
# strange interactions happen, as keeping track what will 
# occur is bit more challenging...

def game():
    bal1 = Ball(150, (255, 0, 0), 2, (100, 0))
    bal2 = Ball(250, (255, 255, 0), 2, (0, 0))
    bal3 = Ball(450, (255, 0, 255), 4, (-200, 0))
    pl1 = Platform(300, (0, 0, 0,), 1)
    pl2 = Platform(100, (255, 150, 0,), 1)
    # After setting these to group 1, 
    # the platforms & balls dont interact. 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        display.fill((255, 255, 255))
        bal1.draw()
        bal2.draw()
        bal3.draw()
        pl1.draw()
        pl2.draw()
 
        pygame.display.update()
        clock.tick(89)
        space.step(1/FPS)


game()
pygame.quit()
