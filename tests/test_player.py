import unittest
from unittest.mock import Mock, patch
import pygame
from src.characters.player import Player

class TestPlayer(unittest.TestCase):
    
    @patch('pygame.image.load')
    @patch('pygame.font.Font')
    def setUp(self, mock_font, mock_image_load):
        pygame.display.set_mode((800, 600))  # Initialize the display
        self.screen = pygame.Surface((800, 600))
        self.mock_font = mock_font
        self.mock_image_load = mock_image_load
        self.mock_image_load.return_value = pygame.Surface((50, 50))
        self.player = Player(self.screen)
    
    def test_singleton_pattern(self):
        player2 = Player(self.screen)
        self.assertIs(self.player, player2)
    
    def test_get_skills(self):
        expected_skills = {"Eloquence": 0, "Clairvoyance": 0, "Forbearance": 0, "Resonance": 0}
        self.assertEqual(self.player.get_skills(), expected_skills)
    
    def test_set_skills(self):
        new_skills = {"Eloquence": 5, "Clairvoyance": 3, "Forbearance": 4, "Resonance": 2}
        self.player.set_skills(new_skills)
        self.assertEqual(self.player.get_skills(), new_skills)
    
    @patch('numpy.random.randint')
    def test_roll_skill_check(self, mock_randint):
        mock_randint.return_value = 15
        self.player.eloquence = 5
        self.assertTrue(self.player.roll_skill_check("Eloquence", 18))
        self.assertFalse(self.player.roll_skill_check("Eloquence", 21))
    
    def test_raise_experience(self):
        self.player.experience = 0
        self.player.raise_experience(10)
        self.assertEqual(self.player.experience, 10)

if __name__ == '__main__':
    unittest.main()