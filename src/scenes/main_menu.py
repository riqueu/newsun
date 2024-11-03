"""Main Menu Scene"""

import pygame

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.options = ["Start Game", "Options", "Exit"]
        self.selected_option = 0
        self.title_font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 52)
        self.font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 26)
        self.default_color = (255, 255, 255)

    def draw(self):
        self.screen.fill((0, 0, 0))
        # Display title and keybinds
        newsun = self.title_font.render("Newsun", True, self.default_color)
        rect_newsun = newsun.get_rect(center=(self.screen.get_width() // 2, 150))
        
        keybinds = self.font.render("Z to Select | X to Cancel | Arrows to Move", True, self.default_color)
        rect_keybinds = keybinds.get_rect(center=(self.screen.get_width() // 2, 500))
        
        self.screen.blit(newsun, rect_newsun)
        self.screen.blit(keybinds, rect_keybinds)
        
        # Select the current option
        for i, option in enumerate(self.options):
            color = self.default_color if i == self.selected_option else (100, 100, 100)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(self.screen.get_width() // 2, 250 + i * 50))
            self.screen.blit(text, rect)
        
        pygame.display.flip()

    def handle_event(self, event):
        # Menu Navigation
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_z:
                return self.options[self.selected_option]
        return None
