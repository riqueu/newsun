"""Options Menu Scene"""

import pygame
from src.ui.animated_sequence import black_bg

class OptionsMenu:
    """
    A class representing the 'Options Menu' scene, allowing the player to modify settings such as volume 
    and navigate back to the previous screen.
    """
    def __init__(self, screen: pygame.Surface) -> None:
        """
        Initializes the OptionsMenu scene, setting up the options and initial volume level.

        Args:
            screen (pygame.Surface): The surface where the game is rendered.
        """
        self.screen = screen
        self.font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 26)
        self.volume = 0.3  # Initial volume level (30%)
        self.options = ["Volume", "Back"]
        self.selected_option = 0  # Initially, "Volume" is selected
        self.previous_screen = None

    def handle_event(self, event: pygame.event.Event) -> str|None:
        """
        Handles user input events during the options menu. This includes navigating between menu options 
        and adjusting the volume.

        Args:
            event (pygame.event.Event): The pygame event to handle.

        Returns:
            str|None: A string representing the action taken, such as "Back", or None if no action occurred.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Move selection up
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                # Move selection down
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_LEFT and self.selected_option == 0:
                # Decrease volume when "Volume" option is selected
                self.volume = max(0.0, self.volume - 0.1)  # Decrease volume
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.Channel(0).set_volume(self.volume)
                pygame.mixer.Channel(1).set_volume(self.volume)
            elif event.key == pygame.K_RIGHT and self.selected_option == 0:
                # Increase volume when "Volume" option is selected
                self.volume = min(1.0, self.volume + 0.1)  # Increase volume
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.Channel(0).set_volume(self.volume)
                pygame.mixer.Channel(1).set_volume(self.volume)
            elif event.key == pygame.K_z:
                # Return to the previous screen if "Back" is selected
                if self.options[self.selected_option] == "Back":
                    return "Back"
            elif event.key == pygame.K_x:
                # Also return to the previous screen when 'X' is pressed
                return "Back"
        return None

    def draw(self) -> None:
        """
        Draws the options menu to the screen, including the volume slider and available menu options.
        """
        black_bg.draw(self.screen)
        black_bg.animate()
        
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (100, 100, 100)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(self.screen.get_width() // 2, 250 + i * 50))
            self.screen.blit(text, rect)
            
        # Draw volume slider if "Volume" is selected
        if self.selected_option == 0:
            slider_x = self.screen.get_width() // 2
            slider_y = 350
            slider_width = 200
            slider_height = 10
            pygame.draw.rect(self.screen, (255, 255, 255), (slider_x - slider_width // 2, slider_y, slider_width, slider_height))
            handle_x = slider_x - slider_width // 2 + int(self.volume * slider_width)
            handle_y = slider_y - 5
            handle_width = 10
            handle_height = 20
            pygame.draw.rect(self.screen, (162, 0, 220), (handle_x, handle_y, handle_width, handle_height))
            
        # Update the volume option text
        self.options[0] = f"Volume: {int(self.volume * 100)}%"
