"""Module for handling dialogue interactions with the player."""

import pygame
import os
import json

from src.ui.animated_sequence import vid_roll, vid_pass, vid_fail, video, video_in, video_out
from src.characters.player import Player
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
            with open(file_path, 'r', encoding="utf8") as file:
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
        self.rendered_done = False

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
                if self.font.size(test_line)[0] <= self.box_width - 35:  # Adjusted to fit within the box
                    current_line = test_line
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "

        if current_line.strip():
            lines.append(current_line.strip())
        
        return lines

    def render_bg(self) -> None:
        """Function that renders the background of the box & its animations
        """
        if video_in.status:
            video_in.draw(self.screen)
            video_in.animate()
            
        elif video_out.status:
            video_out.draw(self.screen)
            video_out.animate()

        else:
            video.draw(self.screen)
            video.animate()


    def render_text(self) -> None:
        """Function that renders the text with animation
        """
        lines = self.wrap_text(self.text)
        text_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        text_surface.fill((0, 0, 0, 0))
        
        if (not hasattr(self, 'current_time')) or self.new_text:
            self.current_time = pygame.time.get_ticks()
            self.new_text = False
        
        text_speed = 10  # Change text speed (lower -> faster)
        total_chars = sum(len(line) for line in lines)
        elapsed_time = pygame.time.get_ticks() - self.current_time
        max_chars = min((elapsed_time // text_speed), total_chars)
        current_chars = 0
        
        for line in lines:
            if current_chars + len(line) < max_chars:
                rendered_line = self.font.render(line, True, (255, 255, 255))
                text_surface.blit(rendered_line, (20, 50 + lines.index(line) * 40))
                current_chars += len(line)
            else:
                rendered_line = self.font.render(line[:max_chars - current_chars], True, (255, 255, 255))
                text_surface.blit(rendered_line, (20, 50 + lines.index(line) * 40))
                current_chars += len(line[:max_chars - current_chars])
                break
        
        if current_chars >= total_chars:
            self.rendered_done = True
        else:
            self.rendered_done = False
        
        self.screen.blit(text_surface, (self.box_x, self.box_y))

    def draw(self) -> None:
        """Function that draws the dialogue box and text
        """
        self.render_bg()
        self.render_text()        


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
        self.next_node_title = None
        self.dialogue_box = DialogueBox(screen)
        
        self.dialogue_active = False
        self.dialogue_ended = False
        self.check_done = False
        
        self.start_count = sum(1 for node in self.dialogue_data if "Start" in node['title'])
        self.nodes_with_body = [node for node in self.dialogue_data if 'body' in node]
        
        self.player = Player(self.screen) # Access singleton player object
    
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
        if self.current_node['title'] == "Start":
            if self.start_count > 1:
            # TODO: Either go to start 1 or 2 depending on conditions, default to start 1 for now
                self.current_node = self.find_node("Start1")
            video_in.status = True
            video_out.status = False
        
        elif self.current_node['title'] == "End":
            video_out.status = True
            self.dialogue_ended = True
            self.dialogue_active = False
        
        # Check if the current node is a check node
        elif "Check" in self.current_node['title']:
            skill_name = self.current_node.get('check_skill')
            difficulty_class = self.current_node.get('difficulty_class')
            if skill_name and difficulty_class:
                check_result = self.player.roll_skill_check(skill_name, difficulty_class)
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('assets/sounds/check_roll.mp3'))
                
                vid_roll.status = True
                
                if check_result == True:
                    pygame.mixer.Channel(1).queue(pygame.mixer.Sound('assets/sounds/check_pass.mp3'))
                    vid_pass.status = True
                    self.next_node_title = self.current_node['title'].replace("Check", "Pass")
                
                elif check_result == False:
                    pygame.mixer.Channel(1).queue(pygame.mixer.Sound('assets/sounds/check_fail.mp3'))
                    vid_fail.status = True
                    self.next_node_title = self.current_node['title'].replace("Check", "Fail")
                
                if self.next_node_title:
                    self.current_node = self.find_node(self.next_node_title)
                    
                    self.dialogue_box.animation_played = False
                
        elif event.type == pygame.KEYDOWN:
            pressed_key = event.unicode
            if self.dialogue_box.rendered_done:
                self.next_node_title = self.current_node['key'].get(pressed_key)
            if self.next_node_title:
                # Change player stats based on the node after the key pressed
                if 'reason' in self.current_node:
                    self.player.reason += self.current_node['reason']
                if 'health' in self.current_node:
                    self.player.health += self.current_node['health']
                self.current_node = self.find_node(self.next_node_title)
                self.dialogue_box.animation_played = False
                self.dialogue_box.new_text = True
                self.next_node_title = None
    
    def draw(self) -> None:
        """Function that draws the dialogue text and ui
        """
        if self.current_node in self.nodes_with_body:
            self.dialogue_box.set_text(self.current_node['body'])
            # Dialogue is active, render text and play box loop animation
            if not self.dialogue_ended or video_out.status:
                self.dialogue_box.draw()
            else:
                # Resets dialogue manager to start when dialogue ends
                self.current_node = self.find_node("Start")
                self.dialogue_ended = False
                
        if vid_roll.status:
            vid_roll.draw(self.screen)
            vid_roll.animate()
                
        if vid_pass.status:
            vid_pass.draw(self.screen)
            vid_pass.animate()
                
        if vid_fail.status:
            vid_fail.draw(self.screen)
            vid_fail.animate()
