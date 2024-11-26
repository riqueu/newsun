"""Interactables class for creating non-player characters/objects in the game."""
import pygame

# TODO: Do this class and put them in the right place
class Interactable:
    def __init__(self, x, y, dialogue_manager):
        self.x = x
        self.y = y
        self.dialogue_manager = dialogue_manager
    
    def draw(self, screen, range=1):
        rect = pygame.Rect(
            self.x - range * 32,  # Assuming each tile is 32x32 pixels
            self.y - range * 32,
            (range * 2 + 1) * 32,
            (range * 2 + 1) * 32
        )
        pygame.draw.rect(screen, (255, 0, 0), rect, 1)
        
    def is_within_range(self, player_x, player_y, range=1):
        return abs(self.x - player_x) <= range and abs(self.y - player_y) <= range

    def handle_event(self, event, player_x, player_y):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            if self.is_within_range(player_x, player_y):
                self.dialogue_manager.start_interaction(self)

class Object(Interactable): # e.g. Mirror
    def __init__(self, x, y, dialogue_manager):
        super().__init__(x, y, dialogue_manager)
    

class NPC(Interactable): # e.g. Tabastan
    def __init__(self, x, y, dialogue_manager):
        super().__init__(x, y, dialogue_manager)
    