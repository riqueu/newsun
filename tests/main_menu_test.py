import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
import unittest
from unittest.mock import patch
from src.scenes.main_menu import MainMenu

class TestMainMenu(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.main_menu = MainMenu(self.screen)

    def test_initialization(self):
        self.assertEqual(self.main_menu.options, ["Start Game", "Options", "Exit"])
        self.assertEqual(self.main_menu.selected_option, 0)
        self.assertIsNotNone(self.main_menu.title_font)
        self.assertIsNotNone(self.main_menu.font)
        self.assertEqual(self.main_menu.default_color, (255, 255, 255))
        self.assertIsNotNone(self.main_menu.black_bg)

    @patch('src.ui.animated_sequence.load_png_sequence')
    @patch('src.ui.animated_sequence.sequence_current_frame')
    def test_draw(self, mock_sequence_current_frame, mock_load_png_sequence):
        mock_surface = pygame.Surface((800, 600))
        mock_load_png_sequence.return_value = [mock_surface]
        mock_sequence_current_frame.return_value = mock_surface
        self.main_menu.black_bg = mock_load_png_sequence('assets/ui/BlackBG')
        try:
            self.main_menu.draw()
        except Exception as e:
            self.fail(f"Falha ao desenhar o menu principal: {e}")

    def test_handle_event_up(self):
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP})
        self.main_menu.handle_event(event)
        expected_option = (0 - 1) % len(self.main_menu.options)
        self.assertEqual(self.main_menu.selected_option, expected_option)

    def test_handle_event_down(self):
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})
        self.main_menu.handle_event(event)
        expected_option = (0 + 1) % len(self.main_menu.options)
        self.assertEqual(self.main_menu.selected_option, expected_option)

    def test_handle_event_select(self):
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_z})
        selected_option = self.main_menu.handle_event(event)
        self.assertEqual(selected_option, self.main_menu.options[self.main_menu.selected_option])

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()