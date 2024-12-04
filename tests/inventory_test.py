import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from src.ui.inventory import Item, Inventory

class TestInventory(unittest.TestCase):

    def setUp(self):
        self.inventory = Inventory()
        self.item1 = Item("Sword")
        self.item2 = Item("Shield")

    def test_add_item(self):
        self.inventory.add_item(self.item1)
        self.assertIn(self.item1, self.inventory.items)
        self.inventory.add_item(self.item2)
        self.assertIn(self.item2, self.inventory.items)

    def test_remove_item(self):
        self.inventory.add_item(self.item1)
        self.inventory.add_item(self.item2)
        self.inventory.remove_item("Sword")
        self.assertNotIn(self.item1, self.inventory.items)
        self.assertIn(self.item2, self.inventory.items)

    def test_has_item(self):
        self.inventory.add_item(self.item1)
        self.assertTrue(self.inventory.has_item("Sword"))
        self.assertFalse(self.inventory.has_item("Shield"))

    def test_display(self):
        self.inventory.add_item(self.item1)
        self.inventory.add_item(self.item2)
        # Captura a saída do método display
        from io import StringIO
        import sys
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        self.inventory.display()
        sys.stdout = sys.__stdout__
        output = capturedOutput.getvalue().strip()
        expected_output = "Inventory: Sword, Shield"
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()