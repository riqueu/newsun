"""
Module containing the main game scenes in the hotel setting, such as rooms, floors, and the underground.

This module defines several scene classes (`Scene`, `Room101`, `Floor1`, `Floor0`, `Underground`) that represent different environments the player can interact with. Each scene is responsible for handling its own interactions, drawing itself, and managing dialogue or transitions between scenes.

Classes:
- `Scene`: Base class for a hotel scene, handling common functionality like event handling, dialogue management, and drawing.
- `Room101`: Represents the first room in the hotel, where the player starts.
- `Floor1`: Represents the first floor of the hotel, where the player can explore.
- `Floor0`: Represents the lobby or ground floor of the hotel.
- `Underground`: Represents the underground area, typically used for the final scenes or transitions.
"""


import pygame

from src.ui.interaction import load_scene_interactions
from src.ui.animated_sequence import status_bar
from src.characters.player import Player
from src.characters.npc import NPC, Object
from main import Game
from settings import *

class Scene(pygame.sprite.Sprite):
    """
    Base class for a hotel scene in the game. Responsible for managing background images, 
    interactions, NPCs, objects, and scene transitions.
    """
    def __init__(self, screen: pygame.Surface, background_path: str, scripts_path: str, width: int, height: int) -> None:
        """
        Initializes the Scene object with the given parameters and prepares all necessary assets 
        such as the background image, collision mask, dialogue managers, and NPCs.

        Args:
            screen (pygame.Surface): The surface (screen) where the scene will be rendered.
            background_path (str): The path to the background image for the scene.
            scripts_path (str): The path to the scripts that define the dialogues and interactions for the scene.
            width (int): The width of the scene in pixels.
            height (int): The height of the scene in pixels.
        """
        # Initialize the screen, and load the dialogue managers from the scripts
        self.screen = screen
        self.dialogue_managers = load_scene_interactions(scripts_path, self.screen)
        self.in_dialogue = False
        self.player = Player(screen) # Singleton pattern to draw the player in the right order
        self.game = Game() # Singleton pattern to access the game instance
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 20)
        
        # Center the scene on the screen
        self.width = width
        self.height = height
        self.x = (WIDTH-self.width)//2
        self.y = (HEIGHT-self.height)//2
        
        # Load and set up the background image
        self.image = pygame.image.load(background_path).convert_alpha()
        self.image.set_colorkey(BLUE)
        
        # Load and set up the background image
        self.inventory_hotbar = pygame.image.load("assets/ui/hotbar.png").convert_alpha()
        self.scaled_hotbar = pygame.transform.scale(self.inventory_hotbar, (3*self.inventory_hotbar.get_width() // 4, 3*self.inventory_hotbar.get_height() // 4))
        
        # Prepare collision image and mask (used for collision detection)
        collision_path = background_path.replace("full.png", "collision.png")
        self.image_collision = pygame.image.load(collision_path).convert_alpha()
        self.image_collision.set_colorkey(BLUE)
        self.mask = pygame.mask.from_surface(self.image_collision)
        
        # Set the position of the scene on the screen
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
        if not hasattr(self, 'objects_positions'):
            self.objects_positions = {}
        
        self.npc_positionns = {
            "npc_tabastan": [(1940, 680), (10,0)],
            "npc_camellia": [(2100, 600), (16,0)],
            "npc_vorakh": [(1680, 700), (4,0)],
            "npc_efrim": [(1370, 770), (13,0)],
            "npc_ersilia": [(1200, 900), (22,0)],
            "npc_matilda": [(1633, 750), (1,0)]
        }
        
        
        # Create NPCs and objects from the dialogue manager (this is how characters and interactive objects are created)
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
        # Combine NPCs and objects into a single list of scene sprites
        self.scene_sprites = self.people + self.objects
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handles user input events such as key presses to interact with NPCs or objects in the scene. 
        It checks if the player is within interaction range of any NPC or object and triggers the 
        corresponding dialogue or action.

        Args:
            event (pygame.event.Event): The event that needs to be handled, typically a key press or mouse interaction.
        """
        # Check for interaction with objects/npcs
        for sprite in self.scene_sprites:
            in_range = sprite.player_in_interaction_range(self.player.rect)
            if in_range:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                    self.dialogue_managers[sprite.name].dialogue_active = True
                    break
        
        self.in_dialogue = any(manager.dialogue_active for manager in self.dialogue_managers.values())
        # Process the event for all dialogue managers that are currently active
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
        """
        Handles the transition to a new scene based on the current dialogue state.
        It checks the dialogue node's title and maps it to a corresponding scene.

        Args:
            scene (str): The name of the scene or action that triggers a scene change.
        
        Returns:
            None | str: The name of the next scene if the scene changes, otherwise None.
        """
        # Get the title of the current dialogue node
        node_title = self.dialogue_managers[scene].current_node['title'] 
        if node_title in self.scene_mapping:
            self.dialogue_managers[scene].dialogue_active = False
            self.dialogue_managers[scene].dialogue_ended = True
            self.dialogue_managers[scene].current_node = self.dialogue_managers[scene].find_node("Start") # To reset dialogue
            return self.scene_mapping[node_title]
        
    def change_conditions(self, condition_name: str, value: int) -> None:
        """
        Changes the value of a specific dialogue condition.

        Args:
            condition_name (str): The name of the condition to change.
            value (int): The new value to assign to the condition.
        """
        if condition_name in self.dialogue_conditions:
            # Update the condition value
            self.dialogue_conditions[condition_name] = value

    def draw(self) -> None:
        """
        Draws the UI elements and game objects for the current scene. 
        This method is responsible for rendering the background, dialogue, 
        player health, reason stats, and the player's inventory UI.

        It also draws the status bar and updates the player’s information, 
        and triggers any necessary dialogue rendering.
        """
        status_bar.draw(self.screen)
        status_bar.animate()
        # Display the player's health and reason
        self.screen.blit(self.font.render(f"Health: {self.player.health}", True, (255, 255, 255)), (20, 18))
        self.screen.blit(self.font.render(f"Reason: {self.player.reason}", True, (255, 255, 255)), (20, 44))
        
        self.screen.blit(self.scaled_hotbar, (20, HEIGHT - 80))
        self.player.inventory.draw(self.screen)
        
        # Draw active dialogue elements
        for manager in self.dialogue_managers.values():
            if manager.dialogue_active or manager.dialogue_ended: # dialogue_ended only to draw out animation
                manager.draw()


class Room101(Scene):
    """
    Represents the Room 101 scene in the game. This is a specific scene where the player 
    interacts with various objects, such as the bed, clock, mirror, and TV. The scene also
    features dialogue interactions with NPCs.
    """
    def __init__(self, screen: pygame.Surface, background_path: str = "assets/images/backgrounds/room_full.png", scripts_path: str = "scripts/room_101", width: int = ROOM_WIDTH, height: int = ROOM_HEIGHT - 400) -> None:
        """
        Initializes the Room 101 scene. This constructor sets up the scene with specific objects,
        dialogue conditions, and NPCs. It loads the background and other visual elements unique
        to Room 101.

        Args:
            screen (pygame.Surface): The display surface for the scene.
            background_path (str, optional): Path to the background image of the room.
            scripts_path (str, optional): Path to the dialogue scripts for the room.
            width (int, optional): The width of the scene. Defaults to `ROOM_WIDTH`.
            height (int, optional): The height of the scene. Defaults to `ROOM_HEIGHT - 400`.
        """
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
        """
        Handles events in the Room 101 scene. It checks for player interaction with objects or NPCs
        and triggers corresponding dialogue. It also checks for a change of scene if the player interacts
        with certain objects

        Args:
            event (pygame.event.Event): The event generated by user input or other actions.
        
        Returns:
            None | str: Returns the new scene name if a change of scene occurs, otherwise None.
        """
        super().handle_event(event)

        # Check if it's a change of scene dialogue (door)
        if 'door' in self.dialogue_managers and self.dialogue_managers['door'].dialogue_active:
            return self.change_of_scene('door')

    def draw(self) -> None:
        """
        Draws the Room 101 scene elements on the screen. This method is responsible for rendering 
        all the interactive objects, NPCs, and UI elements specific to this scene.
        """
        super().draw()
        

class Floor1(Scene):
    """
    Represents the Floor 1 scene in the game. This scene allows the player to interact with various 
    objects and NPCs. The scene includes objects such as the elevator, stairs, and bookshelf, and features 
    dialogues with NPCs like Tabastan and Camellia.

    The class is a subclass of the `Scene` class and includes specific logic for handling events and interactions
    unique to Floor 1.
    """
    def __init__(self, screen: pygame.Surface, background_path: str = "assets/images/backgrounds/hall_full.png", scripts_path: str = "scripts/floor_1", width: int = 0, height: int = 0) -> None:
        """
        Initializes the Floor 1 scene, setting up the objects, dialogue conditions, and NPCs.
        This constructor loads the background and other visual elements unique to Floor 1.

        Args:
            screen (pygame.Surface): The display surface for the scene.
            background_path (str, optional): Path to the background image of the floor.
            scripts_path (str, optional): Path to the dialogue scripts for the floor.
            width (int, optional): The width of the scene. Defaults to `ROOM_WIDTH`.
            height (int, optional): The height of the scene. Defaults to `ROOM_HEIGHT`.
        """
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
        """
        Handles events in the Floor 1 scene. It checks for player interaction with objects or NPCs
        and triggers corresponding dialogue. It also checks for a change of scene if the player interacts
        with certain objects

        Args:
            event (pygame.event.Event): The event generated by user input or other actions.
        
        Returns:
            None | str: Returns the new scene name if a change of scene occurs, otherwise None.
        """
        super().handle_event(event)
        
        # Check if it's a change of scene dialogue (door or stairs)
        if 'door' in self.dialogue_managers and self.dialogue_managers['door'].dialogue_active:
            return self.change_of_scene('door')
        
        elif 'stairs' in self.dialogue_managers and self.dialogue_managers['stairs'].dialogue_active:
            return self.change_of_scene('stairs')

    def draw(self) -> None:
        """
        Draws the Floor 1 scene elements on the screen. This method is responsible for rendering 
        all the interactive objects, NPCs, and UI elements specific to this floor.
        """
        super().draw()


class Floor0(Scene):
    """
    Represents the Floor 0 scene in the game, which is the lobby or ground floor. This scene includes 
    interactions with NPCs, as well as objects like doors, stairs, and sofas. Players can interact with 
    these objects and NPCs, and the scene provides options for transitioning to other areas, such as 
    the stairs or the door.
    """
    
    def __init__(self, screen: pygame.Surface, background_path: str = "assets/images/backgrounds/lobby_full.png", scripts_path: str = "scripts/floor_0", width: int = 0, height: int = 0) -> None:
        """
        Initializes the Floor 0 scene, setting up the objects, dialogue conditions, and NPCs.
        This constructor loads the background and other visual elements unique to Floor 0.

        Args:
            screen (pygame.Surface): The display surface for the scene.
            background_path (str, optional): Path to the background image of the floor.
            scripts_path (str, optional): Path to the dialogue scripts for the floor.
            width (int, optional): The width of the scene. Defaults to `ROOM_WIDTH`.
            height (int, optional): The height of the scene. Defaults to `ROOM_HEIGHT`.
        """
        self.objects_positions = {
            "door": [(1620, 600), (70, 50)],
            "stairs": [(1800, 600), (100, 50)],
            "sofa": [(1595, 900), (290, 60)],
        }
        self.dialogue_conditions = {
            "npc_vorakh": 1,
            "npc_efrim": 1,
            "npc_ersilia": 1,
            "sofa": 1,
            "door": 1
        }
        super().__init__(screen, background_path, scripts_path, width, height)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handles events in the Floor 0 scene. It checks for player interaction with objects or NPCs
        and triggers corresponding dialogue. It also checks for a change of scene if the player interacts
        with certain objects (e.g., door or stairs).

        Args:
            event (pygame.event.Event): The event generated by user input or other actions.
        
        Returns:
            None | str: Returns the new scene name if a change of scene occurs, otherwise None.
        """
        super().handle_event(event)
        
        # Check if it's a change of scene dialogue (door or stairs)
        if 'door' in self.dialogue_managers and self.dialogue_managers['door'].dialogue_active:
            return self.change_of_scene('door')
        
        elif 'stairs' in self.dialogue_managers and self.dialogue_managers['stairs'].dialogue_active:
            return self.change_of_scene('stairs')

    def draw(self) -> None:
        """
        Draws the Floor 0 scene elements on the screen. This method is responsible for rendering 
        all the interactive objects, NPCs, and UI elements specific to this floor.
        """
        super().draw()


class Underground(Scene):
    """
    Represents the Underground scene in the game. This scene takes place in the underground area
    and serves as a transition point to the game's ending. It handles interactions with NPCs and 
    objects specific to this area.
    """
    
    def __init__(self, screen: pygame.Surface, background_path: str = "assets/images/backgrounds/underground_full.png", scripts_path: str = "scripts/underground", width: int = 0, height: int = 0) -> None:
        """
        Initializes the Underground scene, loading specific objects, dialogue conditions, and NPCs.
        This constructor sets up the background and other visual elements for the Underground area.

        Args:
            screen (pygame.Surface): The display surface for the scene.
            background_path (str, optional): Path to the background image of the underground area.
            scripts_path (str, optional): Path to the dialogue scripts for the Underground area.
            width (int, optional): The width of the scene. Defaults to `ROOM_WIDTH`.
            height (int, optional): The height of the scene. Defaults to `ROOM_HEIGHT`.
        """
        self.dialogue_conditions = {}
        self.objects_positions = {}
        super().__init__(screen, background_path, scripts_path, width, height)

    def handle_event(self, event: pygame.event.Event) -> None|str:
        """
        Handles events in the Underground scene. This method is responsible for managing player interaction
        with NPCs or objects in the Underground, and for triggering a scene change to the ending when required.

        Args:
            event (pygame.event.Event): The event generated by user input or other actions.
        
        Returns:
            None | str: Returns the string `"ending"` if the scene transition to the ending occurs.
        """
        super().handle_event(event)
        
        if self.dialogue_managers['npc_matilda'].current_node['title'] == "NEWSUN":
            return "ending"

    def draw(self) -> None:
        """
        Draws the Underground scene on the screen. This method is responsible for rendering the elements
        specific to the Underground area, including the background and any UI components.
        """
        super().draw()
