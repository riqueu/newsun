"""Main Module with Game Class"""

import pygame
import sys

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
        pygame.display.set_icon(pygame.image.load('assets/images/newsun.jpg'))
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.time=pygame.time.get_ticks()
        self.running = True  # Set a running flag for game control
        
        # Scene initialization
        self.main_menu = MainMenu(self.screen) 
        self.options_menu = OptionsMenu(self.screen)
        self.pause_menu = PauseMenu(self.screen)
        
        # Game variables
        self.menu_state = "main"
        self.interaction_state = False
        
        # TODO: Implement Fade in/out effect between scenes
        self.fade = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        self.fade.fill((0, 0, 0, 0))
        self.fade_alpha = 255

    def handle_events(self):
        # outside event loop to allow for continuous movement
        if self.menu_state == "game" and not self.interaction_state:
            keys = pygame.key.get_pressed()
            self.player.handle_movement(keys)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.menu_state == "game":
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load('assets/music/newsun_hotel.ogg')
                    pygame.mixer.music.play(-1)  # Loop the music indefinitely
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu_state = "pause"
                        pygame.mixer.music.pause()
            
            if self.menu_state == "main":
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load('assets/music/main.ogg')
                    pygame.mixer.music.play(-1)  # Loop the music indefinitely
            
                selected_option = self.main_menu.handle_event(event)
                if selected_option == "Start Game":
                    self.new_game = NewGame(self.screen)
                    self.menu_state = "new_game"
                    
                elif selected_option == "Options":
                    self.options_menu.previous_screen = "main"
                    self.menu_state = "options" 
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
                if self.new_game.dialogue_manager.dialogue_active and not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load('assets/music/new_game_conversation.ogg')
                    pygame.mixer.music.play(-1)
                if self.new_game.game_begin:
                    self.screen.fill((0, 0, 0))
                    self.load_map()
                    self.menu_state = "game"
                    self.player = self.new_game.player
                    pygame.mixer.music.stop()
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('assets/sounds/door_knock_angry.mp3'))
            else:
                pass


    def load_map(self):
        """Method that creates the map
        """
        self.room_101 = Room101(self.screen)
        
    def update(self):
        # Placeholder for updating game logic
        pygame.display.update()

    def draw(self):
        self.screen.fill((0, 0, 0))
        if self.menu_state == "main":
            self.main_menu.draw()
        elif self.menu_state == "options":
            self.options_menu.draw()
        elif self.menu_state == "new_game":
            self.new_game.draw()
        elif self.menu_state == "game":
            self.room_101.draw()
            self.player.draw()
        elif self.menu_state == "pause":
            self.pause_menu.draw()
        else:
            pass
        
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
