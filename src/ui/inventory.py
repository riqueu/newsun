"""
Inventory system for the game.

This module manages the player's inventory, allowing the addition, removal, and display of items.
It also integrates the inventory's capacity limit and displays collected items on the screen.

Classes:
    - Item: Represents an item with a name and associated sprite.
    - Inventory: Manages the inventory, including adding, removing, and checking items.
"""

import pygame
from settings import *

class Item:
    """
    Represents an item in the game.

    The Item class defines an item with a name and a sprite image. It loads the image from a specified path, 
    scales it to a fixed size, and sets a transparency key for the image.
    """
    def __init__(self, name: str, img_path: str) -> None:
        """
        Initializes the item with a name and sprite image.

        This method loads the image for the item, scales it to a fixed size of 32x32 pixels, 
        and sets a transparency key to handle transparency in the image.

        Args:
            name (str): The name of the item.
            img_path (str): The path to the image file representing the item sprite.
        """
        self.name = name
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.image.set_colorkey(BLUE)


class Inventory:
    """
    Inventory system for managing a collection of items in the game.

    This class handles the inventory of items, including adding, removing, checking for items,
    and clearing the inventory. It also provides a method for drawing the items on the screen.
    """
    def __init__(self, capacity: int = 4) -> None:
        """
        Initializes the inventory.

        Args:
            capacity (int, optional): The maximum number of items the inventory can hold. Defaults to 4.
        """
        self.capacity = capacity
        self.items = []

    def has_item(self, item: Item) -> bool:
        """
        Checks if an item is present in the inventory.

        Args:
            item (Item): The item to check for in the inventory.

        Returns:
            bool: True if the item is present, False otherwise.
        """
        return item in self.items
    
    def add_item(self, item: Item) -> bool:
        """
        Adds an item to the inventory if there is space and the item is not already present.

        Args:
            item (Item): The item to be added to the inventory.

        Returns:
            bool: True if the item was successfully added, False if the inventory is full or the item is already present.
        """
        if len(self.items) < self.capacity and not self.has_item(item):
            self.items.append(item)
            return True
        return False

    def remove_item(self, item: Item) -> bool:
        """
        Removes an item from the inventory if it exists.

        Args:
            item (Item): The item to be removed from the inventory.

        Returns:
            bool: True if the item was successfully removed, False if the item was not found in the inventory.
        """
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def clear_inventory(self) -> None:
        """
        Clears all items from the inventory.

        This method removes all items from the inventory, resetting it to an empty state.
        """
        self.items = []

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the items in the inventory on the screen.

        This method renders the inventory items as images at specified positions on the screen. 
        It arranges them horizontally with some offset between each item.

        Args:
            screen (pygame.Surface): The surface (screen) on which to draw the inventory items.
        """
        x_offset = 40
        y_offset = screen.get_height() - 65
        for item in self.items:
            screen.blit(item.image, (x_offset, y_offset))
            x_offset += item.image.get_width() + 30
