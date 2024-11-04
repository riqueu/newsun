"""PLACEHOLDER: Room 101 Scene"""

import pygame
import json

from src.ui.interaction import DialogueManager, get_key_to_node

class Room101:
    def __init__(self, screen: pygame.Surface) -> None:
        """Function that initializes the room 101 scene

        Args:
            screen (pygame.Surface): the screen
        """
        self.screen = screen
        self.interactions = json.load(open('scripts/room_101.json'))
        self.background = pygame.image.load("assets/images/backgrounds/temp_bg.jpg")
        self.key_to_node = get_key_to_node(self.interactions)
        self.dialogue_manager = DialogueManager(self.screen, self.interactions, self.key_to_node)
        self.objects = [
            {"name": "Sink", "rect": pygame.Rect(100, 100, 50, 50)},
            {"name": "Mirror", "rect": pygame.Rect(200, 100, 50, 50)}
        ]

    # TODO: Handle Events on room 101
    def handle_event(self, event: pygame.event.Event) -> None:
        pass
    
    def draw(self) -> None:
        """Function that draws the room
        """
        self.screen.blit(self.background, (0, 0))
        for obj in self.objects:
            pygame.draw.rect(self.screen, (255, 0, 0), obj["rect"], 2)

        pygame.display.flip()
