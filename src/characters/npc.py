"""
Module for creating and handling interactive non-player characters (NPCs) and objects in the game.

Classes:
    - Interactable: Base class for objects and NPCs that can be interacted with by the player.
    - Object: Represents static, inanimate objects (e.g., mirrors) that are interactable.
    - NPC: Represents non-player characters (e.g., Tabastan) that can be interacted with for actions like dialogues or quests.

Functions:
    - None directly; the functionality is encapsulated within the classes.
"""
import pygame
from settings import *

class Interactable(pygame.sprite.Sprite):
    """
    Represents an interactable object or NPC in the game.
    
    Attributes:
        image (pygame.Surface): The sprite image for the object.
        name (str): The name of the interactable object.
        rect (pygame.Rect): The rectangle area representing the objects position and dimensions.
    
    Methods:
        player_in_interaction_range(player_rect: pygame.Rect, interaction_range: int = 10) -> bool:
            Checks if the player is within a specified interaction range of the object.
    """
    def __init__(self, pos: tuple[int, int], sprite: pygame.Surface, name: str):
        """
        Initializes an interactable object or NPC.

        Args:
            pos (tuple[int, int]): The position of the object (x, y).
            sprite (pygame.Surface): The sprite image representing the object.
            name (str): The name of the object or NPC.
        """
        super().__init__()
        self.image = sprite
        self.name = name
        self.rect = self.image.get_rect(topleft=pos)
        
    def player_in_interaction_range(self, player_rect: pygame.Rect, interaction_range: int = 10) -> bool:
        """
        Checks if the player is within the interaction range of the object.

        Args:
            player_rect (pygame.Rect): The rectangle representing the player's position and size.
            interaction_range (int, optional): The interaction range around the object. Default is 10.

        Returns:
            bool: True if the player is within interaction range, False otherwise.
        """
        return self.rect.colliderect(player_rect.inflate(interaction_range, interaction_range))

class Object(Interactable):
    """
    Represents an interactive object in the game, such as a mirror or other non-player object.
    The sprite will be transparent as it is already part of the map, and the object can be interacted with.
    """
    def __init__(self, pos: tuple[int, int], name: str, rec: tuple[int, int] = (50, 50)):
        """
        Initializes an interactive object (e.g., a mirror) in the game.

        Args:
            pos (tuple[int, int]): Position (x, y) of the object in the game world.
            name (str): The name of the object.
            rec (tuple[int, int], optional): Size of the object (width, height). Default is (50, 50).

        """
        sprite = pygame.Surface(rec, pygame.SRCALPHA)
        # sprite.fill((255, 0, 0, 255))  # Fill the surface with red
        sprite.fill((0, 0, 0, 0))  # Fill the surface with transparent color
        super().__init__(pos, sprite, name)
        self._layer = BLOCK_LAYER
        self.image_hitbox = pygame.Surface(rec, pygame.SRCALPHA)
        self.image_hitbox.fill((0, 0, 0, 0))  # Fill with transparent color
        self.mask = pygame.mask.from_surface(self.image_hitbox)

class NPC(Interactable): # e.g. Tabastan
    """
    Represents a non-player character (NPC) in the game, such as a character that the player can interact with.
    NPCs can have different layers depending on their role, such as being part of the player's group or an obstacle.
    """
    def __init__(self, pos: tuple[int, int], name: str, sprite: pygame.Surface, matilda: bool = False):
        """
        Initializes a Non-Player Character (NPC) for the game.

        Args:
            pos (tuple[int, int]): Position (x, y) of the NPC.
            name (str): Name of the NPC.
            sprite (pygame.Surface): Sprite image of the NPC.
            matilda (bool): If True, assigns NPC to player layer. Defaults to False.
        """
        super().__init__(pos, sprite, name)
        if matilda:
            self._layer = PLAYER_LAYER  # If matilda is True, the NPC is assigned to the player's layer
        else:
            self._layer = BLOCK_LAYER  # Otherwise, assigns the NPC to the obstacle layer
        self.image_hitbox = pygame.image.load('assets/images/characters/player_hitbox.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image_hitbox)