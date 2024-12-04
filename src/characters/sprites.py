"""
This module defines the `SpriteSheet` class, which facilitates the extraction of individual sprites 
from a larger spritesheet image. The class is useful for games or applications that require the 
use of sprite-based animations and character designs.

Classes:
    - SpriteSheet: A class that loads a spritesheet and extracts individual sprites from it.
    
Functions:
    - None directly. All functionality is encapsulated within the `SpriteSheet` class.
"""
import pygame
from settings import *

class SpriteSheet():
    """
    A class used to represent a spritesheet, which is a large image containing smaller individual sprites.

    This class provides methods for extracting individual sprites from a spritesheet for use in games 
    or graphical applications that require sprite-based animation or static character images.

    Methods:
        __init__(file: str) -> None:
            Initializes the spritesheet from an image file.
        
        get_sprite(x: int, y: int, width: int, height: int) -> pygame.Surface:
            Extracts and returns a sprite from the sheet at given (x, y) position and specified width and height.
    """
    def __init__(self, file: str) -> None:
        """
        Initializes the spritesheet by loading an image file.

        Args:
            file (str): The path to the spritesheet image file.
        """
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x: int, y: int, widht: int, height: int) -> pygame.Surface:
        """
        Extracts a single sprite from the spritesheet.

        Args:
            x (int): Horizontal position (column) of the sprite in the sheet.
            y (int): Vertical position (row) of the sprite in the sheet.
            widht (int): Width of the sprite.
            height (int): Height of the sprite.

        Returns:
            pygame.Surface: The extracted sprite as a surface.
        """
        sprite = pygame.Surface([widht, height])
        sprite.blit(self.sheet, (0,0), (x*widht, y*height, widht, height))
        sprite.set_colorkey(BLUE)
        return sprite
