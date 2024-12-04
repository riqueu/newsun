"""
Pause Menu Scene

This module represents the pause menu scene where the player can resume the game, access options, or exit to the main menu. 
Player interaction is handled through keyboard inputs, and the graphical interface is drawn using Pygame.
"""

import pygame
from src.ui.animated_sequence import black_bg

class PauseMenu:
    """
    This class represents the pause menu scene in the game. The player can interact with the menu to either resume
    the game, go to the options menu, or exit the game. The menu is drawn using Pygame, and the player can navigate
    between options using keyboard inputs.
    """
    def __init__(self, screen: pygame.Surface) -> None:
        """
        Initializes the PauseMenu object.

        Args:
            screen (pygame.Surface): The surface where the menu will be drawn.
        """
        self.screen = screen
        self.font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 26)
        self.options = ["Resume", "Options", "Exit"]
        self.selected_option = 0

    def handle_event(self, event: pygame.event.Event) -> str|None:
        """
        Handles keyboard events for navigating the pause menu and selecting options.

        Args:
            event (pygame.event.Event): The current event, typically from a key press.

        Returns:
            str|None: The selected option as a string (e.g., "Resume", "Options", "Exit") or None if no action is taken.
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
        """
        Draws the pause menu on the screen.

        This method renders the menu options and key instructions to the screen.
        It highlights the currently selected option and displays a set of instructions
        for the player.

        Keybinds are displayed at the bottom of the screen.
        """
        black_bg.draw(self.screen)
        black_bg.animate()
        
        keybinds = self.font.render("Z to Select | X to Cancel | Arrows to Move", True, (255, 255, 255))
        rect_keybinds = keybinds.get_rect(center=(self.screen.get_width() // 2, 500))
        self.screen.blit(keybinds, rect_keybinds)
        
        # Draw the menu options, highlighting the selected option
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (100, 100, 100)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(self.screen.get_width() // 2, 250 + i * 50))
            self.screen.blit(text, rect)
        pygame.display.flip()
