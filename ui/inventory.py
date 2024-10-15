class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item_name):
        """Adds an item to the inventory."""
        self.items.append(item_name)
        print(f"{item_name} added to inventory.")

    def remove_item(self, item_name):
        """Removes an item from the inventory."""
        if item_name in self.items:
            self.items.remove(item_name)
            print(f"{item_name} removed from inventory.")
        else:
            print(f"{item_name} not found in inventory.")

    def has_item(self, item_name):
        """Checks if the inventory contains a specific item."""
        return item_name in self.items

    def display(self):
        """Displays the inventory."""
        if self.items:
            print("Inventory:", ", ".join(self.items))
        else:
            print("Your inventory is empty.")
