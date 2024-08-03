# import and initialize pygame library
import pygame
pygame.init()  # This function calls the separate init() functions of all the included pygame modules

screen = pygame.display.set_mode([500, 500])  # set the display

running = True

while running:
    # check the events on the pygame window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update the screen bg with white
    screen.fill((255, 255, 255))

    # draw a circle
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # flip the display, is important call
    # without this, nothing appears on the screen
    pygame.display.flip()

pygame.quit()
