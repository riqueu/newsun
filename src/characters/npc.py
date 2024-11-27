"""Interactables class for creating non-player characters/objects in the game."""
import pygame
from settings import *

# TODO: Do this class and put them in the right place
class Interactable(pygame.sprite.Sprite):
    pass

class Object(Interactable): # e.g. Mirror (Sprite will be blank as it's already in the map)
    pass

class NPC(Interactable): # e.g. Tabastan
    pass