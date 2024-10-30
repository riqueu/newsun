import pygame
import sys
import json
from settings import WIDTH, HEIGHT, FPS
from src.scenes.main_menu import MainMenu
from src.scenes.options_menu import OptionsMenu

from src.scenes.room_101 import Room101 

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Newsun")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True  # Set a running flag for game control
        self.font = pygame.font.SysFont("arialblack", 36)  # Default font for text
        
        # Interactions
        self.room_101_interactions = json.load(open('scripts/room_101.json'))
            
        
        # Scene initialization
        self.main_menu = MainMenu(self.screen)  # Initialize MainMenu
        self.options_menu = OptionsMenu(self.screen)  # Initialize OptionsMenu
        self.room_101 = Room101(self.screen, self.room_101_interactions)  # Initialize Room101
        
        # Game variables
        self.game_paused = False
        self.menu_state = "main"

    def draw_text(self, text, font, color, x, y):
        img = font.render(text, True, color)
        self.screen.blit(img, (x, y))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.menu_state == "main" or self.menu_state == "options":
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load('assets/music/main.ogg')
                    pygame.mixer.music.play(-1)  # Loop the music indefinitely
                if self.menu_state == "main":
                    selected_option = self.main_menu.handle_event(event)
                    if selected_option == "Start Game":
                        self.menu_state = "game"  # Start the game
                        pygame.mixer.music.stop()  # Stop the menu music
                        pygame.mixer.music.load('assets/sounds/door_knock_angry.mp3')
                        pygame.mixer.music.play()
                    elif selected_option == "Options":
                        self.menu_state = "options"  # Enter options menu
                    elif selected_option == "Exit":
                        self.running = False  # Exit the game
                
                elif self.menu_state == "options":
                    selected_option = self.options_menu.handle_event(event)
                    if selected_option == "Back":
                        self.menu_state = "main"
            
            elif self.menu_state == "game":
                pass
            
            elif self.game_paused:
                pass
            
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
        elif self.menu_state == "game":
            self.room_101.draw()
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
