"""PLACEHOLDER: Floor 1 scene for the game."""

import pygame
import json

class Floor1:
    def __init__(self):
        # Load any assets for this scene (e.g., images, music)
        self.background = pygame.image.load("assets/images/floor_1_background.png")
        with open("scripts/floor_1.json") as f:
            self.dialogue_data = json.load(f)
        self.current_line = 0

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Press space to advance dialogue
                self.current_line += 1
                if self.current_line >= len(self.dialogue_data['dialogue']):
                    self.current_line = 0  # Loop dialogue

    def update(self):
        pass  # Add any game logic here

    def render(self, screen):
        # Draw the background and the current dialogue line
        screen.blit(self.background, (0, 0))
        font = pygame.font.Font(None, 36)
        dialogue_text = self.dialogue_data['dialogue'][self.current_line]
        text_surface = font.render(dialogue_text, True, (255, 255, 255))
        screen.blit(text_surface, (50, 500))  # Position of dialogue
