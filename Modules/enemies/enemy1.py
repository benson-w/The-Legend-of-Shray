import pygame
import math
#from Modules.enemies.enemies import Enemy
#from Modules.player.player

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (112, 128, 144)
RED = (255, 218, 185)
BLUE = (135, 206, 250)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Enemy1(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        #give size, image attributes, and other traits
        self.percentage = 100
        width = 75
        height = 75
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 200

        #simple movement toggle
        self.toggle_movement = False

    def update(self):

        if self.rect.x < 200:
            self.toggle_movement == False
        if self.rect.x > 500:
            self.toggle_movement == True

        if self.toggle_movement == False:
            self.rect.x = self.rect.x + 1
        if self.toggle_movement == True:
            self.rect.x = self.rect.x - 1
