import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pygame
from src.characters.npc import Interactable, Object, NPC
from settings import WIDTH, HEIGHT

class TestNPC(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.player_rect = pygame.Rect(100, 100, 50, 50)
        self.sprite = pygame.Surface((50, 50))
        self.sprite.fill((255, 0, 0))

    def test_interactable_initialization(self):
        interactable = Interactable((100, 100), self.sprite, "TestInteractable")
        self.assertEqual(interactable.name, "TestInteractable")
        self.assertEqual(interactable.rect.topleft, (100, 100))

    def test_player_in_interaction_range(self):
        interactable = Interactable((100, 100), self.sprite, "TestInteractable")
        self.assertTrue(interactable.player_in_interaction_range(self.player_rect))

    def test_object_initialization(self):
        obj = Object((200, 200), "TestObject")
        self.assertEqual(obj.name, "TestObject")
        self.assertEqual(obj.rect.topleft, (200, 200))

    def test_npc_initialization(self):
        npc = NPC((300, 300), "TestNPC", self.sprite)
        self.assertEqual(npc.name, "TestNPC")
        self.assertEqual(npc.rect.topleft, (300, 300))

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()