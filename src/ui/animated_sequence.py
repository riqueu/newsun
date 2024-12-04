"""
Module with Functions for Animated Sequences

This module provides utilities for loading and displaying sequences of images as animated videos 
in a Pygame application. It includes a function for loading PNG sequences and a `Video` class 
for handling animations such as dialogue boxes, skill descriptions, and more.

Classes:
    - Video: Handles playing and rendering a sequence of images as an animation.

Functions:
    - load_png_sequence: Loads a sequence of PNG images from a specified folder.
"""

import os
import pygame
WIDTH, HEIGHT = 1050, 600

def load_png_sequence(folder: str) -> list[pygame.surface.Surface]:
    """Loads a sequence of PNG images from a specified folder.

    Args:
        folder (str): Directory containing PNG files in a sequence (e.g., 'assets/animation/00001.png').

    Returns:
        list[pygame.surface.Surface]: A list of Pygame surfaces representing the images in the sequence.
    """
    sequence = []
    num_frames = len([name for name in os.listdir(folder) if name.endswith('.png')])
    for i in range(num_frames):
        sequence.append(pygame.image.load(f'{folder}/{i:05}.png').convert_alpha())
    
    return sequence


class Video():
    """Handles playback of frame-based animations from a PNG sequence.

    This class manages animations composed of a series of PNG images. It allows for 
    controlling playback, including start delay, frame delay, looping, and rendering 
    the animation at a specified position on the screen.
    """
    def __init__(self, screen: pygame.surface.Surface, x: int, y: int, folder: str, delay: int = 180, start_delay: int = 0, status: bool = False, loop: bool = False) -> None:
        """Initialize the Video object.

        Sets up a frame-based animation from a sequence of PNG images, determining 
        how it will be displayed, its speed, and whether it loops.

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
        """Updates the animation by advancing to the next frame based on the delay.

        The method checks if enough time has passed to switch to the next frame, 
        updating the animation frame counter. If the sequence ends and looping is 
        disabled, the animation stops.

        This method is responsible for controlling the frame rate and playback behavior.
        """
        if self.count >= 0:
            # Get the current time in milliseconds
            currentTime =  pygame.time.get_ticks()
            
            if currentTime - self.time > self.delay:
                self.time = currentTime
                self.count += 1 # Advances to the next frame
                
                if self.count >= len(self.sequence):
                    self.count = -self.start_delay # Restart the animation after the last frame
                    
                    if not self.loop:
                        self.status = False # Sets status to 'False' to stop the animation
        else:
            # If the animation is still waiting for the initial delay, increment the frame counter
            self.count += 1

    def draw(self, targetSurf: pygame.surface.Surface) -> None:
        """Draws the video to the target surface (screen or any other surface).
        
        Args:
            targetSurf (pygame.surface.Surface): the surface where the video will be drawn
        """
        if self.status:
            if self.count >= 0:
                # Blit (copy) the current frame from the sequence to the target surface at (x, y)
                targetSurf.blit(self.sequence[self.count], (self.x, self.y))
            else:
                # If count is less than 0 (during the initial delay), draw a blank (transparent) surface
                blank_surface = pygame.Surface(self.sequence[0].get_size(), pygame.SRCALPHA)
                blank_surface.fill((0, 0, 0, 0))  # Transparent
                targetSurf.blit(blank_surface, (self.x, self.y))
        

# Loads videos outside of the class to avoid loading them multiple times
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Calculating the position where the video will be displayed on the screen
box_x = (7 * (WIDTH - 400)) // 8
box_y = (HEIGHT - 600) // 2

# Initializing various Video objects with their respective attributes
video_in = Video(screen, box_x, box_y, 'assets/ui/DialogueBoxIn', status=True) # In animation
video = Video(screen, box_x, box_y, 'assets/ui/DialogueBox', status=True, loop=True) # Loop animation
video_out = Video(screen, box_x, box_y, 'assets/ui/DialogueBoxOut') # Out animation

# Additional animations with specific properties
vid_roll = Video(screen, 0, 0, 'assets/ui/Check', 60)
vid_pass = Video(screen, 0, 0, 'assets/ui/Pass', 60, 50)
vid_fail = Video(screen, 0, 0, 'assets/ui/Fail', 100, 50)

# Background and UI animations
black_bg = Video(screen, 0, 0, 'assets/ui/BlackBG', delay=240, status=True, loop=True)
skill_desc = Video(screen, 450, 100, 'assets/ui/SkillDesc', status=True, loop=True)
dialogue_box_left = Video(screen, 0, 0, 'assets/ui/DialogueBox', status=True, loop=True)

# UI status bar animation that loops
status_bar = Video(screen, 0, 0, 'assets/ui/StatsBar', status=True, loop=True)
