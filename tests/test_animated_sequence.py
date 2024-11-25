import unittest
import pygame
from src.ui.animated_sequence import load_png_sequence
from unittest.mock import patch, MagicMock

class TestLoadPngSequence(unittest.TestCase):

    @patch('src.ui.animated_sequence.pygame.image.load')
    @patch('src.ui.animated_sequence.os.listdir')
    def test_load_png_sequence(self, mock_listdir, mock_load):
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
        # Setup mocks
        mock_listdir.return_value = []

        # Call the function
        folder = 'mock_folder'
        result = load_png_sequence(folder)

        # Assertions
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()