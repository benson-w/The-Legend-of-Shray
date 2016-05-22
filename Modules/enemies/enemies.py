import pygame
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (112, 128, 144)
RED = (255, 218, 185)
BLUE = (135, 206, 250)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Enemy(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()
        self.percentage = 100


    #health
    def get_percentage(self):
        #update percentage when hit by something
        return self.percentage
