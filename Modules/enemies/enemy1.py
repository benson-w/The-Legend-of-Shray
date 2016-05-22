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

        # Call the parent's constructor
        # Enemy.__init__(self), jk there's nothing to call, maybe once we figure enemies out
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

        # want to make actions contained so game.py isn't huger than it already is >_<

        #simple movement toggle
        self.toggle_movement = False

    def update(self):

        #simple movement, lmao it's not workign but honestly, FUCK it

        if self.rect.x < 200:
            self.toggle_movement == False
        if self.rect.x > 500:
            self.toggle_movement == True

        if self.toggle_movement == False:
            self.rect.x = self.rect.x + 1
        if self.toggle_movement == True:
            self.rect.x = self.rect.x - 1
