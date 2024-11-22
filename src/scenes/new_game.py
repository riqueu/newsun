"""New Game Scene"""

import pygame
import json

from src.ui.interaction import DialogueManager, get_key_to_node
from src.ui.animated_sequence import load_png_sequence, sequence_current_frame
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
        
        self.skills_bg = load_png_sequence('assets/ui/DialogueBox')
        self.desc_bg = load_png_sequence('assets/ui/SkillDesc')
        self.black_bg = load_png_sequence('assets/ui/BlackBG')
        
        self.character_creator_active = True
        self.game_begin = False
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Function that calls and handles dialogue interaction for this scene

        Args:
            event (pygame.event.Event): current event
        """
        if self.dialogue_manager.dialogue_ended:
                self.game_begin = True
                pygame.mixer.music.stop()
        elif self.dialogue_manager.dialogue_active:
            self.dialogue_manager.handle_event(event)
    
    def draw_ui(self) -> None:
        """Function that draws the png sequence of the UI
        """
        self.screen.blit(sequence_current_frame(self.desc_bg), (450,100))
        self.screen.blit(sequence_current_frame(self.skills_bg), (0,0))
            
    def draw_character_creator(self) -> None:
        """Function that handles the character creator part of the new game scene
        """
        # self.screen.fill((0, 0, 0))
        self.screen.blit(sequence_current_frame(self.black_bg), (0,0))
        pygame.display.flip()
        
        # Display player stats selection screen (8 points to distribute)
        points = 8
        text = self.font.render("Choose your stats:", True, (255, 255, 255))
        text_2 = self.font.render("Available Points: {points}", True, (255, 255, 255))

        self.screen.blit(text, (50, 50))
        self.screen.blit(text_2, (50, 100))

        # Display player stats using the Player object
        stats = self.player.get_skills()
        descriptions = self.player.get_skills_description()
        y_offset = 200
        for stat, value in stats.items():
            stat_text = self.font.render(f"{stat}: {value}", True, (255, 255, 255))
            self.screen.blit(stat_text, (50, y_offset))
            y_offset += 50

        # Update the display
        pygame.display.flip()
        # Allow the player to distribute points among skills
        skill_names = list(stats.keys())
        selected_skill = 0

        leave_creator = False
        
        while True:
            if leave_creator:
                break
        
            confirm_text = self.font.render("Press Z to confirm", True, (255, 255, 255))
            self.screen.blit(confirm_text, (50, y_offset + 50))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_skill = (selected_skill - 1) % len(skill_names)
                    elif event.key == pygame.K_DOWN:
                        selected_skill = (selected_skill + 1) % len(skill_names)
                    elif event.key == pygame.K_RIGHT and points > 0:
                        stats[skill_names[selected_skill]] += 1
                        points -= 1
                    elif event.key == pygame.K_LEFT and stats[skill_names[selected_skill]] > 0:
                        stats[skill_names[selected_skill]] -= 1
                        points += 1
                    elif event.key == pygame.K_z:
                        leave_creator = True

            # Redraw the screen
            # self.screen.fill((0, 0, 0))
            self.screen.blit(sequence_current_frame(self.black_bg), (0,0))
            self.draw_ui()
            self.screen.blit(text, (50, 50))
            self.screen.blit(self.font.render(f"Available Points: {points}", True, (255, 255, 255)), (50, 100))
                        
            description_text = descriptions[skill_names[selected_skill]]
            description_lines = description_text.split('\n')
            for i, line in enumerate(description_lines):
                description_surface = self.font.render(line, True, (255, 255, 255))
                self.screen.blit(description_surface, (500, y_offset - 250 + i * 30))

            y_offset = 200
            for i, (stat, value) in enumerate(stats.items()):
                color = (255, 255, 255) if i == selected_skill else (175, 175, 175)
                stat_text = self.font.render(f"{stat}: {value}", True, color)
                self.screen.blit(stat_text, (50, y_offset))
                y_offset += 50

            self.screen.blit(confirm_text, (50, y_offset + 50))
            pygame.display.flip()
            pygame.time.wait(100)
        
        self.dialogue_manager.dialogue_started = True
        self.dialogue_manager.dialogue_active = True
        self.character_creator_active = False
        pygame.mixer.music.stop()
        self.screen.fill((0, 0, 0))
        # self.screen.blit(sequence_current_frame(self.black_bg), (0,0))
        self.player.set_skills(stats)
