import pygame
from settings import *

class SpriteSheet():
    def __init__(self, file: str) -> None:
        """Initializes the spritesheet

        Args:
            file (str): spritesheet path
        """
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x: int, y: int, widht: int, height: int) -> pygame.Surface:
        """Get sprite from the spritesheet

        Args:
            x (int): y
            y (int): x
            widht (int): w
            height (int): h

        Returns:
            pygame.Surface: sprite surface
        """
        sprite = pygame.Surface([widht, height])
        sprite.blit(self.sheet, (0,0), (x*widht, y*height, widht, height))
        sprite.set_colorkey(BLUE)
        return sprite
