"""Player class for the protagonist of the game."""

import pygame
import numpy as np
import math

from settings import *

initial_pos = (WIDTH-ROOM_WIDTH)//2 + 120, (WIDTH-ROOM_HEIGHT)//2 + 240

class Player(pygame.sprite.Sprite):
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """Create a new instance of the Player class if one does not already exist, i.e. Singleton pattern.

        Returns:
            _type_: The Player instance.
        """
        if not cls._instance:
            cls._instance = super(Player, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, screen: pygame.Surface, position: tuple[int] = initial_pos) -> None:
        """Initialize the Player object.

        Args:
            screen (pygame.Surface): The screen where the player will be drawn.
            position (list[int], optional): Initial position of the player. Defaults to [50, 450].
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
            self.reason = 2
            self.speed = 5

            self.door_side = "top"
            
            # PLACEHOLDER: Implement Inventory Object at ui/inventory.py
            self.inventory = []
            
            self.initialized = True  # Mark as initialized
    
    def add_game(self, game) -> None:
        """Add the game instance to the player.

        Args:
            game (Game): The game instance.
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
        """Handles the movement of the player based on the keys pressed if not in dialogue.
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
        """Handles character animation based on the direction they are facing and their movement.
        """
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
        
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 0, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 3, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 1, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 2, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
    
    def get_skills(self) -> dict[str, int]:
        """Get the current skills of the player.

        Returns:
            Dict[str, int]: A dictionary of the player's skills.
        """
        return {"Eloquence": self.eloquence, "Clairvoyance": self.clairvoyance,
                "Forbearance": self.forbearance, "Resonance": self.resonance}
    
    def get_skills_description(self) -> dict[str, str]:
        """Get the descriptions of the player's skills.

        Returns:
            Dict[str, str]: A dictionary of the player's skill descriptions.
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

        Args:
            skills (Dict[str, int]): A dictionary of the player's skills.
        """
        self.eloquence = skills["Eloquence"]
        self.clairvoyance = skills["Clairvoyance"]
        self.forbearance = skills["Forbearance"]
        self.resonance = skills["Resonance"]
        self.experience = self.eloquence + self.clairvoyance + self.forbearance + self.resonance

    def roll_skill_check(self, skill_name: str, difficulty_class: int) -> bool:
        """Roll a skill check based on the player's current stats.

        Args:
            skill_name (str): The name of the skill to check.
            difficulty_class (int): The difficulty class to beat.

        Returns:
            bool: True if the skill check is successful, False otherwise.
        """
        skill_value = getattr(self, skill_name.lower(), 0)  # Get the value of the skill
        roll = np.random.randint(1, 21)
        result = roll + skill_value >= difficulty_class
        if result:
            print(f"Success! Rolled a {roll} + {skill_value} for {skill_name} check.")
            self.raise_experience(1) # Gain experience for successful checks
        else:
            print(f"Failure! Rolled a {roll} + {skill_value} for {skill_name} check.")
        return result  # Simple pass/fail check
    
    def raise_experience(self, amount: int) -> None:
        """Increase the player's experience by a specified amount.

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
        """Updates the player's position and animation.
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
            # print("COLIDIU")
            self.rect.y = previous_y 
            self.rect.x = previous_x
        
        # Resetar as mudanças no movimento após cada atualização
        self.x_change = 0
        self.y_change = 0
        
    def check_collision(self, all_sprites: pygame.sprite.LayeredUpdates) -> bool:
        """Check for collisions with the walls of the room.

        Args:
            all_sprites (pygame.sprite.LayeredUpdates): all sprites in scene.

        Returns:
            bool: True if the player collides with a wall, False otherwise.
        """
        for sprite in all_sprites:
            if not isinstance(sprite, Player):  # Verifique colisão com o fundo do quarto
                # Verifique colisões
                offset = (self.rect.x - sprite.rect.x, self.rect.y - sprite.rect.y)
                if sprite.mask.overlap(self.mask, offset):
                    return True  # Colidiu com a parede horizontalmente
        return False
