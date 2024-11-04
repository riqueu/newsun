"""Pause Menu Scene"""

import pygame
from src.ui.animated_sequence import load_png_sequence, sequence_current_frame

class PauseMenu:
    def __init__(self, screen: pygame.Surface) -> None:
        """Function that initializes the pause menu object scene

        Args:
            screen (pygame.Surface): the screen.
        """
        self.screen = screen
        self.font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 26)
        self.options = ["Resume", "Options", "Exit"]
        self.selected_option = 0
        self.black_bg = load_png_sequence('assets/ui/BlackBG')

    def handle_event(self, event: pygame.event.Event) -> str|None:
        """Function that handles ui interaction on the pause menu

        Args:
            event (pygame.event.Event): current event

        Returns:
            str|None: key pressed or nothing
        """
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

    def draw(self) -> None:
        """Function that draws the pause menu
        """
        #self.screen.fill((0, 0, 0))
        self.screen.blit(sequence_current_frame(self.black_bg), (0,0))
        
        keybinds = self.font.render("Z to Select | X to Cancel | Arrows to Move", True, (255, 255, 255))
        rect_keybinds = keybinds.get_rect(center=(self.screen.get_width() // 2, 500))
        self.screen.blit(keybinds, rect_keybinds)
        
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (100, 100, 100)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(self.screen.get_width() // 2, 250 + i * 50))
            self.screen.blit(text, rect)
        pygame.display.flip()
