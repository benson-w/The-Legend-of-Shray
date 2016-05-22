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

class Player(pygame.sprite.Sprite):

    def __init__(self):
        """ Constructor function """

        super().__init__()

        # player attributes
        width = 40
        height = 60
        self.toggle_gun = False
        self.bullet_count = 50
        self.on_ground = True
        self.image = pygame.image.load("media/shray_right.png")
        width = self.image.get_rect().size[0]
        height = self.image.get_rect().size[1]
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0
        self.accel_x = 0
        self.percentage = 100

        # List of sprites we can bump against
        self.level = None

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x
        self.change_x = self.change_x + self.accel_x

        # See if we hit anything, set right/left side to left/right side of item we hit
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
                self.accel_x = 0
            elif self.change_x < 0:
                self.rect.left = block.rect.right
                self.accel_x = 0

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0

    def get_bullet_count(self):
        return self.bullet_count

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 1.0

        # update position when hit the ground
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.rect.x = 340 + self.level.world_shift
            self.rect.y = SCREEN_HEIGHT - self.rect.height - 200
            self.change_x = 0
            self.change_y = 0
            self.accel_x = 0

    def jump(self):
        # move down a bit and see if there is a platform below us. (1 doesn't work)
        # if yes, we can jump
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
        self.accel_x = 0
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -15

    # Player-controlled movement:

    def go_left(self):
        self.image = pygame.image.load("media/shray_left.png").convert_alpha()
        if self.change_x <= -4:
            self.change_x = -4
            self.accel_x = 0
        else:
            self.accel_x = self.accel_x - .5

    def go_right(self):
        self.image = pygame.image.load("media/shray_right.png").convert_alpha()
        if self.change_x >= 4:
            self.accel_x = 0
        else:
            self.accel_x = self.accel_x + .5

    def stop(self):
        #self.image = pygame.image.load("media/shray_standing1.png").convert()
        self.change_x = 0
        self.accel_x = 0

    def get_percentage(self):
        return self.percentage
