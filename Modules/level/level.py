import pygame
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (112, 128, 144)
RED = (255, 218, 185)
BLUE = (135, 206, 250)

SCREEN_WIDTH = 800

class Level(object):
    """ This is a generic super-class used to define a level. """

    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

        # Background image
        self.background = None

        # How far this world has been scrolled left/right
        self.world_shift = 0
        self.level_limit = -1000

    # Update everythign on this level
    def update(self):
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen) #we might not need enemies, drawn in main loop

    def shift_world(self, shift_x, enemy):
        # Keep track of the shift amount and shift
        self.world_shift += shift_x
        for platform in self.platform_list:
            platform.rect.x += shift_x
        enemy.rect.x += shift_x
