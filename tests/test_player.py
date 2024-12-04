"""
Unit tests for the `Player` class.

This module tests the functionality of the `Player` class, including skills, skill checks, experience, and the singleton pattern.

Tests:
    - Singleton pattern for `Player` instance.
    - Retrieval and setting of player skills.
    - Skill check functionality using random values.
    - Experience point increment.
"""

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

if __name__ == '__main__':
    unittest.main()