"""
Death Ending Scene

This module contains the `DeathMenu` class, which is used to display the death screen when the player loses the game.
It provides options for displaying the reason for the player's death and allows the player to quit the game.
"""

import pygame
from src.ui.animated_sequence import black_bg

class DeathMenu:
    """
    Class that handles the death screen when the player loses the game.
    Displays a message based on the type of death and offers the option
    to quit the game.
    """
    def __init__(self, screen: pygame.Surface, d_type: str = "") -> None:
        """
        Initializes the death menu.

        Args:
            screen (pygame.Surface): The surface where the death menu will be drawn.
            d_type (str, optional): Type of death ("health" or "reason"). Defaults to an empty string.
        """
        self.screen = screen
        self.title_font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 60)
        self.font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 20)
        self.small_font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 14)
        self.default_color = (255, 255, 255)
        self.d_type = d_type

    def update(self) -> str|None:
        """
        Updates the death menu state and checks for events.

        Returns:
            str | None: The next state of the game (e.g., "quit" if the player presses 'Q').
        """
        for event in pygame.event.get():
            result = self.handle_event(event)
            if result:
                return result
        return None

    def handle_event(self, event: pygame.event.Event) -> str|None:
        """
        Handles events in the death menu.

        Args:
            event (pygame.event.Event): The event that occurred.

        Returns:
            str | None: The action to be taken (e.g., "quit" if 'Q' is pressed).
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                return "quit"
    
    def draw(self) -> None:
        """
        Draws the death menu on the screen, including the title, death message,
        and options (such as quitting the game by pressing 'Q').
        """
        black_bg.draw(self.screen)
        black_bg.animate()
        
        # Display title
        newsun = self.title_font.render("NEWSUN", True, self.default_color)
        rect_newsun = newsun.get_rect(center=(self.screen.get_width() // 2, 150))
        
        # Display developer name
        dev_name = self.small_font.render("A Game by Artur Krause, Bruno Rosa, Gustavo Silva, Gustavo Santos, and Henrique Beltrão", True, self.default_color)
        rect_dev_name = dev_name.get_rect(center=(self.screen.get_width() // 2, 50))
        
        # Display thanks for playing
        thanks_text = self.font.render("Thanks for playing! Good luck in your next attempt.", True, self.default_color)
        rect_thanks_text = thanks_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 200))
                
        # Display options
        quit_text = self.font.render("Press 'Q' to Quit", True, self.default_color)
        rect_quit = quit_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 250))
        
        # Display lost text
        if self.d_type == "health":
            text_lines = [
            "You were never the most athletic.",
            "Your death is not a surprise,",
            "it takes strength, however,",
            "to die in such a dumb way."
            ]
        elif self.d_type == "reason":
            text_lines = [
            "A dark void fills your heart,",
            "you feel nothing. It's pointless.",
            "Darkness fills your mind and",
            "your sanity is quickly drained",
            "by the eternal worm."
            ]
        else:  # Impossible case
            text_lines = ["You lost."]

        # Render and blit each line of text
        for i, line in enumerate(text_lines):
            text = self.font.render(line, True, self.default_color)
            rect_death_text = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + (i - 1) * 30))
            self.screen.blit(text, rect_death_text)
        
        # Draw other texts
        self.screen.blit(text, rect_death_text)
        self.screen.blit(newsun, rect_newsun)
        self.screen.blit(thanks_text, rect_thanks_text)
        self.screen.blit(dev_name, rect_dev_name)
        self.screen.blit(quit_text, rect_quit)
