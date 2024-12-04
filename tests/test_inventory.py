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
    """
    Classe de teste para a classe Inventory, utilizando a biblioteca unittest.
    """
    def setUp(self):
        """
        Configuração inicial para os testes. Cria mocks para itens e uma instância
        de Inventory com capacidade para 4 itens.
        """
        self.item1 = Mock(spec=Item)
        self.item2 = Mock(spec=Item)
        self.item3 = Mock(spec=Item)
        self.item4 = Mock(spec=Item)
        self.item5 = Mock(spec=Item)
        self.inventory = Inventory(capacity=4)

    def test_add_item_success(self):
        """
        Testa a adição bem-sucedida de um item ao inventário.
        Verifica se o item foi adicionado e está presente na lista de itens.
        """
        result = self.inventory.add_item(self.item1)
        self.assertTrue(result)
        self.assertIn(self.item1, self.inventory.items)

    def test_add_item_failure_due_to_capacity(self):
        """
        Testa a falha ao adicionar um item quando a capacidade do inventário é excedida.
        Verifica se a operação retorna False e se o item não está presente na lista de itens.
        """
        self.inventory.add_item(self.item1)
        self.inventory.add_item(self.item2)
        self.inventory.add_item(self.item3)
        self.inventory.add_item(self.item4)
        result = self.inventory.add_item(self.item5)
        self.assertFalse(result)
        self.assertNotIn(self.item5, self.inventory.items)

    def test_add_item_failure_due_to_duplicate(self):
        """
        Testa a falha ao adicionar um item duplicado ao inventário.
        Verifica se a operação retorna False e se o item aparece apenas uma vez na lista de itens.
        """
        self.inventory.add_item(self.item1)
        result = self.inventory.add_item(self.item1)
        self.assertFalse(result)
        self.assertEqual(self.inventory.items.count(self.item1), 1)

    def test_remove_item_success(self):
        """
        Testa a remoção bem-sucedida de um item do inventário.
        Verifica se a operação retorna True e se o item foi removido da lista de itens.
        """
        self.inventory.add_item(self.item1)
        result = self.inventory.remove_item(self.item1)
        self.assertTrue(result)
        self.assertNotIn(self.item1, self.inventory.items)

    def test_remove_item_failure(self):
        """
        Testa a falha ao tentar remover um item que não está no inventário.
        Verifica se a operação retorna False.
        """
        result = self.inventory.remove_item(self.item1)
        self.assertFalse(result)

    def test_has_item(self):
        """
        Testa a verificação da presença de um item no inventário.
        Verifica se has_item retorna True para um item presente e False para um item ausente.
        """
        self.inventory.add_item(self.item1)
        self.assertTrue(self.inventory.has_item(self.item1))
        self.assertFalse(self.inventory.has_item(self.item2))

    def test_clear_inventory(self):
        """
        Testa a funcionalidade de limpar o inventário.
        Verifica se a lista de itens está vazia após a operação.
        """
        self.inventory.add_item(self.item1)
        self.inventory.add_item(self.item2)
        self.inventory.clear_inventory()
        self.assertEqual(len(self.inventory.items), 0)

if __name__ == '__main__':
    unittest.main()