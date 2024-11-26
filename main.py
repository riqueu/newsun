import pygame
from src.config import *
from src.sprites import *
import sys

from settings import WIDTH, HEIGHT, FPS
from src.scenes.main_menu import MainMenu
from src.scenes.options_menu import OptionsMenu
from src.scenes.pause_menu import PauseMenu
from src.scenes.new_game import NewGame
from src.scenes.ending_menu import EndingMenu
from src.scenes.hotel_scenes import *


class Game:
    def __init__(self) -> None:
        """Initialize the Game
        """
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
        self.ending_menu = EndingMenu(self.screen)
        
        self.game_scenes = []
        
        # Game variables
        self.menu_state = "main"
        self.interaction_state = False
        self.current_scene = None
        
        # TODO: Implement Fade in/out effect between scenes
        self.fade = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        self.fade.fill((0, 0, 0, 0))
        self.fade_alpha = 255

    def handle_events(self) -> None:
        """Handles events in the game
        """
        # outside event loop to allow for continuous movement
        if self.menu_state == "game":
            keys = pygame.key.get_pressed()
            self.player.handle_movement(keys)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            
            if self.menu_state == "game":
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load('assets/music/newsun_hotel.ogg')
                    pygame.mixer.music.play(-1)  # Loop the music indefinitely
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu_state = "pause"
                        pygame.mixer.music.pause()
                        
                if self.current_scene == "room_101":
                    self.room_101.handle_event(event)
                elif self.current_scene == "floor_1":
                    self.floor_1.handle_event(event)
                elif self.current_scene == "floor_0":
                    self.floor_0.handle_event(event)
                elif self.current_scene == "underground":
                    self.underground.handle_event(event)
            
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
            
            elif self.menu_state == "ending":
                selected_option = self.ending_menu.handle_event(event)
                if selected_option == "quit":
                    self.running = False
            
            elif self.menu_state == "pause":
                selected_option = self.pause_menu.handle_event(event)
                if selected_option == "Resume":
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
                    self.load_map()
                    self.menu_state = "game"
                    self.current_scene = "room_101"
                    self.player = self.new_game.player
                    pygame.mixer.music.stop()
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('assets/sounds/door_knock_angry.mp3'))
            else:
                pass

    def load_map(self) -> None:
        """Method that creates the map
        """
        self.room_101 = Room101(self.screen)
        self.floor_1 = Floor1(self.screen)
        self.floor_0 = Floor0(self.screen)
        self.underground = Underground(self.screen)

    def draw(self) -> None:
        """Method that renders the game
        """
        self.screen.fill((0, 0, 0))
        if self.menu_state == "main":
            self.main_menu.draw()
        elif self.menu_state == "ending":
            self.ending_menu.draw()
        elif self.menu_state == "options":
            self.options_menu.draw()
        elif self.menu_state == "new_game":
            self.new_game.draw()
        elif self.menu_state == "game":
            if self.current_scene == "room_101":
                self.room_101.draw()
            elif self.current_scene == "floor_1":
                self.floor_1.draw()
            elif self.current_scene == "floor_0":
                self.floor_0.draw()
            elif self.current_scene == "underground":
                self.underground.draw()
        elif self.menu_state == "pause":
            self.pause_menu.draw()
        else:
            pass
        
        pygame.display.flip()  # Update the entire screen

    def update(self) -> None:
        pass
    
    def run(self) -> None:
        """Method to run through the game loop
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        pass

class Camera:
    def __init__(self, game, width, height):
        self.game = game
        self.camera_rect = pygame.Rect(0, 0, width, height)
        self.offset = pygame.Vector2(0, 0)
        self.camera_borders = {'left': 200, 'right': 200, 'top': 300, 'bottom': 300}
        self.keyboard_speed = 5

    def box_target_camera(self, target):
        if target.rect.left < self.camera_rect.left + self.camera_borders['left']:
            self.camera_rect.left = target.rect.left - self.camera_borders['left']

        # Verificar se o jogador ultrapassou a borda direita da tela
        if target.rect.right > self.camera_rect.right - self.camera_borders['right']:
            self.camera_rect.right = target.rect.right + self.camera_borders['right']

        # Verificar se o jogador ultrapassou a borda superior da tela
        if target.rect.top < self.camera_rect.top + self.camera_borders['top']:
            self.camera_rect.top = target.rect.top - self.camera_borders['top']

        # Verificar se o jogador ultrapassou a borda inferior da tela
        if target.rect.bottom > self.camera_rect.bottom - self.camera_borders['bottom']:
            self.camera_rect.bottom = target.rect.bottom + self.camera_borders['bottom']

        # Atualiza o deslocamento da câmera para o movimento da tela
        self.offset.x = self.camera_rect.left 
        self.offset.y = self.camera_rect.top

    def keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_d]: self.camera_rect.x += self.keyboard_speed
        if keys[pygame.K_w]: self.camera_rect.y -= self.keyboard_speed
        if keys[pygame.K_s]: self.camera_rect.y += self.keyboard_speed

        self.offset.x = self.camera_rect.left
        self.offset.y = self.camera_rect.top

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()