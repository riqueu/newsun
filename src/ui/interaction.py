"""Module for handling dialogue interactions with the player."""

import pygame
import json
from pygamevideo import Video

from settings import WIDTH, HEIGHT

def load_interactions(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def get_key_to_node(interactions):
    return {interaction['title']: interaction['key'] for interaction in interactions if 'key' in interaction}

class DialogueBox:
    def __init__(self):
        self.box_width = 400
        self.box_height = 600
        self.box_x = (7 * (WIDTH - self.box_width)) // 8
        self.box_y = (HEIGHT - self.box_height) // 2
        self.font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 18)
        self.text = ""
        self.lines = []
        self.video_in = Video('assets/ui/DialogueBoxIn.mp4')
        self.video = Video('assets/ui/DialogueBox.mp4')
        self.video_out = Video('assets/ui/DialogueBoxOut.mp4')

    def set_text(self, text):
        self.text = text
        self.lines = self.wrap_text(text)

    def wrap_text(self, text):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            if '\n' in word:
                parts = word.split('\n')
                for part in parts[:-1]:
                    test_line = current_line + part + " "
                    lines.append(test_line.strip())
                    current_line = ""
                current_line = parts[-1] + " "
            else:
                test_line = current_line + word + " "
                if self.font.size(test_line)[0] <= self.box_width - 30:  # Adjusted to fit within the box
                    current_line = test_line
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "

        if current_line.strip():
            lines.append(current_line.strip())
        return lines

    def render_bg(self, screen):
        #TODO: In and Out Animations
        self.video.play(loop=True)
        self.video.draw_to(screen, (self.box_x, self.box_y))

    
    def render_text(self, screen):
        for i, line in enumerate(self.lines):
            text_surface = self.font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (self.box_x + 20, self.box_y + i * 40 + 20))


class DialogueManager:
    def __init__(self, screen, dialogue_data, key_to_node):
        self.screen = screen
        self.key_to_node = key_to_node
        self.dialogue_data = dialogue_data
        self.current_node = self.find_node("Start")
        self.dialogue_box = DialogueBox()
        self.dialogue_started = False
        self.dialogue_active = False
        self.dialogue_ended = False
    
    def find_node(self, title):
        for node in self.dialogue_data:
            if node['title'] == title:
                return node
        return None

    def handle_event(self, event):    
        if self.current_node['title'] == "End":
            self.dialogue_ended = True
        
        elif event.type == pygame.KEYDOWN:
            pressed_key = event.unicode
            self.next_node_title = self.current_node['key'].get(pressed_key)
            if self.next_node_title:
                self.current_node = self.find_node(self.next_node_title)
    
    def draw(self):
        if self.current_node['title'] != "End":
            self.screen.fill((0, 0, 0))
            self.dialogue_box.set_text(self.current_node['body'])
            
            self.dialogue_box.render_bg(self.screen)
            self.dialogue_box.render_text(self.screen)
            pygame.display.flip()
                

            
