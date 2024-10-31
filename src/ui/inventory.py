"""PLACEHOLDER: Inventory system for the game."""

class Item:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        """Adds an item to the inventory."""
        self.items.append(item)
        print(f"{item} added to inventory.")

    def remove_item(self, item_name):
        """Removes an item from the inventory."""
        for item in self.items:
            if item.name == item_name:
                self.items.remove(item)
                print(f"{item_name} removed from inventory.")
                return
        print(f"{item_name} not found in inventory.")

    def has_item(self, item_name):
        """Checks if the inventory contains a specific item."""
        return any(item.name == item_name for item in self.items)

    def display(self):
        """Displays the inventory."""
        if self.items:
            print("Inventory:", ", ".join(str(item) for item in self.items))
        else:
            print("Your inventory is empty.")
