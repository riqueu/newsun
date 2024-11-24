"""Module with main game scenes, i.e. Hotel scenes."""

import pygame

from src.ui.interaction import load_scene_interactions
from src.characters.player import Player

class Scene:
    def __init__(self, screen: pygame.Surface, background_path: str, scripts_path: str) -> None:
        """Function that initializes the scene

        Args:
            screen (pygame.Surface): the screen
            background_path (str): path to the background image
            scripts_path (str): path to the scripts (interactions)
        """
        self.screen = screen
        self.background = pygame.image.load(background_path)
        self.dialogue_managers = load_scene_interactions(scripts_path, self.screen)
        self.in_dialogue = False
        self.objects = []
        self.player = Player(screen) # Singleton pattern to draw the player in the right order
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Function that handles events in the scene

        Args:
            event (pygame.event.Event): the event
        """
        for manager in self.dialogue_managers.values():
            if manager.dialogue_active:
                manager.handle_event(event)
    
    def draw(self) -> None:
        """Function that draws the scene
        """
        self.screen.blit(self.background, (0, 0))
        
        for obj in self.objects:
            pygame.draw.rect(self.screen, (255, 0, 0), obj["rect"], 2)
        
        self.player.draw()
        
        for manager in self.dialogue_managers.values():
            if manager.dialogue_active or manager.dialogue_ended: # dialogue_ended only to draw out animation
                manager.draw()


class Room101(Scene):
    def __init__(self, screen: pygame.Surface, background_path: str = "assets/images/backgrounds/fundo_temp.png", scripts_path: str = "scripts/room_101") -> None:
        """Function that initializes the room 101 scene

        Args:
            screen (pygame.Surface): the screen
            background_path (str, optional): bg. Defaults to "assets/images/backgrounds/temp_bg.jpg".
            scripts_path (str, optional): scripts. Defaults to "scripts/room_101".
        """
        super().__init__(screen, background_path, scripts_path)
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
    def __init__(self, screen: pygame.Surface, background_path: str = "assets/images/backgrounds/fundo_temp.png", scripts_path: str = "scripts/floor_1") -> None:
        """Function that initializes the floor 1 scene

        Args:
            screen (pygame.Surface): the screen
            background_path (str, optional): bg. Defaults to "assets/images/backgrounds/temp_bg.jpg".
            scripts_path (str, optional): scripts. Defaults to "scripts/floor_1".
        """
        super().__init__(screen, background_path, scripts_path)

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
    def __init__(self, screen: pygame.Surface, background_path: str = "assets/images/backgrounds/fundo_temp.png", scripts_path: str = "scripts/floor_0") -> None:
        """Function that initializes the floor 0 scene

        Args:
            screen (pygame.Surface): the screen
            background_path (str, optional): bg. Defaults to "assets/images/backgrounds/temp_bg.jpg".
            scripts_path (str, optional): scripts. Defaults to "scripts/floor_0".
        """
        super().__init__(screen, background_path, scripts_path)

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
    def __init__(self, screen: pygame.Surface, background_path: str = "assets/images/backgrounds/fundo_temp.png", scripts_path: str = "scripts/underground") -> None:
        """Function that initializes the underground scene

        Args:
            screen (pygame.Surface): the screen
            background_path (str, optional): bg. Defaults to "assets/images/backgrounds/temp_bg.jpg".
            scripts_path (str, optional): scripts. Defaults to "scripts/underground".
        """
        super().__init__(screen, background_path, scripts_path)

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
