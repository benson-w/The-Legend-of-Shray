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

class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        #give size, image attributes
        width = 100
        height = 100
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)

        # add a health
        self.percentage = 0

        # List of sprites we can bump against
        self.level = None

    def update(self):
        """ Enemy movement """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x
        self.change_x = self.change_x + self.accel_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
                self.accel_x = 0
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
                self.accel_x = 0

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

    def get_bullet_count(self):
        return self.bullet_count

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 1.0  #grav

        # update position when hit the ground
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.rect.x = 340 + self.level.world_shift
            self.rect.y = SCREEN_HEIGHT - self.rect.height - 200
            self.change_x = 0
            self.change_y = 0
            self.accel_x = 0

        #    self.change_y = 0
        #    self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        self.accel_x = 0

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -15

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.image = pygame.image.load("media/shray_left.png").convert_alpha()

        if self.change_x <= -4:
            self.change_x = -4
            self.accel_x = 0
        else:
            self.accel_x = self.accel_x - .5

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.image = pygame.image.load("media/shray_right.png").convert_alpha()
        if self.change_x >= 4:
            self.accel_x = 0
        else:
            self.accel_x = self.accel_x + .5

    def stop(self):
        """ Called when the user lets off the keyboard. """
        #self.image = pygame.image.load("media/shray_standing1.png").convert()

        self.change_x = 0
        self.accel_x = 0

    #health
    def get_percentage(self):
        #update percentage when hit by something
        return self.percentage
