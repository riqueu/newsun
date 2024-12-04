"""Game Ending Scene"""

import pygame
from src.ui.animated_sequence import black_bg

class EndingMenu:
    def __init__(self, screen: pygame.Surface) -> None:
        """Initializes the EndingMenu object

        Args:
            screen (pygame.Surface): The screen.
        """
        self.screen = screen
        self.title_font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 60)
        self.font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 20)
        self.small_font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 14)
        self.default_color = (255, 255, 255)

    def update(self) -> str|None:
        """Function to update the ending menu state

        Returns:
            str|None: the next state of the game
        """
        for event in pygame.event.get():
            result = self.handle_event(event)
            if result:
                return result
        return None

    def handle_event(self, event: pygame.event.Event) -> str|None:
        """Function that handles menu interaction

        Args:
            event (pygame.event.Event): current event

        Returns:
            str|None: key pressed or nothing if no key is pressed
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                return "quit"
    
    def draw(self) -> None:
        """Functions that draws the ending menu
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
