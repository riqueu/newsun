"""Main Module"""

import pygame
import sys
import json
from settings import WIDTH, HEIGHT, FPS
from src.scenes.main_menu import MainMenu
from src.scenes.options_menu import OptionsMenu
from src.scenes.pause_menu import PauseMenu

from src.scenes.room_101 import Room101
from src.scenes.new_game import NewGame

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Newsun")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True  # Set a running flag for game control
        self.font = pygame.font.SysFont("arialblack", 36)  # Default font for text
        
        # Interactions
        self.new_game_interactions = json.load(open('scripts/new_game.json'))
        self.room_101_interactions = json.load(open('scripts/room_101.json'))
            
        
        # Scene initialization
        self.main_menu = MainMenu(self.screen)  # Initialize MainMenu
        self.options_menu = OptionsMenu(self.screen)  # Initialize OptionsMenu
        self.new_game = NewGame(self.screen, self.new_game_interactions)  # Initialize NewGame
        self.pause_menu = PauseMenu(self.screen)  # Initialize PauseMenu
        
        self.room_101 = Room101(self.screen, self.room_101_interactions)  # Initialize Room101
        
        # Game variables
        self.menu_state = "main"

    def draw_text(self, text, font, color, x, y):
        img = font.render(text, True, color)
        self.screen.blit(img, (x, y))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.menu_state == "game":
                # TODO: Find the hotel soundtrack
                # pygame.mixer.music.load('assets/music/newsun_hotel.ogg')
                # pygame.mixer.music.play(-1)  # Loop the music indefinitely
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu_state = "pause"
                        pygame.mixer.music.pause()
            
            if self.menu_state == "main":
                # TODO: Check if audio gets paused when entering the options menu (shouldn't happen)
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load('assets/music/main.ogg')
                    pygame.mixer.music.play(-1)  # Loop the music indefinitely
            
                selected_option = self.main_menu.handle_event(event)
                if selected_option == "Start Game":
                    self.menu_state = "new_game" # "game"  # Start the game
                    
                elif selected_option == "Options":
                    self.options_menu.previous_screen = "main"
                    self.menu_state = "options"  # Enter options menu
                elif selected_option == "Exit":
                    self.running = False  # Exit the game
            
            elif self.menu_state == "pause":
                selected_option = self.pause_menu.handle_event(event)
                if selected_option == "Resume":
                    self.screen.fill((0, 0, 0))
                    self.menu_state = "game"
                    pygame.mixer.music.unpause()
                elif selected_option == "Options":
                    self.options_menu.previous_screen = "pause"
                    self.menu_state = "options"
                elif selected_option == "Exit":
                    self.running = False
            
            elif self.menu_state == "options":
                selected_option = self.options_menu.handle_event(event)
                if selected_option == "Back":
                    self.menu_state = self.options_menu.previous_screen # main menu/pause menu
                
            elif self.menu_state == "new_game":
                self.new_game.handle_event(event)
                if self.new_game.game_begin:
                    pygame.mixer.music.stop()  # Stop the menu music
                    self.menu_state = "game"
                    self.player = self.new_game.player
                    pygame.mixer.music.load('assets/sounds/door_knock_angry.mp3')
                    pygame.mixer.music.play()
            
            else:
                pass


    def update(self):
        # Placeholder for updating game logic
        pygame.display.update()

    def draw(self):
        if self.menu_state == "main":
            self.main_menu.draw()
        elif self.menu_state == "options":
            self.options_menu.draw()
        elif self.menu_state == "new_game" and self.new_game.character_creator_active:
            self.new_game.draw_character_creator()
        elif self.menu_state == "game":
            self.room_101.draw()
        elif self.menu_state == "pause":
            self.pause_menu.draw()
        else:
            self.screen.fill((0, 0, 0))  # Clear screen with black; adjust as needed
            pygame.display.flip()  # Update the entire screen

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
