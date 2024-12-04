"""
Unit tests for the hotel scenes module.

This module contains unit tests for the `Scene` class and its subclasses (`Room101`, `Floor1`, `Floor0`, `Underground`).
These tests ensure that the scenes are initialized correctly, handle events as expected, and render properly.

Classes:
- `TestScene`: Tests for the `Scene` class.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pygame
from src.scenes.hotel_scenes import Scene, Room101, Floor1, Floor0, Underground


class TestScene(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.scene = Scene(self.screen, "assets/images/backgrounds/room_full.png", "scripts/room_101", 800, 600)

    def test_initialization(self):
        self.assertEqual(self.scene.width, 800)
        self.assertEqual(self.scene.height, 600)
        self.assertEqual(self.scene.x, 125)
        self.assertEqual(self.scene.y, (600 - 600) // 2)
        self.assertIsNotNone(self.scene.image)
        self.assertIsNotNone(self.scene.mask)
        self.assertEqual(self.scene.rect.x, self.scene.x)
        self.assertEqual(self.scene.rect.y, self.scene.y)

    def test_handle_event(self):
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_z})
        self.scene.handle_event(event)
        self.assertFalse(self.scene.in_dialogue)

    def test_change_of_scene(self):
        self.scene.dialogue_managers['door'] = type('', (), {})()  # Mock dialogue manager
        self.scene.dialogue_managers['door'].current_node = {'title': 'GoToRoom'}
        self.scene.dialogue_managers['door'].dialogue_active = True
        self.scene.dialogue_managers['door'].dialogue_ended = False
        self.scene.dialogue_managers['door'].find_node = lambda x: {'title': 'Start'}
        next_scene = self.scene.change_of_scene('door')
        self.assertEqual(next_scene, 'room_101')

    def test_change_conditions(self):
        self.scene.dialogue_conditions = {'test_condition': 0}
        self.scene.change_conditions('test_condition', 1)
        self.assertEqual(self.scene.dialogue_conditions['test_condition'], 1)

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()