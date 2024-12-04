"""
This module contains the `EndingMenu` class, which is responsible for displaying 
the final screen of the game after the player completes it. The screen includes 
the game title, a thank you message, developer credits, and an option to quit 
the game. The user can quit by pressing the 'Q' key.
"""


import pygame
from src.ui.animated_sequence import black_bg

class EndingMenu:
    """
    Class that handles the game’s ending screen.
    Displays the game title, developer credits, and a thank-you message.
    Offers the option to quit the game.
    """
    def __init__(self, screen: pygame.Surface) -> None:
        """
        Initializes the ending menu.

        Args:
            screen (pygame.Surface): The surface where the ending menu will be drawn.
        """
        self.screen = screen
        self.title_font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 60)
        self.font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 20)
        self.small_font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 14)
        self.default_color = (255, 255, 255)

    def update(self) -> str|None:
        """
        Updates the state of the ending menu.

        Returns:
            str|None: 
                - Returns "quit" if the player presses the 'Q' key to exit the game.
                - Returns None if no relevant input is detected.
        """
        for event in pygame.event.get():
            result = self.handle_event(event)
            if result:
                return result
        return None

    def handle_event(self, event: pygame.event.Event) -> str|None:
        """
        Handles user interaction events for the ending menu.

        Args:
            event (pygame.event.Event): The event object representing the current user input.

        Returns:
            str|None: 
                - Returns "quit" if the player presses the 'Q' key to exit the game.
                - Returns None if no relevant key is pressed or if the event is not related to quitting.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                return "quit"
    
    def draw(self) -> None:
        """
        Renders the ending menu on the screen.

        This method draws the final elements of the game on the screen, including the title, 
        developer names, a thank you message, and the option to quit. It also handles background 
        animations.

        The background is animated using `black_bg` and redrawn each time this method is called.
        """
        black_bg.draw(self.screen)
        black_bg.animate()
        
        # Display title
        newsun = self.title_font.render("NEWSUN", True, self.default_color)
        rect_newsun = newsun.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        
        self.screen.blit(newsun, rect_newsun)
        
        # Display developer name
        dev_name = self.small_font.render("A Game by Artur Krause, Bruno Rosa, Gustavo Silva, Gustavo Santos, and Henrique Beltrão", True, self.default_color)
        rect_dev_name = dev_name.get_rect(center=(self.screen.get_width() // 2, 50))
        
        # Display thanks for playing
        thanks_text = self.font.render("Thanks for playing!", True, self.default_color)
        rect_thanks_text = thanks_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))
        
        self.screen.blit(thanks_text, rect_thanks_text)
        self.screen.blit(dev_name, rect_dev_name)
        
        # Display options
        quit_text = self.font.render("Press 'Q' to Quit", True, self.default_color)
        rect_quit = quit_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 250))
        self.screen.blit(quit_text, rect_quit)
