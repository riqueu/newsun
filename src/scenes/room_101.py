import pygame
from src.ui.interaction import DialogueManager

class Room101:
    def __init__(self, screen, interactions):
        self.screen = screen
        self.background = pygame.image.load("assets/images/backgrounds/temp_bg.jpg")
        self.interactions = interactions
        self.dialogue_manager = DialogueManager(interactions)
        self.objects = [
            {"name": "Sink", "rect": pygame.Rect(100, 100, 50, 50)},
            {"name": "Mirror", "rect": pygame.Rect(200, 100, 50, 50)}
        ]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for obj in self.objects:
                if obj["rect"].collidepoint(event.pos):
                    self.dialogue_manager.start_dialogue(obj["name"])
    
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        for obj in self.objects:
            pygame.draw.rect(self.screen, (255, 0, 0), obj["rect"], 2)
        self.dialogue_manager.draw(self.screen)
        pygame.display.flip()
