import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pygame
from src.characters.player import Player
from settings import WIDTH, HEIGHT

class TestPlayer(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.player = Player(self.screen)

    def test_initial_position(self):
        self.assertEqual(self.player.get_position(), [50, 450])

    def test_movement_up(self):
        keys = pygame.key.get_pressed()
        keys[pygame.K_UP] = True
        self.player.handle_movement(keys)
        self.assertEqual(self.player.get_position(), [50, 450 - self.player.speed])

    def test_movement_down(self):
        keys = pygame.key.get_pressed()
        keys[pygame.K_DOWN] = True
        self.player.handle_movement(keys)
        self.assertEqual(self.player.get_position(), [50, 450 + self.player.speed])

    def test_movement_left(self):
        keys = pygame.key.get_pressed()
        keys[pygame.K_LEFT] = True
        self.player.handle_movement(keys)
        self.assertEqual(self.player.get_position(), [50 - self.player.speed, 450])

    def test_movement_right(self):
        keys = pygame.key.get_pressed()
        keys[pygame.K_RIGHT] = True
        self.player.handle_movement(keys)
        self.assertEqual(self.player.get_position(), [50 + self.player.speed, 450])

    def test_boundary_collision_top(self):
        self.player.position = [50, 0]
        keys = pygame.key.get_pressed()
        keys[pygame.K_UP] = True
        self.player.handle_movement(keys)
        self.assertEqual(self.player.get_position(), [50, 0])

    def test_boundary_collision_bottom(self):
        self.player.position = [50, HEIGHT - self.player.sprite.get_height()]
        keys = pygame.key.get_pressed()
        keys[pygame.K_DOWN] = True
        self.player.handle_movement(keys)
        self.assertEqual(self.player.get_position(), [50, HEIGHT - self.player.sprite.get_height()])

    def test_boundary_collision_left(self):
        self.player.position = [0, 450]
        keys = pygame.key.get_pressed()
        keys[pygame.K_LEFT] = True
        self.player.handle_movement(keys)
        self.assertEqual(self.player.get_position(), [0, 450])

    def test_boundary_collision_right(self):
        self.player.position = [WIDTH - self.player.sprite.get_width(), 450]
        keys = pygame.key.get_pressed()
        keys[pygame.K_RIGHT] = True
        self.player.handle_movement(keys)
        self.assertEqual(self.player.get_position(), [WIDTH - self.player.sprite.get_width(), 450])

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()