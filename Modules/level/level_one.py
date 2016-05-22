import pygame
import math
from .objects import Platform
from .level import Level

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (112, 128, 144)
RED = (255, 218, 185)
BLUE = (135, 206, 250)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create platforms for the level
class Level_01(Level):

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -1500

        # Array with width, height, x, and y of platform
        level = [[600, 40, 300, 500],
                 [600, 40, 700, 480]]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            self.platform_list.add(block)
