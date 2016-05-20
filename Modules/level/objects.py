import pygame
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (112, 128, 144)
RED = (255, 218, 185)
BLUE = (135, 206, 250)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()

        self.image = pygame.Surface([50, 50])
        self.image.fill(GREY)

        self.rect = self.image.get_rect()