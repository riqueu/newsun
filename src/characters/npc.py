"""Interactables class for creating non-player characters/objects in the game."""
import pygame

# TODO: Do this class and put them in the right place
class Interactable:
    def __init__(self, x, y, dialogue_manager):
        self.x = x
        self.y = y
        self.dialogue_manager = dialogue_manager
    
    def draw(self):
        pass
    
    def is_within_range(self, player_x, player_y, range=1):
        return abs(self.x - player_x) <= range and abs(self.y - player_y) <= range

    def handle_event(self, event, player_x, player_y):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            if self.is_within_range(player_x, player_y):
                self.dialogue_manager.start_interaction(self)

class Object(Interactable): # e.g. Mirror
    def __init__(self, x, y, dialogue_manager):
        super().__init__(x, y, dialogue_manager)
    
    def draw(self):
        # Add code to draw the object
        pass
    
    def handle_event(self, event, player_x, player_y):
        super().handle_event(event, player_x, player_y)
        # Add additional event handling for the object
        pass

class NPC(Interactable): # e.g. Tabastan
    def __init__(self, x, y, dialogue_manager):
        super().__init__(x, y, dialogue_manager)
    
    def draw(self):
        # Add code to draw the NPC
        pass
    
    def handle_event(self, event, player_x, player_y):
        super().handle_event(event, player_x, player_y)
        # Add additional event handling for the NPC
        pass