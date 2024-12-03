"""Inventory system for the game."""

import pygame
from settings import *

class Item:
    def __init__(self, name: str, img_path: str) -> None:
        """Initializes the item

        Args:
            name (str): item name
            img_path (str): path to sprite
        """
        self.name = name
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.image.set_colorkey(BLUE)


class Inventory:
    def __init__(self, capacity: int = 4) -> None:
        """Initializes the inventory

        Args:
            capacity (int, optional): max items. Defaults to 4.
        """
        self.capacity = capacity
        self.items = []

    def has_item(self, item: Item) -> bool:
        """Function that checks if item is in inventory

        Args:
            item (Item): item to be checked

        Returns:
            bool: item presence
        """
        return item in self.items
    
    def add_item(self, item: Item) -> bool:
        """Function to add item to inventory

        Args:
            item (Item): item to be added

        Returns:
            bool: Confirmation of addition
        """
        if len(self.items) < self.capacity and not self.has_item(item):
            self.items.append(item)
            return True
        return False

    def remove_item(self, item: Item) -> bool:
        """Function to remove item from inv if it exists

        Args:
            item (Item): item to be removed

        Returns:
            bool: Confirmation of removal
        """
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def clear_inventory(self) -> None:
        """Function to clear inventoru
        """
        self.items = []

    def draw(self, screen: pygame.Surface) -> None:
        """Function to draw items on screen

        Args:
            screen (pygame.Surface): screen to draw on
        """
        x_offset = 40
        y_offset = screen.get_height() - 65
        for item in self.items:
            screen.blit(item.image, (x_offset, y_offset))
            x_offset += item.image.get_width() + 30
