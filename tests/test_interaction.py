"""
Test module for the `interaction` module, covering the functions `load_scene_interactions`, 
`get_key_to_node`, and the `DialogueManager` class.

This module contains unit tests that verify the correct behavior of various functions and methods
within the `interaction` module. It uses mocking to simulate dependencies and isolate the logic 
being tested.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import pygame
from src.ui.interaction import load_scene_interactions, get_key_to_node, DialogueManager


class TestLoadSceneInteractions(unittest.TestCase):
    """
    Unit test class for the `load_scene_interactions` function in the `interaction` module.

    Tests the loading and processing of interaction data from JSON files using mocking to 
    simulate file operations and external dependencies.
    """

    @patch('src.ui.interaction.os.listdir')
    @patch('src.ui.interaction.open', new_callable=mock_open)
    @patch('src.ui.interaction.json.load')
    @patch('src.ui.interaction.DialogueManager')
    def test_load_scene_interactions(self, mock_dialogue_manager, mock_json_load, mock_open, mock_listdir):
        """
        Test for the `load_scene_interactions` function.

        Mocks file operations to simulate reading multiple JSON interaction files. 
        Verifies the correct loading of interactions, including file opening and JSON parsing.

        Assertions:
            - Verifies the number of interactions loaded.
            - Checks that the correct interaction keys are present in the result.
            - Ensures the function interacts with file reading and JSON loading correctly.
        """
        # Setup
        scripts_path = 'fake_path'
        screen = MagicMock(spec=pygame.Surface)
        mock_listdir.return_value = ['interaction1.json', 'interaction2.json']
        mock_json_load.side_effect = [
            {'title': 'Start', 'body': 'Hello'},
            {'title': 'End', 'body': 'Goodbye'}
        ]

        # Execute
        result = load_scene_interactions(scripts_path, screen)

        # Verify
        self.assertEqual(len(result), 2)
        self.assertIn('interaction1', result)
        self.assertIn('interaction2', result)
        mock_listdir.assert_called_once_with(scripts_path)
        mock_open.assert_any_call(os.path.join(scripts_path, 'interaction1.json'), 'r', encoding='utf8')
        mock_open.assert_any_call(os.path.join(scripts_path, 'interaction2.json'), 'r', encoding='utf8')
        self.assertEqual(mock_json_load.call_count, 2)
        self.assertEqual(mock_dialogue_manager.call_count, 2)
      
        
class TestGetKeyToNode(unittest.TestCase):
    """
    Test cases for the `get_key_to_node` function.

    Verifies that the function correctly extracts the key mapping from a list of interactions.
    Tests include cases with keys, without keys, and a mix of both.
    """


    def test_get_key_to_node_with_keys(self):
        """
        Test case for `get_key_to_node` with interactions that include keys.

        Verifies that the function correctly maps node titles to their respective keys when keys are provided in the interaction data.

        Assertions:
            - Confirms that the output dictionary correctly associates each node's title with its respective key.
        """

        interactions = [
            {'title': 'Start', 'body': 'Hello', 'key': 'a'},
            {'title': 'Middle', 'body': 'How are you?', 'key': 'b'},
            {'title': 'End', 'body': 'Goodbye', 'key': 'c'}
        ]
        expected_output = {
            'Start': 'a',
            'Middle': 'b',
            'End': 'c'
        }
        result = get_key_to_node(interactions)
        self.assertEqual(result, expected_output)

    def test_get_key_to_node_without_keys(self):
        """
        Test case for `get_key_to_node` with interactions that do not include keys.

        Verifies that the function returns an empty dictionary when no keys are provided in the interaction data.

        Assertions:
            - Confirms that the output is an empty dictionary when no keys are present.
        """

        interactions = [
            {'title': 'Start', 'body': 'Hello'},
            {'title': 'Middle', 'body': 'How are you?'},
            {'title': 'End', 'body': 'Goodbye'}
        ]
        expected_output = {}
        result = get_key_to_node(interactions)
        self.assertEqual(result, expected_output)

    def test_get_key_to_node_mixed(self):
        """
        Test case for `get_key_to_node` with mixed interactions (some with keys, some without).

        Verifies that the function correctly maps the titles with keys and excludes those without keys.

        Assertions:
            - Confirms that the function returns a dictionary with only the titles that have associated keys.
        """
        interactions = [
            {'title': 'Start', 'body': 'Hello', 'key': 'a'},
            {'title': 'Middle', 'body': 'How are you?'},
            {'title': 'End', 'body': 'Goodbye', 'key': 'c'}
        ]
        expected_output = {
            'Start': 'a',
            'End': 'c'
        }
        result = get_key_to_node(interactions)
        self.assertEqual(result, expected_output)


class TestDialogueManager(unittest.TestCase):
    """
    Test suite for the `DialogueManager` class.

    Tests the functionality of `DialogueManager`, including node searching and dialogue management.
    """
    def setUp(self):
        """
        Initializes necessary components before each test.

        Sets up:
        - A pygame screen (800x600).
        - Sample dialogue data and key-to-node mapping.
        - Initializes the `DialogueManager` instance for testing.

        This ensures that each test has a fresh, consistent environment to run in.
        """
        pygame.init()
        self.screen = pygame.Surface((800, 600))
        self.dialogue_data = [
            {'title': 'Start', 'body': 'Hello'},
            {'title': 'Middle', 'body': 'How are you?'},
            {'title': 'End', 'body': 'Goodbye'}
        ]
        self.key_to_node = {
            'Start': 'a',
            'Middle': 'b',
            'End': 'c'
        }
        self.dialogue_manager = DialogueManager(self.screen, self.dialogue_data, self.key_to_node)

    def test_find_node_existing(self):
        """
        Tests if the `find_node` method correctly finds an existing node.
        """
        node = self.dialogue_manager.find_node('Start')
        self.assertIsNotNone(node)
        self.assertEqual(node['title'], 'Start')

    def test_find_node_non_existing(self):
        """
        Tests if the `find_node` method returns None for a non-existing node.
        """
        node = self.dialogue_manager.find_node('NonExisting')
        self.assertIsNone(node)

    def test_find_node_middle(self):
        """
        Tests if the `find_node` method returns the correct node for the 'Middle' title.
        """
        node = self.dialogue_manager.find_node('Middle')
        self.assertIsNotNone(node)
        self.assertEqual(node['title'], 'Middle')

    def test_find_node_end(self):
        """
        Tests if the `find_node` method returns the correct node for the 'End' title.
        """
        node = self.dialogue_manager.find_node('End')
        self.assertIsNotNone(node)
        self.assertEqual(node['title'], 'End')

if __name__ == '__main__':
    unittest.main()