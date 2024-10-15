import pygame
import json


def load_interactions(filename):
    with open(filename, 'r') as f:
        return json.load(f)
    

class DialogueBox:
    def __init__(self):
        self.current_text = ""
        self.font = pygame.font.Font(None, 36)

    def set_text(self, text):
        self.current_text = text

    def render(self, screen):
        text_surface = self.font.render(self.current_text, True, (255, 255, 255))
        screen.blit(text_surface, (50, 500))  # Position the text
