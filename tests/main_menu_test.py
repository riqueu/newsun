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

    @patch('src.ui.animated_sequence.black_bg.draw')
    @patch('src.ui.animated_sequence.black_bg.animate')
    def test_draw(self, mock_animate, mock_draw):
        self.main_menu.draw()
        mock_draw.assert_called_once_with(self.screen)
        mock_animate.assert_called_once()

    def test_handle_event_up(self):
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
        self.main_menu.handle_event(event)
        self.assertEqual(self.main_menu.selected_option, len(self.main_menu.options) - 1)

    def test_handle_event_down(self):
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
        self.main_menu.handle_event(event)
        self.assertEqual(self.main_menu.selected_option, 1)

    def test_handle_event_select(self):
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_z)
        selected_option = self.main_menu.handle_event(event)
        self.assertEqual(selected_option, "Start Game")
        def test_draw_title_and_keybinds(self):
            with patch.object(self.main_menu, 'title_font') as mock_title_font, \
                 patch.object(self.main_menu, 'font') as mock_font:
                mock_title_font.render.return_value = pygame.Surface((100, 50))
                mock_font.render.return_value = pygame.Surface((200, 50))
                self.main_menu.draw()
                mock_title_font.render.assert_called_once_with("Newsun", True, self.main_menu.default_color)
                mock_font.render.assert_called_once_with("Z to Select | X to Cancel | Arrows to Move", True, self.main_menu.default_color)

        def test_draw_options(self):
            with patch.object(self.main_menu, 'font') as mock_font:
                mock_font.render.return_value = pygame.Surface((200, 50))
                self.main_menu.draw()
                self.assertEqual(mock_font.render.call_count, len(self.main_menu.options))
                for i, option in enumerate(self.main_menu.options):
                    color = self.main_menu.default_color if i == self.main_menu.selected_option else (100, 100, 100)
                    mock_font.render.assert_any_call(option, True, color)

        def test_handle_event_cancel(self):
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_x)
            selected_option = self.main_menu.handle_event(event)
            self.assertIsNone(selected_option)

        def test_handle_event_no_key(self):
            event = pygame.event.Event(pygame.KEYUP, key=pygame.K_UP)
            selected_option = self.main_menu.handle_event(event)
            self.assertIsNone(selected_option)
    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()