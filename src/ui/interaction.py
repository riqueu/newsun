"""
Module for managing player dialogue interactions in the game.

This module handles displaying dialogue, player choices, skill checks, and updating game states based on decisions. 
It also integrates animations for a dynamic interaction experience.

Classes:
    - DialogueBox: Displays dialogue and handles text wrapping and animations.
    - DialogueManager: Manages the dialogue flow, including player choices and skill checks.

Functions:
    - get_key_to_node: Maps player choices to the next dialogue node.
    - load_scene_interactions: Loads dialogue data for a scene from JSON files.
"""

import pygame
import os
import json

from src.ui.animated_sequence import vid_roll, vid_pass, vid_fail, video, video_in, video_out
from src.characters.player import Player
from settings import WIDTH, HEIGHT


def get_key_to_node(interactions: dict) -> dict:
    """Extracts the dialogue options and returns a mapping of titles to the next node keys.

    Args:
        interactions (dict): Dictionary containing the interactions data.

    Returns:
        dict: A mapping of interaction titles to the keys that point to the next dialogue node.
    """
    return {interaction['title']: interaction['key'] for interaction in interactions if 'key' in interaction}


def load_scene_interactions(scripts_path: str, screen: pygame.Surface) -> dict:
    """Loads all the interactions in a scene from JSON files and creates dialogue managers.

    Args:
        scripts_path (str): Path to the folder containing the scene's interaction files.
        screen (pygame.Surface): The screen where the dialogues will be rendered.

    Returns:
        dict: A dictionary containing dialogue managers for each interaction in the scene.
    """
    interactions = {}
    key_to_node = {}
    dialogue_managers = {}
    # Iterate through all files in the provided directory to find JSON files.
    for filename in os.listdir(scripts_path):
        if filename.endswith('.json'):
            file_path = os.path.join(scripts_path, filename)
            # Open and load the interaction data from the JSON file.
            with open(file_path, 'r', encoding="utf8") as file:
                interaction = json.load(file)
                key = filename.split('.')[0]
                # Store the interaction data in the 'interactions' dictionary.
                interactions[key] = interaction
                # Generate the key-to-node mapping for dialogue navigation.
                key_to_node[key] = get_key_to_node(interaction)
                dialogue_managers[key] = DialogueManager(screen, interaction, key_to_node[key])
    return dialogue_managers


