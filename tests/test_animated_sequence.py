import unittest
import pygame
from src.ui.animated_sequence import load_png_sequence

class TestLoadPngSequence(unittest.TestCase):

    def test_load_png_sequence(self):
        # Call the function
        folder = 'tests/test_data/animated_sequence'
        result = load_png_sequence(folder)

        # Assertions
        self.assertEqual(len(result), 3)
        self.assertTrue(all(isinstance(surface, pygame.Surface) for surface in result))

    def test_load_png_sequence_empty_folder(self):
        # Call the function
        folder = 'tests/test_data/empty'
        result = load_png_sequence(folder)

        # Assertions
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()