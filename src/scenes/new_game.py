"""New Game Scene"""

import pygame
from src.ui.interaction import DialogueManager
from src.characters.player import Player

class NewGame:
    def __init__(self, screen, interactions):
        self.screen = screen
        self.interactions = interactions
        self.dialogue_manager = DialogueManager(interactions)
        self.player = Player()  # Initialize the Player object
        
        self.character_creator_active = True
        self.game_begin = False
    
    # FIXME: This method should display the initial dialogue after character creation and before the game starts
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.dialogue_manager.dialogue_active:
            if event.key == pygame.K_z:
                self.dialogue_manager.next_line()
                if not self.dialogue_manager.dialogue_active:
                    self.game_begin = True
            self.dialogue_manager.draw(self.screen)
                
            
    def draw_character_creator(self):
        self.screen.fill((0, 0, 0))
        self.dialogue_manager.draw(self.screen)
        pygame.display.flip()
        # Display player stats selection screen
        font = pygame.font.Font(None, 36)
        points = 8 # Assuming the player has 8 points to distribute
        text = font.render("Choose your stats:", True, (255, 255, 255))
        text_2 = font.render("Available Points: {points}", True, (255, 255, 255))
        self.screen.blit(text, (50, 50))
        self.screen.blit(text_2, (50, 100))

        # Display player stats using the Player object
        stats = self.player.get_skills()  # Assuming Player class has a get_stats method
        y_offset = 200
        for stat, value in stats.items():
            stat_text = font.render(f"{stat}: {value}", True, (255, 255, 255))
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
            
            confirm_text = font.render("Press Z to confirm", True, (255, 255, 255))
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
            self.screen.blit(font.render(f"Available Points: {points}", True, (255, 255, 255)), (50, 100))

            y_offset = 200
            for i, (stat, value) in enumerate(stats.items()):
                color = (255, 0, 0) if i == selected_skill else (255, 255, 255)
                stat_text = font.render(f"{stat}: {value}", True, color)
                self.screen.blit(stat_text, (50, y_offset))
                y_offset += 50

            self.screen.blit(confirm_text, (50, y_offset + 50))
            pygame.display.flip()
            pygame.time.wait(100)
        
        self.dialogue_manager.dialogue_active = True
        self.character_creator_active = False
        self.screen.fill((0, 0, 0))
        self.player.set_skills(stats)  # Assuming Player class has a set_skills method

    def return_player(self):
        return self.player