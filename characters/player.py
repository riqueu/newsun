import pygame

class Player:
    def __init__(self):
        # Initial skill levels or stats
        self.position = (50, 50)
        self.intelligence = 5
        self.charisma = 3
        self.strength = 4
        self.dexterity = 4
        self.wisdom = 3
        self.constitution = 6
        
        # Initial health and mana
        self.health = 100
        self.mana = 50
        
        # Load the player's sprite
        self.sprite = pygame.image.load('assets/images/frames/protagonist_frame.png')
        self.sprite = pygame.transform.scale(self.sprite, (100, 100))  # Resize the sprite to 100x100 pixels
        
        # Movement speed
        self.speed = 2
        
        # Inventory
        self.inventory = []
        
        # Experience and level
        self.experience = 0
        self.level = 1
    
    def get_position(self):
        return self.position

    def roll_skill_check(self, skill_name, difficulty_class):
        """Rolls a skill check based on the character's current stats."""
        import random
        skill_value = getattr(self, skill_name, 0)  # Get the value of the skill
        roll = random.randint(1, 20)
        return roll + skill_value >= difficulty_class  # Simple pass/fail check
    
    def reduce_attribute(self, attribute_name, amount):
        """Reduces the value of an attribute by a specified amount."""
        current_value = getattr(self, attribute_name, 0)
        setattr(self, attribute_name, current_value - amount)
        
    def draw(self, screen):
        screen.blit(self.sprite, self.position)
        
    def handle_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.position = (self.position[0] - self.speed, self.position[1])
        if keys[pygame.K_RIGHT]:
            self.position = (self.position[0] + self.speed, self.position[1])
        if keys[pygame.K_UP]:
            self.position = (self.position[0], self.position[1] - self.speed)
        if keys[pygame.K_DOWN]:
            self.position = (self.position[0], self.position[1] + self.speed)


# Example of using the protagonist in a scene
# protagonist = Player()
# if protagonist.roll_skill_check('intelligence', 12):
#     print("Skill check passed!")
# else:
#     print("Skill check failed!")
