"""Pause Menu Scene"""

import pygame

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 26)
        self.options = ["Resume", "Options", "Exit"]
        self.selected_option = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_z:
                return self.options[self.selected_option]
            if event.key == pygame.K_x:
                return "Resume"
        return None

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        keybinds = self.font.render("Z to Select | X to Cancel | Arrows to Move", True, (255, 255, 255))
        rect_keybinds = keybinds.get_rect(center=(self.screen.get_width() // 2, 500))
        self.screen.blit(keybinds, rect_keybinds)
        
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (100, 100, 100)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(self.screen.get_width() // 2, 250 + i * 50))
            self.screen.blit(text, rect)
        pygame.display.flip()
