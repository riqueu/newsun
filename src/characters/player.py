"""Player class for the protagonist of the game."""

import pygame
import numpy as np
from settings import WIDTH, HEIGHT

class Player:
    def __init__(self):
        # Initial skill levels or stats
        self.position = (50, 50)
        
        self.eloquence = 0
        self.clairvoyance = 0
        self.forbearance = 0
        self.resonance = 0
        
        # Initial health and mana
        self.health = 4
        self.reason = 2
        
        # Load the player's sprite
        self.sprite = pygame.image.load('assets/images/protagonist/protagonist_frame_temp.png')
        self.sprite = pygame.transform.scale(self.sprite, (100, 100))  # Resize the sprite to 100x100 pixels
        
        # Movement speed
        self.speed = 2
        
        # Inventory
        self.inventory = []
    
    def get_position(self):
        return self.position
    
    def get_skills(self):
        return {"Eloquence": self.eloquence, "Clairvoyance": self.clairvoyance,
                "Forbearance": self.forbearance, "Resonance": self.resonance}
    
    def get_skills_description(self):
        return {"Eloquence": "Speech and persuasion skills \nto influence others.",
                "Clairvoyance": "Insight and intuition \ninto what surrounds you.",
                "Forbearance": "Patience and endurance \nin the face of adversity.",
                "Resonance": "Your connection to the world \nand others around you."}
        
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
        
    def draw(self, screen):
        screen.blit(self.sprite, self.position)
        
    def handle_movement(self):
        keys = pygame.key.get_pressed()
        x, y = self.position
        if keys[pygame.K_LEFT]:
            x = max(0, x - self.speed)
        if keys[pygame.K_RIGHT]:
            x = min(WIDTH - self.sprite.get_width(), x + self.speed)
        if keys[pygame.K_UP]:
            y = max(0, y - self.speed)
        if keys[pygame.K_DOWN]:
            y = min(HEIGHT - self.sprite.get_height(), y + self.speed)
        self.position = (x, y)


# Example of using the protagonist in a scene
# protagonist = Player()
# if protagonist.roll_skill_check('eloquence', 12):
#     print("Skill check passed!")
# else:
#     print("Skill check failed!")
