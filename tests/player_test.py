import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
import pygame
from src.characters.player import Player

class TestPlayer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.screen = pygame.display.set_mode((800, 600))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        # Mockando fontes e sequências animadas para evitar erros de carregamento
        font_patcher = patch('pygame.font.Font', return_value=MagicMock())
        self.addCleanup(font_patcher.stop)
        font_patcher.start()

        load_png_sequence_patcher = patch('src.ui.animated_sequence.load_png_sequence', return_value=[MagicMock()])
        self.addCleanup(load_png_sequence_patcher.stop)
        load_png_sequence_patcher.start()

        sequence_current_frame_patcher = patch('src.ui.animated_sequence.sequence_current_frame', return_value=MagicMock())
        self.addCleanup(sequence_current_frame_patcher.stop)
        sequence_current_frame_patcher.start()

        self.player = Player(self.screen)

    def test_initialization(self):
        self.assertEqual(self.player.position, [50, 450])
        self.assertEqual(self.player.eloquence, 0)
        self.assertEqual(self.player.clairvoyance, 0)
        self.assertEqual(self.player.forbearance, 0)
        self.assertEqual(self.player.resonance, 0)
        self.assertEqual(self.player.experience, 0)
        self.assertEqual(self.player.health, 4)
        self.assertEqual(self.player.reason, 2)
        self.assertEqual(self.player.speed, 5)
        self.assertIsNotNone(self.player.sprite)
        self.assertIsNotNone(self.player.stats_bar)

    def test_get_position(self):
        self.assertEqual(self.player.get_position(), [50, 450])

    def test_handle_movement(self):
        keys = pygame.key.get_pressed()
        with patch('pygame.key.get_pressed', return_value=keys):
            self.player.handle_movement(keys)
            self.assertEqual(self.player.position, [50, 450])

    def test_get_skills(self):
        expected_skills = {
            "Eloquence": 0,
            "Clairvoyance": 0,
            "Forbearance": 0,
            "Resonance": 0
        }
        self.assertEqual(self.player.get_skills(), expected_skills)

    def test_set_skills(self):
        new_skills = {
            "Eloquence": 5,
            "Clairvoyance": 3,
            "Forbearance": 4,
            "Resonance": 2
        }
        self.player.set_skills(new_skills)
        self.assertEqual(self.player.eloquence, 5)
        self.assertEqual(self.player.clairvoyance, 3)
        self.assertEqual(self.player.forbearance, 4)
        self.assertEqual(self.player.resonance, 2)

    @patch('numpy.random.randint', return_value=15)
    def test_roll_skill_check(self, mock_randint):
        self.player.eloquence = 5
        self.assertTrue(self.player.roll_skill_check("eloquence", 18))
        self.assertFalse(self.player.roll_skill_check("eloquence", 21))

    def test_reduce_attribute(self):
        self.player.health = 10
        self.player.reduce_attribute("health", 3)
        self.assertEqual(self.player.health, 7)

    def test_raise_experience(self):
        self.player.experience = 10
        self.player.raise_experience(5)
        self.assertEqual(self.player.experience, 15)

    def test_draw(self):
        try:
            self.player.draw()
        except Exception as e:
            self.fail(f"O método draw falhou com a exceção: {e}")

if __name__ == '__main__':
    unittest.main()