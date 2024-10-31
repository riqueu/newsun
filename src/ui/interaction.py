"""Module for handling dialogue interactions with the player."""

import pygame
import json

from settings import WIDTH, HEIGHT

def load_interactions(filename):
    with open(filename, 'r') as f:
        return json.load(f)
    

class DialogueBox:
    def __init__(self):
        self.current_text = ""
        self.font = pygame.font.Font(None, 36)
        self.box_width = 300
        self.box_height = 200
        self.box_x = (WIDTH - self.box_width) // 2
        self.box_y = (HEIGHT - self.box_height) // 2
        

    def set_text(self, text):
        self.current_text = text

    def render(self, screen):
        text_surface = self.font.render(str(self.current_text), True, (255, 255, 255))
        screen.blit(text_surface, (50, 500))  # Position the text

    
class DialogueManager:
    def __init__(self, dialogue_data):
        self.dialogue_data = dialogue_data
        self.current_line = 0
        self.dialogue_box = DialogueBox()
        self.dialogue_active = False
    
    def start_dialogue(self, object_name):
        self.current_line = 0
        self.dialogue_active = True
        self.dialogue_box.set_text(self.dialogue_data[object_name][self.current_line])
    
    def next_line(self):
        self.current_line += 1
        if self.current_line < len(self.dialogue_data):
            self.dialogue_box.set_text(self.dialogue_data[self.current_line])
        else:
            self.dialogue_active = False
    
    def draw(self, screen):
        if self.dialogue_active:
            self.dialogue_box.render(screen)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.next_line()
