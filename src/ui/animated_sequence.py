"""Module with Functions for Animated Sequences"""

import os
import pygame
WIDTH, HEIGHT = 1050, 600

def load_png_sequence(folder: str) -> list[pygame.surface.Surface]:
    """Function that loads a png sequence

    Args:
        folder (str): directory with png sequence with [#####].png files

    Returns:
        list[pygame.surface.Surface]: list of png sequence
    """
    sequence = []
    num_frames = len([name for name in os.listdir(folder) if name.endswith('.png')])
    for i in range(num_frames):
        sequence.append(pygame.image.load(f'{folder}/{i:05}.png').convert_alpha())
    
    return sequence


class Video():
    def __init__(self, screen: pygame.surface.Surface, x: int, y: int, folder: str, delay: int = 180, start_delay: int = 0, status: bool = False, loop: bool = False) -> None:
        """Initialize Video Object

        Args:
            screen (pygame.surface.Surface): screen where the video will be drawn
            x (int): x location of the video
            y (int): y location of the video
            folder (str): directory with png sequence with [#####].png files
            delay (int, optional): Delay between each frame, i.e. animation speed. Defaults to 180.
            start_delay (int, optional): Delay to start the animation. Defaults to 0.
            status (bool, optional): If its playing or not. Defaults to False.
            loop (bool, optional): Whether it loops or not. Defaults to False.
        """        
        self.screen = screen
        self.x, self.y = x, y
        self.sequence = load_png_sequence(folder)
        self.start_delay = start_delay # Delay before starting the animation
        self.count = -start_delay # Frame Counter, blank for start_delay frames
        self.delay = delay # Animation Speed
        self.time = 0
        self.status = status
        self.loop = loop
    
    def animate(self) -> None:
        """Animates the video
        """
        if self.count >= 0:
            currentTime =  pygame.time.get_ticks()
            if currentTime - self.time > self.delay:
                self.time = currentTime
                self.count += 1
                if self.count >= len(self.sequence):
                    self.count = -self.start_delay
                    if not self.loop:
                        self.status = False # Animation ends
        else:
            self.count += 1

    def draw(self, targetSurf: pygame.surface.Surface) -> None:
        """Draws the video

        Args:
            targetSurf (pygame.surface.Surface): the surface where the video will be drawn
        """
        if self.status:
            if self.count >= 0:
                targetSurf.blit(self.sequence[self.count], (self.x, self.y))
            else:
                blank_surface = pygame.Surface(self.sequence[0].get_size(), pygame.SRCALPHA)
                blank_surface.fill((0, 0, 0, 0))  # Transparent
                targetSurf.blit(blank_surface, (self.x, self.y))
        

# Loads videos outside of the class to avoid loading them multiple times
screen = pygame.display.set_mode((WIDTH, HEIGHT))
box_x = (7 * (WIDTH - 400)) // 8
box_y = (HEIGHT - 600) // 2

video_in = Video(screen, box_x, box_y, 'assets/ui/DialogueBoxIn', status=True) # In animation
video = Video(screen, box_x, box_y, 'assets/ui/DialogueBox', status=True, loop=True) # Loop animation
video_out = Video(screen, box_x, box_y, 'assets/ui/DialogueBoxOut') # Out animation
        
vid_roll = Video(screen, 0, 0, 'assets/ui/Check', 60)
vid_pass = Video(screen, 0, 0, 'assets/ui/Pass', 60, 50)
vid_fail = Video(screen, 0, 0, 'assets/ui/Fail', 100, 50)

black_bg = Video(screen, 0, 0, 'assets/ui/BlackBG', delay=240, status=True, loop=True)

skill_desc = Video(screen, 450, 100, 'assets/ui/SkillDesc', status=True, loop=True)
dialogue_box_left = Video(screen, 0, 0, 'assets/ui/DialogueBox', status=True, loop=True)

status_bar = Video(screen, 0, 0, 'assets/ui/StatsBar', status=True, loop=True)
