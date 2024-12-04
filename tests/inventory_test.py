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
        def test_add_item_success(self):
            item = Item("Potion", "path/to/potion.png")
            result = self.inventory.add_item(item)
            self.assertTrue(result)
            self.assertIn(item, self.inventory.items)

        def test_add_item_failure_full_inventory(self):
            self.inventory.capacity = 1
            item1 = Item("Potion", "path/to/potion.png")
            item2 = Item("Elixir", "path/to/elixir.png")
            self.inventory.add_item(item1)
            result = self.inventory.add_item(item2)
            self.assertFalse(result)
            self.assertNotIn(item2, self.inventory.items)

        def test_add_item_failure_duplicate(self):
            item = Item("Potion", "path/to/potion.png")
            self.inventory.add_item(item)
            result = self.inventory.add_item(item)
            self.assertFalse(result)
            self.assertEqual(self.inventory.items.count(item), 1)

        def test_remove_item_success(self):
            item = Item("Potion", "path/to/potion.png")
            self.inventory.add_item(item)
            result = self.inventory.remove_item(item)
            self.assertTrue(result)
            self.assertNotIn(item, self.inventory.items)

        def test_remove_item_failure(self):
            item = Item("Potion", "path/to/potion.png")
            result = self.inventory.remove_item(item)
            self.assertFalse(result)

        def test_clear_inventory(self):
            item1 = Item("Potion", "path/to/potion.png")
            item2 = Item("Elixir", "path/to/elixir.png")
            self.inventory.add_item(item1)
            self.inventory.add_item(item2)
            self.inventory.clear_inventory()
            self.assertEqual(len(self.inventory.items), 0)

        def test_draw_inventory(self):
            screen = pygame.display.set_mode((800, 600))
            item = Item("Potion", "path/to/potion.png")
            self.inventory.add_item(item)
            self.inventory.draw(screen)
            # Since we cannot directly test the drawing, we ensure no exceptions are raised
if __name__ == '__main__':
    unittest.main()