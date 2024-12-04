"""This module contains the Player class, representing the protagonist of the game.
It manages the player's movement, animation, skills, and interaction with the game world."""

import pygame
import numpy as np
import math

from settings import *
from src.ui.inventory import Inventory

initial_pos = ((WIDTH-ROOM_WIDTH)//2 + 120, (WIDTH-ROOM_HEIGHT)//2 + 240)

class Player(pygame.sprite.Sprite):
    """
    Represents the player character in the game.

    Attributes:
        screen (pygame.Surface): The screen to render the player.
        position (tuple[int]): The player's starting position.
        stats (dict): Player's skills, health, and experience.
        inventory (Inventory): The player's inventory.
    """
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """Ensure only one instance of Player is created (Singleton pattern).

        Args:
            *args: Arguments for the superclass constructor.
            **kwargs: Keyword arguments for the superclass constructor.

        Returns:
            Player: The single Player instance.
        """
        if not cls._instance:
            cls._instance = super(Player, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, screen: pygame.Surface, position: tuple[int] = initial_pos) -> None:
        """Initialize the Player object.

        Args:
            screen (pygame.Surface): The screen where the player will be drawn.
            position (tuple[int], optional): Initial position of the player. Defaults to initial_pos.
        """
        if not hasattr(self, "initialized"):  # Prevent re-initialization
            self.screen = screen
            self.font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 20)
            
            # Initial values
            self.x = position[0]
            self.y = position[1]
            self.width = 48
            self.height = 72
            
            self.x_change = 0
            self.y_change = 0

            self.facing = 'down'
            self.animation_loop = 1
            
            self.current_room = None
            
            # Player Stats
            self.eloquence = 0
            self.clairvoyance = 0
            self.forbearance = 0
            self.resonance = 0
            self.experience = 0
            self.health = 4
            self.reason = 3
            
            self.inventory = Inventory()
            
            self.initialized = True  # Mark as initialized
    
    def add_game(self, game) -> None:
        """
        Associates the player with the game instance.

        Args:
            game (Game): The game instance to associate with.
        """
        self.game = game  # Use the passed game instance
        self._layer = PLAYER_LAYER
        
        # Load the player's sprite
        self.image = self.game.character_spritesheet.get_sprite(1, 0, self.width, self.height)
        self.image_hitbox = pygame.image.load('assets/images/characters/player_hitbox.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image_hitbox)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
            
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
    
    def handle_movement(self) -> None:
        """
        Updates the player's movement based on key inputs (WASD or arrow keys), 
        unless the player is in dialogue mode.
        """
        keys = pygame.key.get_pressed()
        # Only move if the player is not in dialogue
        if not self.game.current_scene.in_dialogue:
            if keys[pygame.K_LEFT]:
                self.x_change -= PLAYER_SPEED
                self.facing = 'left'
            if keys[pygame.K_RIGHT]:
                self.x_change += PLAYER_SPEED
                self.facing = 'right'
            if keys[pygame.K_UP]:
                self.y_change -= PLAYER_SPEED
                self.facing = 'up'
            if keys[pygame.K_DOWN]:
                self.y_change += PLAYER_SPEED
                self.facing = 'down'

    def animate(self) -> None:
        """Updates the player's animation based on their movement and facing direction.
    
        Chooses from pre-defined animation frames (down, up, left, right) based on movement and direction. 
        Loops through frames for walking animations, resets after 3 frames.
        """
        # Define animation frames for each direction (down, up, left, right)
        down_animations = [self.game.character_spritesheet.get_sprite(1, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(2, 0, self.width, self.height)]

        up_animations = [self.game.character_spritesheet.get_sprite(1, 3, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(0, 3, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(2, 3, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(1, 1, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(0, 1, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(2, 1, self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite(1, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(0, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(2, 2, self.width, self.height)]
    
        # Update the character's sprite based on their facing direction and movement
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 0, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1  # Reset animation loop for down movement
        
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 3, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1  # Reset animation loop for up movement
        
        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 1, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1  # Reset animation loop for left movement
        
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 2, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1  # Reset animation loop for right movement
    
    def get_skills(self) -> dict[str, int]:
        """Get the current skills of the player.
        
        This method returns the player's current skill values as a dictionary. The skills include 
        Eloquence, Clairvoyance, Forbearance, and Resonance, each represented as integers.
        
        Returns:
            dict[str, int]: A dictionary containing the player's skill names as keys and their 
            corresponding skill values as integers.
        """
        return {
            "Eloquence": self.eloquence,
            "Clairvoyance": self.clairvoyance,
            "Forbearance": self.forbearance,
            "Resonance": self.resonance
            }
    
    def get_skills_description(self) -> dict[str, str]:
        """Get the descriptions of the player's skills.
        
        This method returns a dictionary containing detailed descriptions for each of the player's skills.
        Each skill's description provides an explanation of its function and role within the game.

        Returns:
            dict[str, str]: A dictionary containing the skill names as keys and their descriptions as values.
        """
        return {
            "Eloquence": "Your speech and persuasion\nskills to influence others.\n"
                 "Eloquence allows you to sway\nopinions, negotiate effectively,\n"
                 "and charm those around you\nwith your words. It is the art of\n"
                 "communication, where every word\nis a tool to achieve your goals.",
            "Clairvoyance": "Insight and intuition\ninto what surrounds you.\n"
                    "Clairvoyance grants you the ability\nto perceive hidden truths,\n"
                    "sense the emotions of others,\nand foresee potential outcomes.\n"
                    "It is a deep connection to the\nunseen, guiding you through\n"
                    "the complexities of the world with\nan almost supernatural awareness.",
            "Forbearance": "Patience and endurance in\nthe face of adversity. "
                   "Forbearance\nis your inner strength,\nallowing you to withstand\n"
                   "hardships, remain calm under\npressure, and persist through\n"
                   "challenges. It is the quiet resilience\nthat keeps you moving forward,\n"
                   "no matter the obstacles in your path.",
            "Resonance": "Your connection to the\nworld and others around you.\n"
                 "Resonance is the harmony you share\nwith the environment and people,\n"
                 "enabling you to empathize deeply,\nform strong bonds, and draw strength\n"
                 "from your surroundings. It is the\nsymphony of life, where every\ninteraction "
                 "and relationship adds to\nthe richness of your experience."
        }
        
    def set_skills(self, skills: dict[str, int]) -> None:
        """
        Set the player's skills.
        
        This method assigns values to the player's skills based on a given dictionary.
        It also updates the player's experience by summing the values of all skills.

        Args:
            skills (Dict[str, int]): A dictionary where the keys are skill names (e.g., "Eloquence", "Clairvoyance")
                                    and the values are the skill levels (integers).
        """
        self.eloquence = skills["Eloquence"]
        self.clairvoyance = skills["Clairvoyance"]
        self.forbearance = skills["Forbearance"]
        self.resonance = skills["Resonance"]
        self.experience = self.eloquence + self.clairvoyance + self.forbearance + self.resonance

    def roll_skill_check(self, skill_name: str, difficulty_class: int) -> bool:
        """
        Roll a skill check based on the player's current stats.

        This method simulates a skill check by rolling a 20-sided die and adding the player's 
        skill value. The result is compared to the specified difficulty class (DC) to determine 
        success or failure.

        Args:
            skill_name (str): The name of the skill to check (e.g., "Eloquence").
            difficulty_class (int): The difficulty class that the player must meet or exceed.

        Returns:
            bool: True if the skill check is successful (roll + skill value >= DC), False otherwise.
        """
        skill_value = getattr(self, skill_name.lower(), 0)  # Get the value of the skill
        roll = np.random.randint(1, 21)
        result = roll + skill_value >= difficulty_class
        """if result:
            print(f"Success! Rolled a {roll} + {skill_value} for {skill_name} check.")
            self.raise_experience(1) # Gain experience for successful checks
        else:
            print(f"Failure! Rolled a {roll} + {skill_value} for {skill_name} check.")"""
        return result  # Simple pass/fail check
    
    def raise_experience(self, amount: int) -> None:
        """
        Increase the player's experience by a specified amount.

        This method increments the player's experience based on the given `amount`.
        It's typically called when the player successfully performs an action or achieves a goal.

        Args:
            amount (int): The amount to increase the experience by.
        """
        self.experience += amount
        
    """def draw(self) -> None:
        # Draw the player & their stats on the screen.
        self.screen.blit(self.image, [self.rect.x, self.rect.y])
        status_bar.draw(self.screen)
        status_bar.animate()
        self.screen.blit(self.font.render(f"Health: {self.health}", True, (255, 255, 255)), (20, 18))
        self.screen.blit(self.font.render(f"Reason: {self.reason}", True, (255, 255, 255)), (20, 44))"""

    def update(self) -> None:
        """
        Updates the player's position and animation. Handles movement, checks for collisions, 
        and reverts position if a collision is detected. Resets movement changes after each update.
        """
        previous_x = self.rect.x
        previous_y = self.rect.y

        # Executar o movimento do jogador
        self.handle_movement()
        self.animate()
        
        # Tentar mover, se possível
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        if self.check_collision(self.game.all_sprites):
            self.rect.y = previous_y 
            self.rect.x = previous_x
        
        # Resetar as mudanças no movimento após cada atualização
        self.x_change = 0
        self.y_change = 0
        
    def check_collision(self, all_sprites: pygame.sprite.LayeredUpdates) -> bool:
        """
        Checks for collisions between the player and other objects in the scene,
        such as walls or obstacles, using masks for precise collision detection.
        
        Args:
            all_sprites (pygame.sprite.LayeredUpdates): A collection of all sprites in the current scene.
        
        Returns:
            bool: True if the player collides with a wall or obstacle, otherwise False.
        """
        for sprite in all_sprites:
            if not isinstance(sprite, Player):  # Verifique colisão com o fundo do quarto
                # Verifique colisões
                offset = (self.rect.x - sprite.rect.x, self.rect.y - sprite.rect.y)
                if sprite.mask.overlap(self.mask, offset):
                    return True  # Colidiu com a parede horizontalmente
        return False
