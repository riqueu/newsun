"""Module for handling dialogue interactions with the player."""

import pygame
import os
import json

from src.ui.animated_sequence import load_png_sequence, sequence_current_frame
from settings import WIDTH, HEIGHT


def get_key_to_node(interactions: dict) -> dict:
    """Function that gets interactions and returns the key_to_node dict to handle dialogue options

    Args:
        interactions (dict): dict with interactions

    Returns:
        dict: dict with the keys that point to the next node when pressed
    """
    return {interaction['title']: interaction['key'] for interaction in interactions if 'key' in interaction}


def load_scene_interactions(scripts_path: str, screen: pygame.Surface) -> dict:
    """Function that gets all the interactions in a scene

    Args:
        scripts_path (str): path to folder where the scene's interactions are stored
        screen (pygame.Surface): the screen

    Returns:
        dict: dict with all dialogue managers for the scene
    """
    interactions = {}
    key_to_node = {}
    dialogue_managers = {}
    for filename in os.listdir(scripts_path):
        if filename.endswith('.json'):
            file_path = os.path.join(scripts_path, filename)
            with open(file_path, 'r') as file:
                interaction = json.load(file)
                key = filename.split('.')[0]
                interactions[key] = interaction
                key_to_node[key] = get_key_to_node(interaction)
                dialogue_managers[key] = DialogueManager(screen, interaction, key_to_node[key])
    return dialogue_managers


class DialogueBox:
    def __init__(self, screen: pygame.Surface) -> None:
        """Function that initializes the Dialogue Box object

        Args:
            screen (pygame.Surface): the screen
        """
        self.screen = screen
        self.box_width = 400
        self.box_height = 600
        self.box_x = (7 * (WIDTH - self.box_width)) // 8
        self.box_y = (HEIGHT - self.box_height) // 2
        self.font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 18)
        self.text = ""
        self.lines = []
        self.video_in = load_png_sequence('assets/ui/DialogueBoxIn')
        self.video = load_png_sequence('assets/ui/DialogueBox')
        self.video_out = load_png_sequence('assets/ui/DialogueBoxOut')

    def set_text(self, text: str) -> None:
        """Function that sets the text to be displayed

        Args:
            text (str): the text
        """
        self.text = text
        self.lines = self.wrap_text(text)

    def wrap_text(self, text: str) -> list:
        """Function that wraps the text inside the box

        Args:
            text (str): the text

        Returns:
            list: list of strings fitting the box
        """
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

    def render_bg(self) -> None:
        """Function that renders the background of the box
        """
        self.screen.blit(sequence_current_frame(self.video), (self.box_x,self.box_y))

    def render_text(self) -> None:
        """Function that renders the text with animation
        """
        
        if not hasattr(self, 'animation_played'):
            self.animation_played = False

        # FIXME: Animation has a weird effect to it. See if fixable. 
        if not self.animation_played:
            max_chars = len(self.text)
            char_index = 0
            for i, line in enumerate(self.lines):
                for j in range(len(line)):
                    if char_index < max_chars:
                        text_surface = self.font.render(line[:j+1], True, (255, 255, 255))
                        self.screen.blit(text_surface, (self.box_x + 20, self.box_y + i * 40 + 20))
                        char_index += 1
                        pygame.display.flip()
                        pygame.time.delay(5)  # Adjust delay for speed of animation
            self.animation_played = True
        else:
            for i, line in enumerate(self.lines):
                text_surface = self.font.render(line, True, (255, 255, 255))
                self.screen.blit(text_surface, (self.box_x + 20, self.box_y + i * 40 + 20))


class DialogueManager:
    def __init__(self, screen: pygame.Surface, dialogue_data: list, key_to_node: dict) -> None:
        """Function that initializes the dialogue manager

        Args:
            screen (pygame.Surface): the screen
            dialogue_data (list): dialogue data
            key_to_node (dict): keys that point to the next node when pressed
        """
        self.screen = screen
        self.key_to_node = key_to_node
        self.dialogue_data = dialogue_data
        self.current_node = self.find_node("Start")
        self.dialogue_box = DialogueBox(screen)
        self.dialogue_started = False
        self.dialogue_active = False
        self.dialogue_ended = False
    
    def find_node(self, title: str) -> dict|None:
        """Function that finds the next node

        Args:
            title (str): node to find

        Returns:
            dict|None: node or None if not found
        """
        for node in self.dialogue_data:
            if node['title'] == title:
                return node
        return None

    def handle_event(self, event: pygame.event.Event) -> None:
        """Function that handles dialogue/interaction events

        Args:
            event (pygame.event.Event): current event
        """
        if self.current_node['title'] == "End":
            self.dialogue_ended = True
        
        elif event.type == pygame.KEYDOWN:
            # TODO: Implement Skill Checks
            pressed_key = event.unicode
            self.next_node_title = self.current_node['key'].get(pressed_key)
            if self.next_node_title:
                self.current_node = self.find_node(self.next_node_title)
                self.dialogue_box.animation_played = False
    
    def draw(self) -> None:
        """Function that draws the dialogue text and ui
        """
        if self.current_node['title'] != "End":
            self.screen.fill((0, 0, 0))
            self.dialogue_box.set_text(self.current_node['body'])
            if self.dialogue_started: # First time dialogue is shown, play box in animation
                for frame in self.dialogue_box.video_in:
                    self.screen.blit(frame, (self.dialogue_box.box_x, self.dialogue_box.box_y))
                    pygame.display.flip()
                    pygame.time.delay(60)  # Adjust delay for speed of animation
                self.dialogue_started = False
            elif self.dialogue_active: # Dialogue is active, render text and play box loop animation
                self.dialogue_box.render_bg()
                self.dialogue_box.render_text()
                pygame.display.flip()
        else: # Dialogue has ended, play box out animation
            for frame in self.dialogue_box.video_out:
                self.screen.fill((0, 0, 0))
                self.screen.blit(frame, (self.dialogue_box.box_x, self.dialogue_box.box_y))
                pygame.display.flip()
                pygame.time.delay(60)  # Adjust delay for speed of animation
