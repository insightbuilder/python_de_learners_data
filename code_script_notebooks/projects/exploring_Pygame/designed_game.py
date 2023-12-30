import pygame
import random
# import below constants are declared by Pygame as constants, 
from pygame.locals import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    RLEACCEL
)
# Create a player object by extending pygame.sprite.Sprite
# Surface drawn on screen is attribute to a player
# define scren dimension constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # self.surf = pygame.Surface((75, 25))
        self.surf = pygame.image.load("jetfighter.png").convert()
        #  The RLEACCEL constant is an optional parameter that helps pygame render more quickly on non-accelerated displays
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
       
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            # move_ip stands for move in_place
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # keeping the player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Define the cloud object by extending pygame.sprite.Sprite
# Use an image for a better-looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        # self.surf = pygame.Surface((20, 10))
        self.surf = pygame.image.load("bullet.png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()  # the kill method is taken from the Sprite class

pygame.init()  # init the environment

# create the screen instance
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# create a custom event for adding enemy
ADDENEMY = pygame.USEREVENT + 1  # The last event pygame reserves is called USEREVENT, so defining ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 750)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 350)
clock = pygame.time.Clock()

# initializing the player
player = Player()
# create group to hold enemy sprite, and another group to hold all_sprites
enemies = pygame.sprite.Group()
all_sprite = pygame.sprite.Group()
all_sprite.add(player)
clouds = pygame.sprite.Group()
running = True
"""
Couple of event dicts
dict_items([('unicode', '9'), ('key', 57), ('mod', 4096), ('scancode', 29), ('window', None)]) : KeyDown
dict_items([('pos', (395, 286)), ('button', 1), ('touch', False), ('window', None)]) : MouseClick
dict_items([('pos', (396, 286)), ('rel', (1, 0)), ('buttons', (0, 0, 0)), ('touch', False), ('window', None)]) : MouseMove
"""
#main loop
while running:
    # look for all events in the queue
    for event in pygame.event.get():
        # print(event.type)  # key player is event object which contains all the data
        # print(event.dict.items())
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                # print(event.dict.items())  # dict_items([('unicode', '\x1b'), ('key', 27), ('mod', 4096), ('scancode', 41), ('window', None)])
                running = False

        elif event.type == QUIT:
            running = False
        
        elif event.type == ADDENEMY:
            # create a new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprite.add(new_enemy)

        # Add a new cloud?
        elif event.type == ADDCLOUD:
            # Create the new cloud and add it to sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprite.add(new_cloud)

        pressed_keys = pygame.key.get_pressed()

        # make the screen white (example commented out)
        # screen.fill((255, 255, 255))
        # make the screen black
        screen.fill((0, 0, 0))

        # create a surface, another way to create / draw shapes
        surf = pygame.Surface((50, 50))
        # make the surface black to seperate it
        surf.fill((0, 0, 0))
        rect = surf.get_rect()
        # print(rect)
        # Commenting out the code to render player
        # do the math to subtract surface center 
        # surf_center = (
            # (SCREEN_WIDTH - surf.get_width())/2,
            # (SCREEN_HEIGHT - surf.get_height())/2
        # )
        #  The term blit stands for Block Transfer, and .blit() is how you copy the contents of one Surface to another.
        # screen.blit(surf, surf_center)

        # screen.blit(player.surf, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        player.update(pressed_keys)
        # update enemy position
        enemies.update()
        # updated cloud position
        clouds.update()
        screen.fill((125, 206, 250))
        # expecting the player to move to top left of screen
        # screen.blit(player.surf, player.rect)
        for entity in all_sprite:
            screen.blit(entity.surf, entity.rect)
        # check if there is a collision
        if pygame.sprite.spritecollideany(player, enemies):
            # if so remove the player and stop the game
            player.kill()
            running = False
        pygame.display.flip()
        clock.tick(45)