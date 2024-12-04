import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pygame
from src.characters.player import Player
from settings import WIDTH, HEIGHT

class TestPlayer(unittest.TestCase):
    def setUp(self):
        pygame.font.init()
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.player = Player(self.screen)
        self.player.add_game(self)  # Adiciona o jogo ao jogador

    def test_initial_position(self):
        self.assertEqual(self.player.get_position(), [50, 450])

    def test_movement_up(self):
        keys = pygame.key.get_pressed()
        keys = list(keys)  # Converte para lista para permitir modificações
        keys[pygame.K_UP] = True
        self.player.handle_movement()
        self.assertEqual(self.player.get_position(), [50, 450 - self.player.speed])

    def test_boundary_collision_right(self):
        self.player.rect.x = WIDTH - self.player.width
        self.player.rect.y = 450
        keys = pygame.key.get_pressed()
        keys = list(keys)  # Converte para lista para permitir modificações
        keys[pygame.K_RIGHT] = True
        self.player.handle_movement()
        self.player.update()
        self.assertEqual(self.player.rect.x, WIDTH - self.player.width)
        self.assertEqual(self.player.rect.y, 450)

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()