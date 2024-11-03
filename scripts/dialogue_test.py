"""TEMP. TEST SCRIPT FOR DIALOGUE TREE GAME"""
import pygame
import json

# Screen dimensions
WIDTH = 1280
HEIGHT = 720

class DialogueBox:
    def __init__(self, font, width, height):
        self.font = font
        self.width = width
        self.height = height
        self.text = ""
        self.lines = []

    def set_text(self, text):
        self.text = text
        self.lines = self.wrap_text(text)

    def wrap_text(self, text):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            if '\n' in word:
                parts = word.split('\n')
                for part in parts[:-1]:
                    test_line = current_line + part + " "
                    lines.append(test_line)
                    current_line = ""
                current_line = parts[-1] + " "
            else:
                test_line = current_line + word + " "
                if self.font.size(test_line)[0] < self.width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "

        lines.append(current_line)
        return lines

    def render(self, screen, x, y):
        # Draw the red background box
        pygame.draw.rect(screen, (255, 0, 0), (x, y, self.width, self.height))
        for i, line in enumerate(self.lines):
            text_surface = self.font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (x + 10, y + i * 40 + 10))

class DialogueTreeGame:
    def __init__(self, json_file, key_to_node):
        # Load the dialogue tree from the JSON file
        with open(json_file, 'r') as f:
            self.dialogue_tree = json.load(f)
        
        # Initialize Pygame
        pygame.init()
        
        # Set up the display
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Dialogue Tree Game")
        
        # Set up fonts
        self.font = pygame.font.Font(None, 34)
        
        # Create a DialogueBox instance
        self.dialogue_box = DialogueBox(self.font, 700, 200)
        
        # Start with the "Start" node
        self.current_node = self.find_node("Start")
        
        # Key to node mapping
        self.key_to_node = key_to_node

    def find_node(self, title):
        for node in self.dialogue_tree:
            if node['title'] == title:
                return node
        return None

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            
            # Set the text of the dialogue box to the current node's body
            self.dialogue_box.set_text(self.current_node['body'])
            
            # Render the dialogue box
            self.dialogue_box.render(self.screen, 50, 50)
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif self.current_node['title'] == "End":
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    next_node_title = self.key_to_node.get(self.current_node['title'], {}).get(event.key)
                    if next_node_title:
                        self.current_node = self.find_node(next_node_title)
            
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    key_to_node = {
        "Start": {pygame.K_1: "Questions", pygame.K_2: "Questions", pygame.K_3: "Next"},
        "Questions": {pygame.K_1: "Next"},
        "Next": {pygame.K_1: "Next2", pygame.K_2: "Sorry"},
        "Sorry": {pygame.K_1: "Next2"},
        "Next2": {pygame.K_1: "Tutorial_Hello"},
        "Tutorial_Hello": {pygame.K_1: "Tutorial"},
        "Tutorial": {pygame.K_1: "Tutorial_Confusion", pygame.K_2: "Tutorial_SkillCheck", pygame.K_3: "Begin"},
        "Tutorial_SkillCheck": {pygame.K_1: "Tutorial_Again", pygame.K_2: "Begin"},
        "Tutorial_Again": {pygame.K_1: "Tutorial"},
        "Tutorial_Confusion": {pygame.K_1: "Tutorial_Again", pygame.K_2: "Begin"},
        "Begin": {pygame.K_z: "End"}
    }
    game = DialogueTreeGame('new_game.json', key_to_node)
    game.run()
