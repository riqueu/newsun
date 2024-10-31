"""PLACEHOLDER: NPC class for creating non-player characters in the game."""

class NPC:
    def __init__(self, name, dialogue_lines):
        """Initializes the NPC with a name and a list of dialogue lines."""
        self.name = name
        self.dialogue_lines = dialogue_lines
        self.current_line = 0

    def speak(self):
        """Displays the next line of dialogue for the NPC."""
        if self.current_line < len(self.dialogue_lines):
            print(f"{self.name}: {self.dialogue_lines[self.current_line]}")
            self.current_line += 1
        else:
            print(f"{self.name} has nothing more to say.")
            self.current_line = 0  # Reset dialogue for next interaction
