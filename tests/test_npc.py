"""
Tests for the Interactable class.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pygame
from src.characters.npc import Interactable

class TestInteractable(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.sprite = pygame.Surface((50, 50))
        self.sprite.fill((255, 0, 0))
        self.interactable = Interactable((100, 100), self.sprite, "TestObject")

    def tearDown(self):
        pygame.quit()

    def test_initialization(self):
        self.assertEqual(self.interactable.name, "TestObject")
        self.assertEqual(self.interactable.rect.topleft, (100, 100))
        self.assertIsInstance(self.interactable.image, pygame.Surface)

    def test_player_in_interaction_range_true(self):
        player_rect = pygame.Rect(105, 105, 50, 50)
        self.assertTrue(self.interactable.player_in_interaction_range(player_rect))

    def test_player_in_interaction_range_false(self):
        player_rect = pygame.Rect(200, 200, 50, 50)
        self.assertFalse(self.interactable.player_in_interaction_range(player_rect))

    def test_player_in_interaction_range_custom_range(self):
        player_rect = pygame.Rect(150, 150, 50, 50)
        self.assertTrue(self.interactable.player_in_interaction_range(player_rect, interaction_range=100))

if __name__ == '__main__':
    unittest.main()