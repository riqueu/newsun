"""
Test module for the `load_png_sequence` function in the `animated_sequence` module.

This module contains unit tests for the `load_png_sequence` function, which loads a sequence of PNG images 
from a folder, converts them into `pygame.Surface` objects, and returns them as a list. The tests validate 
different scenarios such as successfully loading images from a folder, and handling cases where the folder is empty.

Functions:
    - `test_load_png_sequence`: Tests the loading of PNG files from a folder and checks if the result contains 
      valid `pygame.Surface` objects.
    - `test_load_png_sequence_empty_folder`: Tests the case when the folder contains no PNG files, ensuring 
      that the function returns an empty list.
"""

import unittest
import pygame
from src.ui.animated_sequence import load_png_sequence
from unittest.mock import patch, MagicMock

class TestLoadPngSequence(unittest.TestCase):
    """
    Test case for the `load_png_sequence` function.
    
    This test class validates the behavior of the `load_png_sequence` function in various scenarios.
    The function loads PNG images from a folder, converts them to `pygame.Surface` objects, and returns them as a list.
    """
    
    @patch('src.ui.animated_sequence.pygame.image.load')
    @patch('src.ui.animated_sequence.os.listdir')
    def test_load_png_sequence(self, mock_listdir, mock_load):
        """
        Tests the loading of PNG images from a folder and ensures the loaded surfaces are pygame.Surface objects.

        Asserts:
            - The result list contains 3 surfaces.
            - Each surface in the result is an instance of `pygame.Surface`.
        """
        # Setup mocks
        mock_listdir.return_value = ['00000.png', '00001.png', '00002.png']
        mock_load.return_value.convert_alpha.return_value = MagicMock(spec=pygame.Surface)

        # Call the function
        folder = 'mock_folder'
        result = load_png_sequence(folder)
        # Assertions
        self.assertEqual(len(result), 3)
        self.assertTrue(all(isinstance(surface, pygame.Surface) for surface in result))

    @patch('src.ui.animated_sequence.os.listdir')
    def test_load_png_sequence_empty_folder(self, mock_listdir):
        """
        Tests the case where the folder contains no PNG files.

        Asserts:
            - The result is an empty list when no PNG files are found in the folder.
        """
        # Setup mocks
        mock_listdir.return_value = []

        # Call the function
        folder = 'mock_folder'
        result = load_png_sequence(folder)

        # Assertions
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()