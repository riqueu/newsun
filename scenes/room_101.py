import pygame
from ui.interaction import DialogueManager

class Room101:
    def __init__(self, interactions):
        self.background = pygame.image.load("assets/images/backgrounds/temp_bg.jpg")
        self.interactions = interactions
        self.dialogue_manager = DialogueManager(interactions)
        self.objects = [
            {"name": "Sink", "rect": pygame.Rect(100, 100, 50, 50)},
            {"name": "Mirror", "rect": pygame.Rect(200, 100, 50, 50)}
        ]

    # TODO: Make Method Work
    """def check_interaction(self, player_position):
        for obj in self.objects:
            if obj["rect"].collidepoint(player_position):
                interaction = self.interactions.get(obj["name"], None)
                if interaction:
                    self.dialogue_manager.start_interaction(interaction)
                return interaction
        return None"""

    def draw_background(self, screen):
        screen.blit(self.background, (0, 0))

    # TODO: Make Method Work
    """def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            self.check_interaction(mouse_pos)"""
