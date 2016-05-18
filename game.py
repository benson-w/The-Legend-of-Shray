"""

THE LEGEND OF SHRAY

|======================|
|                      |
|         "ok"         |
|                      |
|======================|

built upon: http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py"""

import pygame
import math
import Modules.player
from Modules.weapons.bullet import Bullet as Bullet
from Modules.player.player import Player

# Global constants
'''
#doesn't match to actual colors
Red is color of character
Blue is color of background
Green is color of blocks
'''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (112, 128, 144)
RED = (255, 218, 185)
BLUE = (135, 206, 250)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Crosshair(pygame.sprite.Sprite):

    #Crosshair constructor
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(BLACK)
        self.image.set_alpha(100) #0 is fully transparent, #255 opaque

        # Set a reference as image rect
        self.rect = self.image.get_rect()

    '''def update(self, mouse):
        # Move the crosshair
        self.rect.x = pygame.mouse.get_pos()[0]
        self.rect.y = pygame.mouse.get_pos()[1]
    '''


class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()


class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
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
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        #screen.fill(BLUE)

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll everything:"""

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x


# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -1500

        # Array with width, height, x, and y of platform
        level = [[600, 40, 100, 500],
                 [600, 40, 700, 480]]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


def main():
    """ Main Program """

    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size, 0, 32)

    pygame.display.set_caption("The Legend of Shray")

    # Create the player
    player = Player()

    # Create the crosshair
    crosshair = Crosshair()

    # Remove mouse icon
    pygame.mouse.set_visible(False)

    # Create all the levels
    level_list = []
    level_list.append( Level_01(player) )

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height - 200
    active_sprite_list.add(player)
    active_sprite_list.add(crosshair)

    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    #initialize text display
    font = pygame.font.Font('freesansbold.ttf', 24)

    # -------- Main Program Loop -----------
    while not done:

        #Update crosshair position (Crosshair.update is broken; not sure what arguments to pass)
        crosshair.rect.x = pygame.mouse.get_pos()[0]
        crosshair.rect.y = pygame.mouse.get_pos()[1]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #exit the game
                    done = True
                if event.key == pygame.K_1:
                    player.rect.x = 340 + player.level.world_shift #need argument with diff (frame shift) for reset
                    player.rect.y = SCREEN_HEIGHT - player.rect.height - 200
                    player.change_x = 0
                    player.change_y = 0

            #shoot bulllet
            if event.type == pygame.MOUSEBUTTONDOWN:
                bullet = Bullet(pygame.mouse.get_pos(), [player.rect.x, player.rect.y])
                player.bullet_count = player.bullet_count + 1
                active_sprite_list.add(bullet)

            #only allow key presses if on the ground
            player.rect.y += 2
            platform_hit_list = pygame.sprite.spritecollide(player, player.level.platform_list, False)
            player.rect.y -= 2
            if (event.type == pygame.KEYDOWN):
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.go_left()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.go_right()
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.jump()

            #stop moving if you stop holding
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and player.change_x < 0:
                    player.stop()
                if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and player.change_x > 0:
                    player.stop()

        # Update the player.
        active_sprite_list.update()


        screen.fill(BLUE)


        # Update health, time, bullet text
        display_percent = font.render("Health: " + str(player.get_percentage()), True, (0, 0, 0))
        display_time = font.render("Time: " + str(pygame.time.get_ticks()), True, (0, 0, 0))
        display_bullet_count = font.render("Bullets used: " + str(player.get_bullet_count()), True, (0, 0, 0))

        #display text
        screen.blit(display_percent, (10, 10))
        screen.blit(display_time, (10, 50))
        screen.blit(display_bullet_count, (10, 90))

        # Update items in the level
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)


        ''' Code for end of level
         http://programarcadegames.com/python_examples/show_file.php?file=platform_moving.py
         around line 425
         '''

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT

        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        # Limit to 60 frames per second
        clock.tick(60)

        # ! Change screen by shifting everything in screen

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

if __name__ == "__main__":
    main()
