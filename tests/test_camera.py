"""
Unit tests for the Camera module in Pygame
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pygame
from src.ui.camera import Camera
from unittest.mock import Mock


class TestCamera(unittest.TestCase):

    def setUp(self):
        self.game = Mock()
        self.width = 800
        self.height = 600
        self.camera = Camera(self.game, self.width, self.height)
        self.target = Mock()
        self.target.rect = pygame.Rect(100, 100, 50, 50)

    def test_initialization(self):
        self.assertEqual(self.camera.camera_rect.width, self.width)
        self.assertEqual(self.camera.camera_rect.height, self.height)
        self.assertEqual(self.camera.offset.x, 0)
        self.assertEqual(self.camera.offset.y, 0)

    def test_box_target_camera_left_border(self):
        self.target.rect.left = 50
        self.camera.box_target_camera(self.target)
        self.assertEqual(self.camera.camera_rect.left, -150)

    def test_box_target_camera_right_border(self):
        self.target.rect.right = 850
        self.camera.box_target_camera(self.target)
        self.assertEqual(self.camera.camera_rect.right, 1050)

    def test_box_target_camera_top_border(self):
        self.target.rect.top = 50
        self.camera.box_target_camera(self.target)
        self.assertEqual(self.camera.camera_rect.top, -150)

    def test_box_target_camera_bottom_border(self):
        self.target.rect.bottom = 650
        self.camera.box_target_camera(self.target)
        self.assertEqual(self.camera.camera_rect.bottom, 850)

    def test_keyboard_control(self):
        pygame.key.get_pressed = Mock(return_value=[0] * 323)
        pygame.key.get_pressed()[pygame.K_a] = 1
        self.camera.keyboard_control()
        self.assertEqual(self.camera.camera_rect.x, -self.camera.keyboard_speed)

        pygame.key.get_pressed = Mock(return_value=[0] * 323)
        pygame.key.get_pressed()[pygame.K_d] = 1
        self.camera.keyboard_control()
        self.assertEqual(self.camera.camera_rect.x, 0)

        pygame.key.get_pressed = Mock(return_value=[0] * 323)
        pygame.key.get_pressed()[pygame.K_w] = 1
        self.camera.keyboard_control()
        self.assertEqual(self.camera.camera_rect.y, -self.camera.keyboard_speed)

        pygame.key.get_pressed = Mock(return_value=[0] * 323)
        pygame.key.get_pressed()[pygame.K_s] = 1
        self.camera.keyboard_control()
        self.assertEqual(self.camera.camera_rect.y, 0)

if __name__ == '__main__':
    unittest.main()