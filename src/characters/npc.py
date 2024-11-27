"""Interactables class for creating non-player characters/objects in the game."""
import pygame
from settings import *

# TODO: Do this class and put them in the right place
class Interactable(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], sprite: pygame.Surface):
        super().__init__()
        self.image = sprite
        self.rect = self.image.get_rect(topleft=pos)

class Object(Interactable): # e.g. Mirror (Sprite will be blank as it's already in the map)
    def __init__(self, pos: tuple[int, int], x: int = 50, y: int = 50): #sprite: pygame.Surface = pygame.Surface((50, 50))):
        sprite = pygame.Surface((x, y))
        super().__init__(pos, sprite)
        sprite.fill((255, 0, 0))  # Fill the surface with red color
        self._layer = BLOCK_LAYER
        self.image_hitbox = pygame.Surface((x, y), pygame.SRCALPHA)
        self.image_hitbox.fill((0, 0, 0, 0))  # Fill with transparent color
        self.mask = pygame.mask.from_surface(self.image_hitbox)

class NPC(Interactable): # e.g. Tabastan
    def __init__(self, pos: tuple[int, int], sprite: pygame.Surface):
        super().__init__(pos, sprite)
        self._layer = PLAYER_LAYER
        self.image_hitbox = pygame.image.load('assets/images/characters/player_hitbox.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image_hitbox)