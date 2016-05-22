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
from Modules.weapons.bullet import Bullet
from Modules.player.player import Player
from Modules.level.objects import Platform
from Modules.level.level import Level
from Modules.enemies.enemies import Enemy
from Modules.enemies.enemy1 import Enemy1


#doesn't match to actual colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (112, 128, 144)
RED = (255, 218, 185)
BLUE = (135, 206, 250)

LEVEL_STRING = 'Modules/level/level_data/level_'

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


def main():
    """ Main Program """

    pygame.init()
    done = False

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
    # Get total list of levels
    levelListFile = open('Modules/level/level_list.txt')
    levelList = [x.strip('\n') for x in levelListFile.readlines()]



    # Set the current level
    current_level_no = 0

    levelFile = open(LEVEL_STRING + levelList[current_level_no] + '.txt')

    current_level_data = levelFile.readlines()
    #print(current_level_data)
    for x in range(len(current_level_data)):
        current_level_data[x] = current_level_data[x].strip('\n')
        current_level_data[x] = list(current_level_data[x])

    initialLevel = Level(player)
    initialLevel.level_limit = -1500
    for y in range(len(current_level_data)):
        for x in range(len(current_level_data[y])):
            if current_level_data[y][x] == 'P':
                block = Platform()
                block.rect.x = int(x * (SCREEN_WIDTH/len(current_level_data[y])))
                block.rect.y = int(y * (SCREEN_HEIGHT/len(current_level_data)))
                initialLevel.platform_list.add(block)


    current_level = initialLevel

    #group for almost everything that doesn't need independent handling
    active_sprite_list = pygame.sprite.Group()

    #group for Bullets
    bullet_list = pygame.sprite.Group()

    player.level = current_level

    # sprite list contain enemy objects for specific level
    enemy_list = pygame.sprite.Group()


    # delete all the enemies before adding the new one for the level
    for enemy in enemy_list:
        enemy_list.remove(enemy)

    # populate the right enemy for the level, use enemy_list to handle
    if player.level == initialLevel:
        enemy = Enemy1()
        enemy_list.add(enemy)
    # elif level == level 2, etc

    # Set playe starting point
    # TODO: Change this to be set by level data
    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height - 200


    active_sprite_list.add(player)
    active_sprite_list.add(crosshair)

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    #initialize text display
    font = pygame.font.Font('freesansbold.ttf', 24)

    # -------- Main Program Loop -----------
    while not done:

        # Use mouse to look beyond the scope of the screen
        # The below conditional doesn't work as anticipated

        if (pygame.mouse.get_pos()[0] - 50) < 1:

            if (player.rect.right < (SCREEN_WIDTH - 50)):
            # Mouse is left side of screen, we want to shift screen with player in view

                diff = pygame.mouse.get_pos()[0]
                player.rect.right = player.rect.right + diff
                current_level.shift_world(diff, enemy)

            if (player.rect.left > 50 and player.rect.left ):
            # Mouse is right side of screen, we want to shift screen with player in view

                diff = pygame.mouse.get_pos()[0] - SCREEN_WIDTH - 50
                player.rect.left = player.rect.left - diff
                current_level.shift_world(-diff, enemy)


        #Update crosshair position (Crosshair.update is broken; not sure what arguments to pass)
        crosshair.rect.x = pygame.mouse.get_pos()[0]
        crosshair.rect.y = pygame.mouse.get_pos()[1]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #exit the game
                    done = True
                if event.key == pygame.K_TAB:
                    player.rect.x = 340 + player.level.world_shift #need argument with diff (frame shift) for reset
                    player.rect.y = SCREEN_HEIGHT - player.rect.height - 200
                    player.change_x = 0
                    player.change_y = 0

            #shoot bullet
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player.toggle_gun == True:
                    bullet = Bullet(pygame.mouse.get_pos(), [player.rect.x, player.rect.y], player.toggle_gun)
                    player.bullet_count = player.bullet_count - 1
                    #active_sprite_list.add(bullet)
                    bullet_list.add(bullet)

            if (event.type == pygame.KEYDOWN):
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.go_left()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.go_right()
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.jump()
                if event.key == pygame.K_r and player.toggle_gun == True:
                    player.bullet_count = 50
                if event.key == pygame.K_1:     #weapon 1
                    player.toggle_gun = True
                if event.key == pygame.K_2:     #weapon 2
                    player.toggle_gun = False
                if event.key == pygame.K_3:     #weapon 3
                    player.toggle_gun = False
                if event.key == pygame.K_4:     #weapon 4
                    player.toggle_gun = False

            player.rect.y += 2
            platform_hit_list = pygame.sprite.spritecollide(player, player.level.platform_list, False)
            player.rect.y -= 2

            ''' doens't work fuck me, i already tried praying to heavenly divine based zuofu so basically gg fml
            if (len(platform_hit_list) > 0):
                player.on_ground = True
            elif (len(platform_hit_list) == 0 and player.change_y != 0) :
                player.on_ground = False
            '''

            #stop moving if you stop holding
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and player.change_x < 0:
                    player.stop()
                if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and player.change_x > 0:
                    player.stop()


        # Update everthing in sprite_list defined by super().__init__
        active_sprite_list.update()
        bullet_list.update()
        enemy_list.update()

        screen.fill(BLUE) #fill background maybe with a picture later

        # Update health, time, bullet text, enemy health
        display_percent = font.render("Health: " + str(player.get_percentage()), True, (0, 0, 0))
        display_time = font.render("Time: " + str(int(pygame.time.get_ticks()/1000)), True, (0, 0, 0))
        if player.toggle_gun == True:
            display_weapon_text = font.render("Magazine: " + str(player.get_bullet_count()), True, (0, 0, 0))
        else:
            display_weapon_text = font.render("Melee Mode", True, (0, 0, 0))

        display_enemy_percent = font.render("Enemy hp: " + str(enemy.percentage), True, (0, 0, 0))

        #display text
        screen.blit(display_percent, (10, 10))
        screen.blit(display_time, (10, 50))
        screen.blit(display_weapon_text, (10, 90))
        screen.blit(display_enemy_percent, (10, 130))

        # bullet collision with enemies
        for bullet in bullet_list:
            for enemy in enemy_list:
                if bullet.rect.colliderect(enemy.rect):
                    bullet_list.remove(bullet)
                    #print(enemy_list)
                    if enemy.percentage <= 0:
                        enemy_list.remove(enemy)
                        enemy.percentage = 0
                    if (enemy.percentage > 0):
                        enemy.percentage = enemy.percentage - 10


        # bullet collision with walls
        for bullet in bullet_list:
            for platform in player.level.platform_list:
                if bullet.rect.colliderect(platform.rect):
                    bullet_list.remove(bullet)

        # Update items in the level
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff, enemy)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff, enemy)

        # Code for end of level, line 425: http://programarcadegames.com/python_examples/show_file.php?file=platform_moving.py

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT

        current_level.draw(screen)
        bullet_list.draw(screen)
        enemy_list.draw(screen)
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
