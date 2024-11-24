"""Player class for the protagonist of the game."""

import pygame
import numpy as np

from settings import WIDTH, HEIGHT
from src.ui.animated_sequence import load_png_sequence, sequence_current_frame

class Player:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """Create a new instance of the Player class if one does not already exist, i.e. Singleton pattern.

        Returns:
            _type_: The Player instance.
        """
        if not cls._instance:
            cls._instance = super(Player, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, screen: pygame.Surface, position: list[int] = [50, 450]) -> None:
        """Initialize the Player object.

        Args:
            screen (pygame.Surface): The screen where the player will be drawn.
            position (list[int], optional): Initial position of the player. Defaults to [50, 450].
        """
        if not hasattr(self, "initialized"):  # Prevent re-initialization
            self.screen = screen
            self.font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 20)
            self.stats_bar = load_png_sequence('assets/ui/StatsBar')
            
            # Initial values
            self.position = position
            
            self.eloquence = 0
            self.clairvoyance = 0
            self.forbearance = 0
            self.resonance = 0
            self.experience = 0
            
            self.health = 4
            self.reason = 2
            self.speed = 5
            
            # Load the player's sprite
            self.sprite = pygame.image.load('assets/images/protagonist/protagonist_frame_temp.png')
            self.sprite = pygame.transform.scale(self.sprite, (100, 100))  # Resize the sprite to 100x100 pixels
            
            # PLACEHOLDER: Implement Inventory Object at ui/inventory.py
            self.inventory = []
            
            self.initialized = True  # Mark as initialized
    
    def get_position(self) -> list[int]:
        """Get the current position of the player.

        Returns:
            List[int]: The current position of the player.
        """
        return self.position
    
    def handle_movement(self, keys: pygame.key.ScancodeWrapper) -> None:
        """Handle the movement of the player based on key presses.

        Args:
            keys (pygame.key.ScancodeWrapper): The keys that are currently pressed.
        """
        if keys[pygame.K_UP]:
            self.position[1] -= self.speed
        if keys[pygame.K_DOWN]:
            self.position[1] += self.speed
        if keys[pygame.K_LEFT]:
            self.position[0] -= self.speed
        if keys[pygame.K_RIGHT]:
            self.position[0] += self.speed
        # Ensure the player does not move out of the screen boundaries
        self.position[0] = max(0, min(self.position[0], WIDTH - self.sprite.get_width()))
        self.position[1] = max(0, min(self.position[1], HEIGHT - self.sprite.get_height()))

    
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
        print(f"Rolled a {roll} for {skill_name} check. attr: {skill_value}")
        return roll + skill_value >= difficulty_class  # Simple pass/fail check
    
    def reduce_attribute(self, attribute_name: str, amount: int) -> None:
        """Reduce the value of an attribute by a specified amount.

        Args:
            attribute_name (str): The name of the attribute to reduce.
            amount (int): The amount to reduce the attribute by.
        """
        current_value = getattr(self, attribute_name, 0)
        setattr(self, attribute_name, current_value - amount)
    
    def raise_experience(self, amount: int) -> None:
        """Increase the player's experience by a specified amount.

        Args:
            amount (int): The amount to increase the experience by.
        """
        self.experience += amount
        
    def draw(self) -> None:
        """Draw the player & their stats on the screen."""
        self.screen.blit(self.sprite, self.position)
        self.screen.blit(sequence_current_frame(self.stats_bar), (0, 0))
        self.screen.blit(self.font.render(f"Health: {self.health}", True, (255, 255, 255)), (20, 18))
        self.screen.blit(self.font.render(f"Reason: {self.reason}", True, (255, 255, 255)), (20, 44))
