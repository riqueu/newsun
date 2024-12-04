"""
Unit tests for the `Player` class.

This module tests the functionality of the `Player` class, including skills, skill checks, experience, and the singleton pattern.

Tests:
    - Singleton pattern for `Player` instance.
    - Retrieval and setting of player skills.
    - Skill check functionality using random values.
    - Experience point increment.
    - Colision with other sprites and with itself.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import Mock, patch
import pygame
from src.characters.player import Player

class TestPlayer(unittest.TestCase):
    """
    Unit tests for the `Player` class.

    This test class validates the functionality of the `Player` class, including methods for skill management, experience handling, and skill checks.
    It also ensures that the `Player` follows the singleton design pattern.
    """
    @patch('pygame.image.load')
    @patch('pygame.font.Font')
    def setUp(self, mock_font, mock_image_load):
        """Sets up the necessary mocks and initializes the Player instance for testing.

        Mocks the `pygame.image.load` and `pygame.font.Font` functions to avoid actual file loading.
        Initializes the screen surface for the `Player` class and creates a `Player` instance.
        """
        pygame.display.set_mode((800, 600))  # Initialize the display
        self.screen = pygame.Surface((800, 600))
        self.mock_font = mock_font
        self.mock_image_load = mock_image_load
        self.mock_image_load.return_value = pygame.Surface((50, 50))
        self.player = Player(self.screen)
        self.player.rect = pygame.Rect(100, 100, 50, 50)  # Set the player's initial position and size

    
    def test_singleton_pattern(self):
        """Tests that the Player class follows the Singleton pattern.
        
        Asserts:
            - That the first and second instances of Player are the same object.
        """
        player2 = Player(self.screen)
        self.assertIs(self.player, player2)
    
    def test_get_skills(self):
        """Tests the `get_skills` method of the Player class.

        Asserts:
            - The returned skills match the expected default values.
        """
        expected_skills = {"Eloquence": 0, "Clairvoyance": 0, "Forbearance": 0, "Resonance": 0}
        self.assertEqual(self.player.get_skills(), expected_skills)
    
    def test_set_skills(self):
        """Tests the `set_skills` method of the Player class.

        Asserts:
            - The player's skills are updated to the new values passed to `set_skills`.
        """
        new_skills = {"Eloquence": 5, "Clairvoyance": 3, "Forbearance": 4, "Resonance": 2}
        self.player.set_skills(new_skills)
        self.assertEqual(self.player.get_skills(), new_skills)
    
    @patch('numpy.random.randint')
    def test_roll_skill_check(self, mock_randint):
        """Tests the `roll_skill_check` method of the Player class.

        Args:
            mock_randint: Mock for the `numpy.random.randint` function to control the random result.

        Asserts:
            - The skill check passes when the random roll plus the skill level exceeds the difficulty.
            - The skill check fails when the random roll plus the skill level is below the difficulty.
        """
        mock_randint.return_value = 15
        self.player.eloquence = 5
        self.assertTrue(self.player.roll_skill_check("Eloquence", 18))
        self.assertFalse(self.player.roll_skill_check("Eloquence", 21))
    
    def test_raise_experience(self):
        """Tests the `raise_experience` method of the Player class.

        Verifies that the player's experience is correctly increased.

        Asserts:
            - The player's experience is incremented as expected when calling `raise_experience`.
        """
        self.player.experience = 0
        self.player.raise_experience(10)
        self.assertEqual(self.player.experience, 10)
    
    @patch('pygame.sprite.Sprite')
    def test_check_collision(self, MockSprite):
        """Tests the `check_collision` method of the Player class.

        Mocks sprites for collision detection and ensures that the player detects collisions correctly.

        Asserts:
            - The player collides with objects as expected based on their masks.
        """
        # Create a mock sprite (simulating an obstacle)
        mock_sprite = MockSprite.return_value
        mock_sprite.rect = pygame.Rect(150, 100, 50, 50)  # Position the mock sprite near the player
        mock_sprite.mask = pygame.mask.from_surface(pygame.Surface((500, 500)))  # Give the mock sprite a mask
        
        # Set the player mask (simulate the player's collision box)
        self.player.mask = pygame.mask.from_surface(pygame.Surface((500, 500)))

        # Call the `check_collision` method and assert collision detection
        all_sprites = [mock_sprite]  # Add the mock sprite to the list of all sprites
        collision = self.player.check_collision(all_sprites)
        self.assertTrue(collision, "Player should collide with the obstacle")

        # Move the mock sprite away from the player to test no collision
        mock_sprite.rect = pygame.Rect(30000, 10000, 50, 50)  # Move sprite far enough that no collision occurs
        collision = self.player.check_collision(all_sprites)
        self.assertFalse(collision, "Player should not collide when the obstacle is far away")

    @patch('pygame.sprite.Sprite')
    def test_no_collision_with_itself(self, MockSprite):
        """Tests if the player does not collide with itself.

        Ensures that the player’s own sprite is not considered for collision detection.
        """
        all_sprites = [self.player]  # Add the player to the all_sprites group
        collision = self.player.check_collision(all_sprites)
        self.assertFalse(collision, "Player should not collide with itself")

if __name__ == '__main__':
    unittest.main()