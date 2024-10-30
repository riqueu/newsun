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

    
class DialogueManager:
    def __init__(self, dialogue_data):
        self.dialogue_data = dialogue_data
        self.current_line = 0

    # TODO: Make Method Work
    def start_interaction(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Space to advance dialogue
                self.current_line += 1
                if self.current_line >= len(self.dialogue_data['dialogue']):
                    self.current_line = 0  # Loop back to start (for simplicity)
    
    # TODO: Make Method Work
    def draw(self, screen):
        dialogue_box = DialogueBox()
        current_stage = self.dialogue_data
        for _ in range(self.current_line):
            if 'next_stage' in current_stage:
                current_stage = current_stage['next_stage']
            else:
                break
        if 'dialogue' in current_stage:
            dialogue_box.set_text(current_stage['dialogue'])
        dialogue_box.render(screen)