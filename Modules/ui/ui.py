import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (112, 128, 144)
RED = (255, 218, 185)
BLUE = (135, 206, 250)

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