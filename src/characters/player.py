"""Player class for the protagonist of the game."""

import pygame
import numpy as np
from settings import WIDTH, HEIGHT

class Player:
    def __init__(self, screen, position=[50, 450]):
        self.screen = screen
        
        # Initial values
        self.position = position
        
        self.eloquence = 0
        self.clairvoyance = 0
        self.forbearance = 0
        self.resonance = 0
        self.experience = 0
        
        self.health = 4
        self.reason = 2
        self.speed = 2
        
        # Load the player's sprite
        self.sprite = pygame.image.load('assets/images/protagonist/protagonist_frame_temp.png')
        self.sprite = pygame.transform.scale(self.sprite, (100, 100))  # Resize the sprite to 100x100 pixels
        
        # Inventory
        self.inventory = []
    
    def get_position(self):
        return self.position
    
    def get_skills(self):
        return {"Eloquence": self.eloquence, "Clairvoyance": self.clairvoyance,
                "Forbearance": self.forbearance, "Resonance": self.resonance}
    
    def get_skills_description(self):
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
        
    def set_skills(self, skills):
        self.eloquence = skills["Eloquence"]
        self.clairvoyance = skills["Clairvoyance"]
        self.forbearance = skills["Forbearance"]
        self.resonance = skills["Resonance"]

    def roll_skill_check(self, skill_name, difficulty_class):
        """Rolls a skill check based on the character's current stats."""
        skill_value = getattr(self, skill_name, 0)  # Get the value of the skill
        roll = np.random.randint(1, 21)
        return roll + skill_value >= difficulty_class  # Simple pass/fail check
    
    def reduce_attribute(self, attribute_name, amount):
        """Reduces the value of an attribute by a specified amount."""
        current_value = getattr(self, attribute_name, 0)
        setattr(self, attribute_name, current_value - amount)
    
    def raise_experience(self, amount):
        """Increases the player's experience by a specified amount."""
        self.experience += amount
        
    def draw(self):
        self.screen.blit(self.sprite, self.position)
        
    # FIXME: Not working properly
    """def handle_movement(self):
        keys = pygame.key.get_pressed()
        # x, y = self.position
        if keys[pygame.K_LEFT]:
            self.position[0] += max(0, self.position[0] - self.speed)
        if keys[pygame.K_RIGHT]:
            self.position[0] += min(WIDTH - self.sprite.get_width(), self.position[0] + self.speed)
        if keys[pygame.K_UP]:
            self.position[1] += max(0, self.position[1] - self.speed)
        if keys[pygame.K_DOWN]:
            self.position[1] = min(HEIGHT - self.sprite.get_height(), self.position[1] + self.speed)
        # self.position = (x, y)"""
