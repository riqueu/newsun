"""
Main Menu Scene

This module contains the implementation of the main menu scene for the game. The main menu is the initial
screen presented to the player, where they can choose between different options such as "Start Game",
"Options", and "Exit". It also handles the navigation and selection of these options via keyboard input.
"""

import pygame
from src.ui.animated_sequence import black_bg

class MainMenu:
    """
    Main Menu Scene for the game.

    The `MainMenu` class represents the main menu screen where the player can choose from various options such as 
    "Start Game", "Options", and "Exit". The menu allows the player to navigate through these options using 
    the arrow keys and confirm the selection with the "Z" key.
    """
    def __init__(self, screen: pygame.Surface) -> None:
        """
        Initializes the MainMenu object.

        Args:
            screen (pygame.Surface): The screen where the menu will be displayed.
        """
        self.screen = screen
        self.options = ["Start Game", "Options", "Exit"]
        self.selected_option = 0
        self.title_font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 52)
        self.font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 26)
        self.default_color = (255, 255, 255)

    def draw(self) -> None:
        """
        Draws the main menu screen on the given surface (screen).

        This method renders the menu title, instructions for keybindings, and the list of options. The selected 
        option is highlighted. It also handles drawing the background animation using `black_bg`.
        """
        black_bg.draw(self.screen)
        black_bg.animate()
        
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

    def handle_event(self, event: pygame.event.Event) -> str|None:
        """
        Handles the events for navigating and selecting options in the main menu.

        Args:
            event (pygame.event.Event): The event to handle (e.g., keyboard input).

        Returns:
            str | None: The selected option as a string if a key is pressed, otherwise None.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_z:
                return self.options[self.selected_option]
        return None
