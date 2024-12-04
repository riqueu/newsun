import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch
from src.characters.npc import NPC

class TestNPC(unittest.TestCase):

    def setUp(self):
        self.npc = NPC(
            name="TestNPC",
            dialogue_lines=["Olá!", "Como vai?", "Até logo!"]
        )

    def test_npc_initialization(self):
        self.assertEqual(self.npc.name, "TestNPC")
        self.assertEqual(self.npc.dialogue_lines, ["Olá!", "Como vai?", "Até logo!"])
        self.assertEqual(self.npc.current_line, 0)

    @patch('builtins.print')
    def test_npc_speak(self, mock_print):
        # Testa todas as linhas de diálogo em sequência
        self.npc.speak()
        self.assertEqual(self.npc.current_line, 1)
        mock_print.assert_called_with("TestNPC: Olá!")

        self.npc.speak()
        self.assertEqual(self.npc.current_line, 2)
        mock_print.assert_called_with("TestNPC: Como vai?")

        self.npc.speak()
        self.assertEqual(self.npc.current_line, 3)
        mock_print.assert_called_with("TestNPC: Até logo!")

        # Depois de todas as linhas, deve reiniciar o diálogo
        self.npc.speak()
        self.assertEqual(self.npc.current_line, 0)
        mock_print.assert_called_with("TestNPC has nothing more to say.")

    @patch('builtins.print')
    def test_npc_speak_multiple_cycles(self, mock_print):
        # Executa várias vezes para testar a reinicialização do diálogo
        total_lines = len(self.npc.dialogue_lines)
        cycles = 2
        for cycle in range(cycles):
            for line in range(total_lines):
                self.npc.speak()
                self.assertEqual(self.npc.current_line, line + 1)
            # Após o último, deve reiniciar
            self.npc.speak()
            self.assertEqual(self.npc.current_line, 0)
        self.assertEqual(mock_print.call_count, cycles * (total_lines + 1))

    @patch('builtins.print')
    def test_npc_speak_no_dialogue(self, mock_print):
        # Testa NPC sem linhas de diálogo
        npc_no_dialogue = NPC(name="SilentNPC", dialogue_lines=[])
        npc_no_dialogue.speak()
        self.assertEqual(npc_no_dialogue.current_line, 0)
        mock_print.assert_called_with("SilentNPC has nothing more to say.")

if __name__ == '__main__':
    unittest.main()