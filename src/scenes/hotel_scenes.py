"""Module with main game scenes, i.e. Hotel scenes."""

import pygame

from src.ui.interaction import load_scene_interactions
from src.ui.animated_sequence import status_bar
from src.characters.player import Player
from src.characters.npc import NPC, Object
from main import Game
from settings import *

class Scene(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, background_path: str, scripts_path: str, width: int, height: int) -> None:
        """Initializes the scene

        Args:
            screen (pygame.Surface): screen
            background_path (str): path to bg
            scripts_path (str): path to scene scripts
            width (int): scene width
            height (int): scene height
        """
        self.screen = screen
        self.dialogue_managers = load_scene_interactions(scripts_path, self.screen)
        self.in_dialogue = False
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
        
        self.inventory_hotbar = pygame.image.load("assets/ui/hotbar.png").convert_alpha()
        self.scaled_hotbar = pygame.transform.scale(self.inventory_hotbar, (3*self.inventory_hotbar.get_width() // 4, 3*self.inventory_hotbar.get_height() // 4))
        
        collision_path = background_path.replace("full.png", "collision.png")
        self.image_collision = pygame.image.load(collision_path).convert_alpha()
        self.image_collision.set_colorkey(BLUE)

        self.mask = pygame.mask.from_surface(self.image_collision)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.scene_mapping = {
            "GoToRoom": 'room_101',
            "GoToCorridor": 'floor_1',
            "Upstairs": 'floor_1',
            "Downstairs": 'floor_0',
            "EnterElevator": 'underground'
        }
        
        self.people = []
        self.objects = []
        self.scene_sprites = []
        
        self.npc_positionns = {
            "npc_tabastan": [(1940, 680), (10,0)],
            "npc_camellia": [(2100, 600), (16,0)],
            "npc_vorakh": [(1680, 700), (4,0)],
            "npc_efrim": [(1370, 770), (13,0)],
            "npc_ersilia": [(1200, 900), (22,0)],
            "npc_matilda": [(1633, 750), (1,0)]
        }
        
        
        # Create people and objects
        for name in self.dialogue_managers:
            if name.startswith("npc_"):
                if name == "npc_matilda":
                    sprite = self.game.matilda_spritesheet.get_sprite(self.npc_positionns[name][1][0], self.npc_positionns[name][1][1], 48, 72)
                    npc_object = NPC(self.npc_positionns[name][0], name, sprite, matilda=True)
                else:
                    sprite = self.game.character_spritesheet.get_sprite(self.npc_positionns[name][1][0], self.npc_positionns[name][1][1], 48, 72)
                    npc_object = NPC(self.npc_positionns[name][0], name, sprite)
                self.people.append(npc_object)
            elif name in self.objects_positions:
                if len(self.objects_positions[name]) > 1:
                    object_object = Object(self.objects_positions[name][0], name, self.objects_positions[name][1])
                else:
                    object_object = Object(self.objects_positions[name][0], name)
                self.objects.append(object_object)
        
        self.scene_sprites = self.people + self.objects
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Function that handles events in the scene

        Args:
            event (pygame.event.Event): the event
        """
        # Check for interaction with objects/npcs
        for sprite in self.scene_sprites:
            in_range = sprite.player_in_interaction_range(self.player.rect)
            if in_range:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                    self.dialogue_managers[sprite.name].dialogue_active = True
                    break
        
        self.in_dialogue = any(manager.dialogue_active for manager in self.dialogue_managers.values())
        for name, manager in self.dialogue_managers.items():
            if manager.dialogue_active:
                condition = self.dialogue_conditions.get(name, None)
                if condition is not None:
                    manager.handle_event(event, condition)
                else:
                    manager.handle_event(event)
                if 'condition' in manager.current_node:
                    self.change_conditions(name, manager.current_node['condition'])
        
    
    def change_of_scene(self, scene: str) -> None|str:
        """Function that returns change of scenes

        Args:
            scene (str): the scene string (stairs or door)

        Returns:
            None|str: if the scene is changed
        """
        node_title = self.dialogue_managers[scene].current_node['title'] 
        if node_title in self.scene_mapping:
            self.dialogue_managers[scene].dialogue_active = False
            self.dialogue_managers[scene].dialogue_ended = True
            self.dialogue_managers[scene].current_node = self.dialogue_managers[scene].find_node("Start") # To reset dialogue
            return self.scene_mapping[node_title]
        
    def change_conditions(self, condition_name: str, value: int) -> None:
        """Function to change dialogue conditions

        Args:
            condition_name (str): the name of the condition to change
            value (int): the new value of the condition
        """
        if condition_name in self.dialogue_conditions:
            self.dialogue_conditions[condition_name] = value

    def draw(self) -> None:
        """Function that draws the UI elements in the scene
        """
        status_bar.draw(self.screen)
        status_bar.animate()
        self.screen.blit(self.font.render(f"Health: {self.player.health}", True, (255, 255, 255)), (20, 18))
        self.screen.blit(self.font.render(f"Reason: {self.player.reason}", True, (255, 255, 255)), (20, 44))
        
        self.screen.blit(self.scaled_hotbar, (20, HEIGHT - 80))
        self.player.inventory.draw(self.screen)
        
        for manager in self.dialogue_managers.values():
            if manager.dialogue_active or manager.dialogue_ended: # dialogue_ended only to draw out animation
                manager.draw()


class Room101(Scene):
    def __init__(self, screen: pygame.Surface, background_path: str = "assets/images/backgrounds/room_full.png", scripts_path: str = "scripts/room_101", width: int = ROOM_WIDTH, height: int = ROOM_HEIGHT - 400) -> None:
        """Function that initializes the room 101 scene"""
        self.dialogue_conditions = {
            "bed": 1,
            "mirror": 1,
            "tv": 1,
        }
        self.objects_positions = {
            "bed": [(890, 480)],
            "clock": [(508, 450)],
            "door": [(870, 670)],
            "mirror": [(274, 450)],
            "poster": [(780, 450)],
            "sink": [(348, 450)],
            "toilet": [(195, 555)],
            "tv": [(652, 451)]
        }
        super().__init__(screen, background_path, scripts_path, width, height)
        
    def handle_event(self, event: pygame.event.Event) -> None|str:
        """Function that handles events in the room 101 scene

        Args:
            event (pygame.event.Event): current event
        """
        super().handle_event(event)

        # Check if it's a change of scene dialogue (door)
        if 'door' in self.dialogue_managers and self.dialogue_managers['door'].dialogue_active:
            return self.change_of_scene('door')

    def draw(self) -> None:
        """Function that draws the room
        """
        super().draw()
        

class Floor1(Scene):
    def __init__(self, screen: pygame.Surface, background_path: str = "assets/images/backgrounds/hall_full.png", scripts_path: str = "scripts/floor_1", width: int = 0, height: int = 0) -> None:
        """Function that initializes the room 101 scene"""
        self.dialogue_conditions = {
            "npc_tabastan": 1,
            "npc_camellia": 1,
            "bookshelf": 1,
            "stairs_up": 1,
        }
        self.objects_positions = {
            "door": [(870, 600)],
            "elevator": [(1965, 600)],
            "stairs_up": [(2170, 600), (100, 50)],
            "stairs": [(1750, 600), (110, 50)],
            "bookshelf": [(1240, 600), (84, 60)],
        }
        super().__init__(screen, background_path, scripts_path, width, height)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Function that handles events in the floor 1 scene

        Args:
            event (pygame.event.Event): current event
        """
        super().handle_event(event)
        
        # Check if it's a change of scene dialogue (door or stairs)
        if 'door' in self.dialogue_managers and self.dialogue_managers['door'].dialogue_active:
            return self.change_of_scene('door')
        
        elif 'stairs' in self.dialogue_managers and self.dialogue_managers['stairs'].dialogue_active:
            return self.change_of_scene('stairs')

    def draw(self) -> None:
        """Function that draws the room
        """
        super().draw()


class Floor0(Scene):
    def __init__(self, screen: pygame.Surface, background_path: str = "assets/images/backgrounds/lobby_full.png", scripts_path: str = "scripts/floor_0", width: int = 0, height: int = 0) -> None:
        """Function that initializes the hall scene"""
        self.objects_positions = {
            "door": [(1620, 600), (70, 50)],
            "stairs": [(1800, 600), (100, 50)],
            "sofa": [(1595, 900), (290, 60)],
        }
        super().__init__(screen, background_path, scripts_path, width, height)
        self.dialogue_conditions = {
            "npc_vorakh": 1,
            "npc_efrim": 1,
            "npc_ersilia": 1,
            "sofa": 1,
            "door": 1
        }

    def handle_event(self, event: pygame.event.Event) -> None:
        """Function that handles events in the floor 0 scene

        Args:
            event (pygame.event.Event): current event
        """
        super().handle_event(event)
        
        # Check if it's a change of scene dialogue (door or stairs)
        if 'door' in self.dialogue_managers and self.dialogue_managers['door'].dialogue_active:
            return self.change_of_scene('door')
        
        elif 'stairs' in self.dialogue_managers and self.dialogue_managers['stairs'].dialogue_active:
            return self.change_of_scene('stairs')

    def draw(self) -> None:
        """Function that draws the room
        """
        super().draw()


class Underground(Scene):
    def __init__(self, screen: pygame.Surface, background_path: str = "assets/images/backgrounds/underground_full.png", scripts_path: str = "scripts/underground", width: int = 0, height: int = 0) -> None:
        """Function that initializes the underground scene"""
        self.dialogue_conditions = {}
        self.objects_positions = {}
        super().__init__(screen, background_path, scripts_path, width, height)

    def handle_event(self, event: pygame.event.Event) -> None|str:
        """Function that handles events in the underground scene

        Args:
            event (pygame.event.Event): current event
        """
        super().handle_event(event)
        
        if self.dialogue_managers['npc_matilda'].current_node['title'] == "NEWSUN":
            return "ending"

    def draw(self) -> None:
        """Function that draws the room
        """
        super().draw()
