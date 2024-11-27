import pygame
from src.characters.sprites import *
import sys

from settings import *
from src.ui.camera import Camera
from src.scenes.main_menu import MainMenu
from src.scenes.options_menu import OptionsMenu
from src.scenes.pause_menu import PauseMenu
from src.scenes.new_game import NewGame
from src.scenes.ending_menu import EndingMenu
from src.scenes.hotel_scenes import *


class Game:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """Create a new instance of the Game class if one does not already exist, i.e. Singleton pattern.

        Returns:
            _type_: The Player instance.
        """
        if not cls._instance:
            cls._instance = super(Game, cls).__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """Initialize the Game
        """
        if not hasattr(self, "initialized"):  # Prevent re-initialization
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
            self.all_sprites = pygame.sprite.LayeredUpdates()
            
            # Character & Camera initialization
            self.character_spritesheet = SpriteSheet('assets/images/characters/characters.png')
            self.camera = Camera(self, WIDTH, HEIGHT)
            
            # Game variables
            self.menu_state = "main"
            self.interaction_state = False
            self.current_scene = None

            self.initialized = True  #  Mark as initialized
            
    def handle_events(self) -> None:
        """Handles events in the game
        """
        # outside event loop to allow for continuous movement
        #if self.menu_state == "game":
            #keys = pygame.key.get_pressed()
            #self.player.handle_movement(keys)
        
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
                    

                    # TEMP: Change maps with number keys
                    if event.key == pygame.K_7:
                        self.change_map(self.current_scene, self.room_101)
                        self.current_scene = self.room_101
                    if event.key == pygame.K_8:
                        self.change_map(self.current_scene, self.floor_1)
                        self.current_scene = self.floor_1
                    if event.key == pygame.K_9:
                        self.change_map(self.current_scene, self.floor_0)
                        self.current_scene = self.floor_0
                    if event.key == pygame.K_0:
                        self.change_map(self.current_scene, self.underground)
                        self.current_scene = self.underground
                
                event_handled = self.current_scene.handle_event(event)
                # check if event is a scene change
                if event_handled in self.current_scene.scene_mapping.values():
                    self.change_map(self.current_scene, getattr(self, event_handled))
                    self.current_scene = getattr(self, event_handled)
                # check if game ended
                elif event_handled == "ending":
                    self.menu_state = "ending"
                    pygame.mixer.music.stop()
                
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
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load('assets/music/credits.ogg')
                    pygame.mixer.music.play(-1)  # Loop the music indefinitely
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
                    self.current_scene = self.room_101
                    self.player = self.new_game.player
                    self.player.add_game(self)
                    self.all_sprites.add(self.player)
                    self.all_sprites.add(self.current_scene)
                    #for sprite in self.current_scene.scene_sprites: TODO: do this after done with map sprites
                    #    self.all_sprites.add(sprite)
                    pygame.mixer.music.stop()
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('assets/sounds/door_knock_angry.mp3'))
            else:
                pass

    def load_map(self) -> None:
        """Method that creates the map
        """
        self.room_101 = Room101(self.screen)
        self.floor_1 = Floor1(self.screen, width=self.room_101.rect.topleft[0] + 500, height=self.room_101.rect.topleft[1] - 600)
        self.floor_0 = Floor0(self.screen, width=self.floor_1.rect.topleft[0] + 500, height=self.floor_1.rect.topleft[1] - 750)
        self.underground = Underground(self.screen, width=self.floor_0.rect.topleft[0] - 1950, height=self.floor_0.rect.topleft[1] - 750)
    
    def change_map(self, old_map, new_map) -> None:
        """Method that changes the current map, i.e. removes the old and adds the new map

        Args:
            old_map (Scene): old scene
            new_map (Scene): target scene
        """
        self.all_sprites.remove(old_map)
        #for sprite in old_map.scene_sprites: TODO: do this after done with map sprites
        #    self.all_sprites.remove(sprite)
        
        self.all_sprites.add(new_map)
        #for sprite in new_map.scene_sprites: TODO: do this after done with map sprites
        #    self.all_sprites.add(sprite)

    def draw(self) -> None:
        """Method that renders the game
        """
        self.screen.fill((35, 14, 13))
            
        if self.menu_state == "main":
            self.main_menu.draw()
        elif self.menu_state == "ending":
            self.ending_menu.draw()
        elif self.menu_state == "options":
            self.options_menu.draw()
        elif self.menu_state == "new_game":
            self.new_game.draw()
        elif self.menu_state == "game":
            for sprite in self.all_sprites:
                self.screen.blit(sprite.image, sprite.rect.topleft - self.camera.offset)
                
            self.current_scene.draw()

        elif self.menu_state == "pause":
            self.pause_menu.draw()
        else:
            pass
        
        pygame.display.flip()  # Update the entire screen

    def update(self) -> None:
        """Function that updates the game loop
        """
        if hasattr(self, 'player') and self.menu_state == "game":
            self.all_sprites.update()
            self.camera.box_target_camera(self.player)
            self.camera.keyboard_control()
    
    def run(self) -> None:
        """Method to run through the game loop
        """
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
