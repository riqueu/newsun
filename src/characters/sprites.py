import pygame
from settings import *

class SpriteSheet():
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, widht, height):
        sprite = pygame.Surface([widht, height])
        sprite.blit(self.sheet, (0,0), (x*widht, y*height, widht, height))
        sprite.set_colorkey(BLUE)
        return sprite
    
character_spritesheet = SpriteSheet('assets/images/characters/characters.png')