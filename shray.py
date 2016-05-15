"""

THE LEGEND OF SHRAY

|======================|
|                      |
|        "ok"          |
|                      |
|======================|

built upon: http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py"""

import pygame

# Global constants

# Colors
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

        # Call the parent's constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
        self.accel_x = 0

        # Set initial health/percentage
        self.percentage = 0

        # List of sprites we can bump against
        self.level = None

    def update(self):
        """ Move the player. """
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
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

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

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 1.0  #grav

        # update position when hit the ground
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.rect.x = 340
            self.rect.y = SCREEN_HEIGHT - self.rect.height - 200

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

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """

        if self.change_x < -4:
            self.accel_x = 0
            self.change_x = -4
        else:
            self.accel_x = -1

    def go_right(self):
        """ Called when the user hits the right arrow. """
        if self.change_x > 4:
            self.accel_x = 0
            self.change_x = 4
        else:
            self.accel_x = 1

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
        self.accel_x = 0

    #health
    def get_percentage(self):
        #update percentage when hit by something
        self.percentage = 0


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
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("The Legend of Shray")

    # Create the player
    player = Player()

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

    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    #initialize text display
    font = pygame.font.Font('freesansbold.ttf',30)

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #exit the game
                    done = True
                if event.key == pygame.K_1:
                    player.rect.x = 340 #need argument with diff (frame shift) for reset
                    player.rect.y = SCREEN_HEIGHT - player.rect.height - 200

            #only allow key presses if on the ground
            player.rect.y += 2
            platform_hit_list = pygame.sprite.spritecollide(player, player.level.platform_list, False)
            player.rect.y -= 2
            if (len(platform_hit_list) > 0) and (event.type == pygame.KEYDOWN):
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            #stop moving if you stop holding
            if event.type == pygame.KEYUP and len(platform_hit_list) > 0:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

            # stop moving if you're coliding with something (ground)
            # and you're not pressing anything
            if (len(platform_hit_list) > 0) and (event.type == pygame.KEYUP):
                player.stop()

        # Update the player.
        active_sprite_list.update()

        # Update percentage
        display_percent = font.render("Percentage: " + str(player.get_percentage()), True, (0, 0, 0))
        screen.fill(BLUE)
        screen.blit(display_percent, (10, 10))

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
