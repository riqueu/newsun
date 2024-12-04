import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pygame
from unittest.mock import patch, mock_open
from src.ui.interaction import get_key_to_node, load_scene_interactions, DialogueBox, DialogueManager

class TestInteraction(unittest.TestCase):

    def test_get_key_to_node(self):
        interactions = [
            {'title': 'Start', 'key': {'a': 'Middle'}},
            {'title': 'Middle', 'key': {'b': 'End'}},
            {'title': 'End'}
        ]
        expected_output = {
            'Start': {'a': 'Middle'},
            'Middle': {'b': 'End'}
        }
        self.assertEqual(get_key_to_node(interactions), expected_output)

    @patch('os.listdir')
    @patch('builtins.open')
    @patch('json.load')
    def test_load_scene_interactions(self, mock_json_load, mock_open_file, mock_listdir):
        # Configura os mocks
        mock_listdir.return_value = ['interaction1.json', 'interaction2.json']
        interaction_data = [
            {'title': 'Start', 'key': {'a': 'Middle'}},
            {'title': 'Middle', 'key': {'b': 'End'}},
            {'title': 'End'}
        ]
        mock_json_load.return_value = interaction_data
        screen = pygame.Surface((800, 600))
        scripts_path = 'mock_path'

        dialogue_managers = load_scene_interactions(scripts_path, screen)

        self.assertEqual(len(dialogue_managers), 2)
        self.assertIsInstance(dialogue_managers['interaction1'], DialogueManager)
        self.assertIsInstance(dialogue_managers['interaction2'], DialogueManager)

if __name__ == '__main__':
    unittest.main()