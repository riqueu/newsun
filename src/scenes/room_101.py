"""PLACEHOLDER: Room 101 Scene"""

import pygame

from src.ui.interaction import load_scene_interactions #, DialogueManager, get_key_to_node


class Room101:
    def __init__(self, screen: pygame.Surface) -> None:
        """Function that initializes the room 101 scene

        Args:
            screen (pygame.Surface): the screen
        """
        self.screen = screen
        self.background = pygame.image.load("assets/images/backgrounds/temp_bg.jpg")

        scripts_path = 'scripts/room_101'
        self.dialogue_managers = load_scene_interactions(scripts_path, self.screen)
        # print(self.dialogue_managers['clock'].dialogue_data[0]['body'])

        self.objects = [
            {"name": "Sink", "rect": pygame.Rect(100, 100, 50, 50)},
            {"name": "Mirror", "rect": pygame.Rect(200, 100, 50, 50)},
            {"name": "Clock", "rect": pygame.Rect(900, 400, 50, 50)},
            {"name": "Door", "rect": pygame.Rect(900, 500, 50, 50)}
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

