import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import json
import pygame
from src.ui.interaction import load_scene_interactions, get_key_to_node, DialogueManager


class TestLoadSceneInteractions(unittest.TestCase):

    @patch('src.ui.interaction.os.listdir')
    @patch('src.ui.interaction.open', new_callable=mock_open)
    @patch('src.ui.interaction.json.load')
    @patch('src.ui.interaction.DialogueManager')
    def test_load_scene_interactions(self, mock_dialogue_manager, mock_json_load, mock_open, mock_listdir):
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

    def test_get_key_to_node_with_keys(self):
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
        interactions = [
            {'title': 'Start', 'body': 'Hello'},
            {'title': 'Middle', 'body': 'How are you?'},
            {'title': 'End', 'body': 'Goodbye'}
        ]
        expected_output = {}
        result = get_key_to_node(interactions)
        self.assertEqual(result, expected_output)

    def test_get_key_to_node_mixed(self):
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

    def setUp(self):
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
        node = self.dialogue_manager.find_node('Start')
        self.assertIsNotNone(node)
        self.assertEqual(node['title'], 'Start')

    def test_find_node_non_existing(self):
        node = self.dialogue_manager.find_node('NonExisting')
        self.assertIsNone(node)

    def test_find_node_middle(self):
        node = self.dialogue_manager.find_node('Middle')
        self.assertIsNotNone(node)
        self.assertEqual(node['title'], 'Middle')

    def test_find_node_end(self):
        node = self.dialogue_manager.find_node('End')
        self.assertIsNotNone(node)
        self.assertEqual(node['title'], 'End')

if __name__ == '__main__':
    unittest.main()