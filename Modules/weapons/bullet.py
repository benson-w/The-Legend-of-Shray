import pygame
import math
import Modules.player
from Modules.level.objects import Platform
from Modules.level.level import Level

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (112, 128, 144)
RED = (255, 218, 185)
BLUE = (135, 206, 250)

class Bullet(pygame.sprite.Sprite):

    def __init__(self, mouse, player, toggle):
        if toggle == True:
            super().__init__()

            # bullet appearances and location attributes
            self.image = pygame.Surface([10, 10])
            self.image.fill(BLACK)
            self.mouse_x, self.mouse_y = mouse[0], mouse[1]
            self.player = player

            self.rect = self.image.get_rect()

            self.rect.x = player[0]
            self.rect.y = player[1]

    def update(self):

        #self explanatory, shoot at vector created from player to crosshair (mouse)
        speed = 30
        #range = 200
        distance = [self.mouse_x - self.player[0], self.mouse_y - self.player[1]]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = [distance[0] / norm, distance[1 ] / norm]
        bullet_vector = [direction[0] * speed, direction[1] * speed]


        self.rect.x += bullet_vector[0]
        self.rect.y += bullet_vector[1]
