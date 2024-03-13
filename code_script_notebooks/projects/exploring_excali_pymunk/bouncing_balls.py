import pymunk
import pygame

pygame.init()

display = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = 0, -1000  # this is interesting
FPS = 60


def convert_coordinates(point):
    return int(point[0]), int(800 - point[1])


# ball body and shape creation
ball_rad = 40
body = pymunk.Body()
body.position = 400, 600
shape = pymunk.Circle(body, ball_rad)
shape.density = 1
shape.elasticity = 1
space.add(body, shape)

# line segment shape creation, and making it static
seg_body = pymunk.Body(body_type=pymunk.Body.STATIC)
seg_shape = pymunk.Segment(seg_body, (0, 250), (800, 50), 5)
seg_shape.elasticity = 1
space.add(seg_body, seg_shape)

mge = pygame.image.load("balls.jpg")
mge = pygame.transform.scale(mge, (ball_rad * 2, ball_rad * 2))


def game():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        display.fill((255, 255, 255))
        x, y = convert_coordinates(body.position)
        pygame.draw.circle(display, (255, 255, 255), (x, y),
                           radius=ball_rad)
        display.blit(mge, (x, y))
        pygame.draw.line(display, (0, 0, 0), (0, 550), (800, 750), 5)
        pygame.display.update()
        clock.tick(30)
        space.step(1/FPS)


game()
pygame.quit()