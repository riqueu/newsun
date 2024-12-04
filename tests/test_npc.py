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
    """
    Classe de teste para a classe Interactable, utilizando a biblioteca unittest.
    """
    def setUp(self):
        """
        Configuração inicial para os testes. Inicializa o pygame, cria um sprite e uma instância
        de Interactable com uma posição e um nome.
        """
        pygame.init()
        self.sprite = pygame.Surface((50, 50))
        self.sprite.fill((255, 0, 0))
        self.interactable = Interactable((100, 100), self.sprite, "TestObject")

    def tearDown(self):
        """
        Finaliza o pygame após os testes.
        """
        pygame.quit()

    def test_initialization(self):
        """
        Testa a inicialização do objeto Interactable. Verifica se o nome do objeto está correto.
        """
        self.assertEqual(self.interactable.name, "TestObject")
        self.assertEqual(self.interactable.rect.topleft, (100, 100))
        self.assertIsInstance(self.interactable.image, pygame.Surface)

    def test_player_in_interaction_range_true(self):
        player_rect = pygame.Rect(105, 105, 50, 50)
        self.assertTrue(self.interactable.player_in_interaction_range(player_rect))

    def test_player_in_interaction_range_false(self):
        """
        Testa se o jogador não está no alcance de interação padrão do Interactable.
        """
        player_rect = pygame.Rect(200, 200, 50, 50)
        self.assertFalse(self.interactable.player_in_interaction_range(player_rect))

    def test_player_in_interaction_range_custom_range(self):
        player_rect = pygame.Rect(150, 150, 50, 50)
        self.assertTrue(self.interactable.player_in_interaction_range(player_rect, interaction_range=100))

if __name__ == '__main__':
    unittest.main()