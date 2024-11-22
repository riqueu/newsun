"""New Game Scene"""

import pygame
import json

from src.ui.interaction import DialogueManager, get_key_to_node
from src.ui.animated_sequence import black_bg, dialogue_box_left, skill_desc
from src.characters.player import Player

class NewGame:
    def __init__(self, screen: pygame.Surface) -> None:
        """Function that initializes the NewGame object

        Args:
            screen (pygame.Surface): The screen.
        """
        self.screen = screen
        # self.interactions = json.load(open('scripts/new_game/new_game.json'))
        self.interactions = json.load(open('scripts/room_101/mirror.json'))
        self.key_to_node = get_key_to_node(self.interactions)
        self.dialogue_manager = DialogueManager(self.screen, self.interactions, self.key_to_node)
        self.font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 24)
        self.player = Player(self.screen)  # Initialize the Player object
        
        self.points = 8 # Points to distribute
        self.stats = self.player.get_skills()  # Get the player stats
        self.descriptions = self.player.get_skills_description()  # Get the player stats descriptions
        self.skill_names = list(self.stats.keys())
        self.selected_skill = 0
        
        self.character_creator_active = True
        self.game_begin = False
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Function that calls and handles dialogue interaction and character creation events for this scene

        Args:
            event (pygame.event.Event): current event
        """
        if self.character_creator_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_skill = (self.selected_skill - 1) % len(self.skill_names)
            elif event.key == pygame.K_DOWN:
                self.selected_skill = (self.selected_skill + 1) % len(self.skill_names)
            elif event.key == pygame.K_RIGHT and self.points > 0:
                self.stats[self.skill_names[self.selected_skill]] += 1
                self.points -= 1
            elif event.key == pygame.K_LEFT and self.stats[self.skill_names[self.selected_skill]] > 0:
                self.stats[self.skill_names[self.selected_skill]] -= 1
                self.points += 1
            elif event.key == pygame.K_z:
                self.character_creator_active = False
                self.dialogue_manager.dialogue_started = True
                self.dialogue_manager.dialogue_active = True
                pygame.mixer.music.stop()
                self.player.set_skills(self.stats)
                    
        elif self.dialogue_manager.dialogue_active:
            self.dialogue_manager.handle_event(event)
        
        if self.dialogue_manager.dialogue_ended:
            self.game_begin = True
            pygame.mixer.music.stop()

    """def draw_ui(self) -> None:
        Function that draws the png sequence of the UI
        
        dialogue_box_left.draw(self.screen)
        dialogue_box_left.animate()
        
        skill_desc.draw(self.screen)
        skill_desc.animate()"""
            
    def draw(self) -> None:
        """Function that handles the character creator part of the new game scene
        """      

        black_bg.draw(self.screen)
        black_bg.animate()
        
        if self.character_creator_active:
            dialogue_box_left.draw(self.screen)
            dialogue_box_left.animate()
            
            skill_desc.draw(self.screen)
            skill_desc.animate()
            
            # Display player stats selection screen (8 points to distribute)
            text = self.font.render("Choose your stats:", True, (255, 255, 255))
            text_2 = self.font.render(f"Available Points: {self.points}", True, (255, 255, 255))

            self.screen.blit(text, (50, 50))
            self.screen.blit(text_2, (50, 100))

            # Display player stats using the Player object
            y_offset = 200
            for stat, value in self.stats.items():
                color = (255, 255, 255) if stat == self.skill_names[self.selected_skill] else (175, 175, 175)
                stat_text = self.font.render(f"{stat}: {value}", True, color)
                self.screen.blit(stat_text, (50, y_offset))
                y_offset += 50

            # Display descriptions
            description_text = self.descriptions[self.skill_names[self.selected_skill]]
            description_lines = description_text.split('\n')
            for i, line in enumerate(description_lines):
                description_surface = self.font.render(line, True, (255, 255, 255))
                self.screen.blit(description_surface, (500, y_offset - 250 + i * 30))

            confirm_text = self.font.render("Press Z to confirm", True, (255, 255, 255))
            self.screen.blit(confirm_text, (50, y_offset + 50))
        else:
            self.dialogue_manager.draw()