class DialogueBox:
    """
    Class for managing the dialogue box UI in the game.

    The `DialogueBox` class handles the rendering of the dialogue box and its text, 
    including wrapping the text to fit within the box and animating the text display.
    """
    def __init__(self, screen: pygame.Surface) -> None:
        """
        Initializes the DialogueBox object.

        Args:
            screen (pygame.Surface): The surface (screen) where the dialogue box will be drawn.
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
        """
        Sets the text to be displayed in the dialogue box.

        Args:
            text (str): The text to be shown in the dialogue box.
        """
        self.text = text
        self.lines = self.wrap_text(text)

    def wrap_text(self, text: str) -> list:
        """
        Wraps the input text to fit within the width of the dialogue box.

        Args:
            text (str): The text to be wrapped.

        Returns:
            list: A list of strings, each fitting within the box width.
        """
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            if '\n' in word: # Handle newline character in words
                parts = word.split('\n')
                for part in parts[:-1]:
                    test_line = current_line + part + " "
                    lines.append(test_line.strip())   # Add the current line to lines list
                    current_line = ""
                current_line = parts[-1] + " "
            else:
                test_line = current_line + word + " "
                if self.font.size(test_line)[0] <= self.box_width - 35:  # Adjusted to fit within the box
                    current_line = test_line
                else:
                    lines.append(current_line.strip())   # If the line is too long, finalize it and add to lines
                    current_line = word + " "

        if current_line.strip():
            lines.append(current_line.strip())
        
        return lines

    def render_bg(self) -> None:
        """
        Renders the background of the dialogue box, including its animations (video_in, video_out, or video).
        Handles the animation states and draws the corresponding video.
        """
        if video_in.status:  # If the 'video_in' animation is active, draw and animate it
            video_in.draw(self.screen)
            video_in.animate()
            
        elif video_out.status:  # If the 'video_out' animation is active, draw and animate it
            video_out.draw(self.screen)
            video_out.animate()

        else:  # If no specific video animation is active, draw the default 'video' animation
            video.draw(self.screen)
            video.animate()


    def render_text(self) -> None: 
        """
        Renders the dialogue text with an animation effect, revealing characters gradually.
        The speed at which the text is rendered can be adjusted.
        """
        lines = self.wrap_text(self.text)  # Wrap the text to fit the box
        text_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        text_surface.fill((0, 0, 0, 0))
        
        # Initialize time tracking if it's a new text or if it hasn't been set
        if (not hasattr(self, 'current_time')) or self.new_text:
            self.current_time = pygame.time.get_ticks()
            self.new_text = False
        
        text_speed = 10  # Change text speed (lower -> faster)
        total_chars = sum(len(line) for line in lines)
        elapsed_time = pygame.time.get_ticks() - self.current_time
        max_chars = min((elapsed_time // text_speed), total_chars)
        current_chars = 0
        
        # Loop through each line and render part of the text
        for line in lines:
            if current_chars + len(line) < max_chars:
                rendered_line = self.font.render(line, True, (255, 255, 255))
                text_surface.blit(rendered_line, (20, 50 + lines.index(line) * 40))
                current_chars += len(line)
            else:  # If the line should be cut off at max_chars
                rendered_line = self.font.render(line[:max_chars - current_chars], True, (255, 255, 255))
                text_surface.blit(rendered_line, (20, 50 + lines.index(line) * 40))
                current_chars += len(line[:max_chars - current_chars])
                break
        
        # Determine if the text has finished rendering
        if current_chars >= total_chars:
            self.rendered_done = True
        else:
            self.rendered_done = False
        
        self.screen.blit(text_surface, (self.box_x, self.box_y))  # Finally, blit the surface with text

    def draw(self) -> None:
        """
        Draws the dialogue box and the text inside it.
        This function is responsible for rendering the entire dialogue UI.
        """
        self.render_bg()
        self.render_text()        


class DialogueManager:
    """
    Class that manages dialogue flow in the game.

    The DialogueManager handles the display of dialogue, transitions between nodes, and player interactions.
    It manages dialogue boxes, animations, and updates player stats based on choices.
    """
    def __init__(self, screen: pygame.Surface, dialogue_data: list, key_to_node: dict) -> None:
        """Initializes the DialogueManager.

        Sets up the dialogue flow, initializing variables and linking the dialogue data with the screen.
        
        Args:
            screen (pygame.Surface): The game screen where dialogue will be displayed.
            dialogue_data (list): List of nodes that contain dialogue and interaction data.
            key_to_node (dict): Maps interaction choices (keys) to corresponding dialogue nodes.
        """
        self.screen = screen
        self.key_to_node = key_to_node
        self.dialogue_data = dialogue_data
        self.current_node = self.find_node("Start")
        self.next_node_title = None
        self.dialogue_box = DialogueBox(screen)
        
        # Initialize state flags
        self.dialogue_active = False
        self.dialogue_ended = False
        self.check_done = False
        
        # Count how many "Start" nodes exist (for branching dialogue)
        self.start_count = sum(1 for node in self.dialogue_data if "Start" in node['title'])
        self.nodes_with_body = [node for node in self.dialogue_data if 'body' in node]
        
        self.player = Player(self.screen) # Access singleton player object
    
    def find_node(self, title: str) -> dict|None:
        """Finds and returns a node based on its title.

        Args:
            title (str): The title of the node to find.

        Returns:
            dict | None: The node matching the title or None if not found.
        """
        for node in self.dialogue_data:
            if node['title'] == title:
                return node
        return None

    def handle_event(self, event: pygame.event.Event, condition: int = 1) -> None:
        """Handles dialogue and interaction events during the game.

        Args:
            event (pygame.event.Event): The current event to process.
            condition (int): Used to handle multiple "Start" nodes if applicable.
        """
        if self.current_node['title'] == "Start":
            if self.start_count > 1:
                self.current_node = self.find_node(f"Start{condition}")
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
        
        # Handle key press to navigate dialogue
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
        """Draws the dialogue box and its elements to the screen.

        Handles rendering of the dialogue box, text, and animations (e.g., skill check videos).
        """
        if self.current_node in self.nodes_with_body:
            self.dialogue_box.set_text(self.current_node['body'])
            # Render dialogue if it's active, and animate the text
            if not self.dialogue_ended or video_out.status:
                self.dialogue_box.draw()
            else:
                # Resets dialogue manager to start when dialogue ends
                self.current_node = self.find_node("Start")
                self.dialogue_ended = False
            
		# Render skill check animations based on current status
        if vid_roll.status:
            vid_roll.draw(self.screen)
            vid_roll.animate()
                
        if vid_pass.status:
            vid_pass.draw(self.screen)
            vid_pass.animate()
                
        if vid_fail.status:
            vid_fail.draw(self.screen)
            vid_fail.animate()
