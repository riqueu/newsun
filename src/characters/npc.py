"""Interactables class for creating non-player characters/objects in the game."""
import pygame
from settings import *

# TODO: Do this class and put them in the right place
class Interactable(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], sprite: pygame.Surface, name: str):
        super().__init__()
        self.image = sprite
        self.name = name
        self.rect = self.image.get_rect(topleft=pos)
        
    def player_in_interaction_range(self, player_rect: pygame.Rect, interaction_range: int = 10) -> bool:
        return self.rect.colliderect(player_rect.inflate(interaction_range, interaction_range))

class Object(Interactable): # e.g. Mirror (Sprite will be blank as it's already in the map)
    def __init__(self, pos: tuple[int, int], name: str, rec: tuple[int, int] = (50, 50)):
        # pos = (int(pos[0]), int(pos[1]))  # Ensure pos is a tuple of integers
        sprite = pygame.Surface(rec, pygame.SRCALPHA)
        sprite.fill((0, 0, 0, 0))  # Fill the surface with transparent color
        super().__init__(pos, sprite, name)
        self._layer = BLOCK_LAYER
        self.image_hitbox = pygame.Surface(rec, pygame.SRCALPHA)
        self.image_hitbox.fill((0, 0, 0, 0))  # Fill with transparent color
        self.mask = pygame.mask.from_surface(self.image_hitbox)

class NPC(Interactable): # e.g. Tabastan
    def __init__(self, pos: tuple[int, int], name: str, sprite: pygame.Surface, matilda: bool = False):
        super().__init__(pos, sprite, name)
        if matilda:
            self._layer = PLAYER_LAYER
        else:
            self._layer = BLOCK_LAYER
        self.image_hitbox = pygame.image.load('assets/images/characters/player_hitbox.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image_hitbox)