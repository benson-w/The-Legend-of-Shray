import pygame
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (112, 128, 144)
RED = (255, 218, 185)
BLUE = (135, 206, 250)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Enemy1(pygame.sprite.Sprite):
    '''
        not sure what to add in the parent enemy class
    '''

    def __init__(self):

        # Call the parent's constructor
        super().__init__()

        self.percentage = 100

        #give size, image attributes
        width = 75
        height = 75
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        #location
        self.rect.x = 400
        self.rect.y = 200

    #def update(self):
        #nothing
