"""
Module for Inventory Testing
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import Mock
from src.ui.inventory import Item, Inventory

class TestInventory(unittest.TestCase):

    def setUp(self):
        self.item1 = Mock(spec=Item)
        self.item2 = Mock(spec=Item)
        self.item3 = Mock(spec=Item)
        self.item4 = Mock(spec=Item)
        self.item5 = Mock(spec=Item)
        self.inventory = Inventory(capacity=4)

    def test_add_item_success(self):
        result = self.inventory.add_item(self.item1)
        self.assertTrue(result)
        self.assertIn(self.item1, self.inventory.items)

    def test_add_item_failure_due_to_capacity(self):
        self.inventory.add_item(self.item1)
        self.inventory.add_item(self.item2)
        self.inventory.add_item(self.item3)
        self.inventory.add_item(self.item4)
        result = self.inventory.add_item(self.item5)
        self.assertFalse(result)
        self.assertNotIn(self.item5, self.inventory.items)

    def test_add_item_failure_due_to_duplicate(self):
        self.inventory.add_item(self.item1)
        result = self.inventory.add_item(self.item1)
        self.assertFalse(result)
        self.assertEqual(self.inventory.items.count(self.item1), 1)

    def test_remove_item_success(self):
        self.inventory.add_item(self.item1)
        result = self.inventory.remove_item(self.item1)
        self.assertTrue(result)
        self.assertNotIn(self.item1, self.inventory.items)

    def test_remove_item_failure(self):
        result = self.inventory.remove_item(self.item1)
        self.assertFalse(result)

    def test_has_item(self):
        self.inventory.add_item(self.item1)
        self.assertTrue(self.inventory.has_item(self.item1))
        self.assertFalse(self.inventory.has_item(self.item2))

    def test_clear_inventory(self):
        self.inventory.add_item(self.item1)
        self.inventory.add_item(self.item2)
        self.inventory.clear_inventory()
        self.assertEqual(len(self.inventory.items), 0)

if __name__ == '__main__':
    unittest.main()