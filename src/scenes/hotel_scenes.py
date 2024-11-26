"""Module with main game scenes, i.e. Hotel scenes."""

import pygame

from src.ui.interaction import load_scene_interactions
from src.ui.animated_sequence import status_bar
from src.characters.player import Player
from main import Game
from settings import *

class Scene(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, background_path: str, scripts_path: str, width: int, height: int) -> None:
        self.screen = screen
        # self.background = pygame.image.load(background_path)
        self.dialogue_managers = load_scene_interactions(scripts_path, self.screen)
        self.in_dialogue = False
        self.objects = []
        self.player = Player(screen) # Singleton pattern to draw the player in the right order
        self.game = Game() # Singleton pattern to access the game instance
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 20)
        
        self.width = width
        self.height = height
        self.x = (WIDTH-self.width)//2
        self.y = (HEIGHT-self.height)//2

        self.image = pygame.image.load(background_path).convert_alpha()
        self.image.set_colorkey(BLUE)

        collision_path = background_path.replace("full.png", "collision.png")
        self.image_collision = pygame.image.load(collision_path).convert_alpha()
        self.image_collision.set_colorkey(BLUE)

        self.mask = pygame.mask.from_surface(self.image_collision)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Function that handles events in the scene

        Args:
            event (pygame.event.Event): the event
        """
        for manager in self.dialogue_managers.values():
            if manager.dialogue_active:
                manager.handle_event(event)
    
    def draw(self) -> None:
        """Function that draws the UI elements in the scene
        """
        #self.screen.blit(self.image, (0, 0))
        
        #for obj in self.objects:
        #    pygame.draw.rect(self.screen, (255, 0, 0), obj["rect"], 2)
        
        #self.player.draw()
        
        status_bar.draw(self.screen)
        status_bar.animate()
        self.screen.blit(self.font.render(f"Health: {self.player.health}", True, (255, 255, 255)), (20, 18))
        self.screen.blit(self.font.render(f"Reason: {self.player.reason}", True, (255, 255, 255)), (20, 44))
        
        for manager in self.dialogue_managers.values():
            if manager.dialogue_active or manager.dialogue_ended: # dialogue_ended only to draw out animation
                manager.draw()


class Room101(Scene):
    def __init__(self, screen: pygame.Surface, background_path: str = "assets/images/backgrounds/room_full.png", scripts_path: str = "scripts/room_101", width: int = ROOM_WIDHT, height: int = ROOM_HEIGHT) -> None:
        """Function that initializes the room 101 scene"""
        super().__init__(screen, background_path, scripts_path, width, height)
        self.objects = [
            {"name": "sink", "rect": pygame.Rect(100, 100, 50, 50)},
            {"name": "mirror", "rect": pygame.Rect(200, 100, 50, 50)},
            {"name": "clock", "rect": pygame.Rect(900, 400, 50, 50)},
            {"name": "door", "rect": pygame.Rect(900, 500, 50, 50)}
        ]

    def handle_event(self, event: pygame.event.Event) -> None:
        """Function that handles events in the room 101 scene

        Args:
            event (pygame.event.Event): current event
        """
        super().handle_event(event)
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.dialogue_managers['mirror'].dialogue_active = True     

    def draw(self) -> None:
        """Function that draws the room
        """
        super().draw()
        

class Floor1(Scene):
    def __init__(self, screen: pygame.Surface, background_path: str = "assets/images/backgrounds/hall_full.png", scripts_path: str = "scripts/floor_1", width: int = ROOM_WIDHT, height: int = ROOM_HEIGHT) -> None:
        """Function that initializes the room 101 scene"""
        super().__init__(screen, background_path, scripts_path, width, height)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Function that handles events in the floor 1 scene

        Args:
            event (pygame.event.Event): current event
        """
        super().handle_event(event)

    def draw(self) -> None:
        """Function that draws the room
        """
        super().draw()


class Floor0(Scene):
    def __init__(self, screen: pygame.Surface, background_path: str = "assets/images/backgrounds/lobby_full.png", scripts_path: str = "scripts/floor_0", width: int = ROOM_WIDHT, height: int = ROOM_HEIGHT) -> None:
        """Function that initializes the hall scene"""
        super().__init__(screen, background_path, scripts_path, width, height)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Function that handles events in the floor 0 scene

        Args:
            event (pygame.event.Event): current event
        """
        super().handle_event(event)

    def draw(self) -> None:
        """Function that draws the room
        """
        super().draw()


class Underground(Scene):
    def __init__(self, screen: pygame.Surface, background_path: str = "assets/images/backgrounds/underground_full.png", scripts_path: str = "scripts/underground", width: int = ROOM_WIDHT, height: int = ROOM_HEIGHT) -> None:
        """Function that initializes the underground scene"""
        super().__init__(screen, background_path, scripts_path, width, height)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Function that handles events in the underground scene

        Args:
            event (pygame.event.Event): current event
        """
        super().handle_event(event)

    def draw(self) -> None:
        """Function that draws the room
        """
        super().draw()
