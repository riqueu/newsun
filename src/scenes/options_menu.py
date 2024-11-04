"""Options Menu Scene"""

import pygame
from src.ui.animated_sequence import load_png_sequence, sequence_current_frame

class OptionsMenu:
    def __init__(self, screen: pygame.Surface) -> None:
        """Function that initializes the options menu object scene

        Args:
            screen (pygame.Surface): the screen.
        """
        self.screen = screen
        self.font = pygame.font.Font("assets/fonts/Helvetica-Bold.ttf", 26)
        self.volume = 0.5  # Initial volume level (50%)
        self.options = ["Volume", "Back"]
        self.selected_option = 0
        self.previous_screen = None
        self.black_bg = load_png_sequence('assets/ui/BlackBG')
        

    def handle_event(self, event: pygame.event.Event) -> str|None:
        """Function that handles the menu interaction

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
            elif event.key == pygame.K_LEFT and self.selected_option == 0:
                self.volume = max(0.0, self.volume - 0.1)  # Decrease volume
                pygame.mixer.music.set_volume(self.volume)
            elif event.key == pygame.K_RIGHT and self.selected_option == 0:
                self.volume = min(1.0, self.volume + 0.1)  # Increase volume
                pygame.mixer.music.set_volume(self.volume)
            elif event.key == pygame.K_z:
                if self.options[self.selected_option] == "Back":
                    return "Back"
            elif event.key == pygame.K_x:
                return "Back"
        return None

    def draw(self) -> None:
        """Function that draws the options menu
        """
        #self.screen.fill((0, 0, 0))
        self.screen.blit(sequence_current_frame(self.black_bg), (0,0))
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

        pygame.display.flip()