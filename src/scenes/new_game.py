"""New Game Scene"""

import pygame
from src.ui.interaction import DialogueManager, get_key_to_node
from src.characters.player import Player

class NewGame:
    def __init__(self, screen, interactions):
        self.screen = screen
        self.key_to_node = get_key_to_node(interactions)
        self.dialogue_manager = DialogueManager(self.screen, interactions, self.key_to_node)
        self.player = Player(self.screen)  # Initialize the Player object
        
        self.character_creator_active = True
        self.game_begin = False
    
    def handle_event(self, event):
        if self.dialogue_manager.dialogue_ended:
                self.game_begin = True
                pygame.mixer.music.stop()
        elif self.dialogue_manager.dialogue_active:
            self.dialogue_manager.handle_event(event)
                
            
    def draw_character_creator(self):
        self.screen.fill((0, 0, 0))
        # self.dialogue_manager.draw()
        pygame.display.flip()
        # Display player stats selection screen
        self.font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 26)
        points = 8 # Assuming the player has 8 points to distribute
        text = self.font.render("Choose your stats:", True, (255, 255, 255))
        text_2 = self.font.render("Available Points: {points}", True, (255, 255, 255))
        self.screen.blit(text, (50, 50))
        self.screen.blit(text_2, (50, 100))

        # Display player stats using the Player object
        stats = self.player.get_skills()  # Assuming Player class has a get_stats method
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

        begin = False
        
        while True:
            if begin:
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
                        begin = True

            # Redraw the screen
            self.screen.fill((0, 0, 0))
            self.screen.blit(text, (50, 50))
            self.screen.blit(self.font.render(f"Available Points: {points}", True, (255, 255, 255)), (50, 100))
                        
            description_text = descriptions[skill_names[selected_skill]]
            description_lines = description_text.split('\n')
            for i, line in enumerate(description_lines):
                description_surface = self.font.render(line, True, (255, 255, 255))
                self.screen.blit(description_surface, (500, y_offset - 250 + i * 30))

            y_offset = 200
            for i, (stat, value) in enumerate(stats.items()):
                color = (255, 0, 0) if i == selected_skill else (255, 255, 255)
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
        self.player.set_skills(stats)  # Assuming Player class has a set_skills method

    def return_player(self):
        return self.player