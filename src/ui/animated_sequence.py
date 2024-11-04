"""Module with Functions for Animated Sequences"""

import os
import pygame

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

def sequence_current_frame(sequence: list[pygame.surface.Surface], loop: bool = True) -> pygame.surface.Surface:
    """Function that gets a png sequence and returns the current frame

    Args:
        sequence (list[pygame.surface.Surface]): PNG Sequence
        loop (bool, optional): Loops or not. Defaults to True.

    Returns:
        pygame.surface.Surface: current frame
    """
    frame_duration = 200  # Duration of each frame in milliseconds
    total_duration = frame_duration * len(sequence) # Probably needed for non-loop case
    current_time = pygame.time.get_ticks()
    
    if loop:
        current_frame = sequence[current_time // frame_duration % len(sequence)]
    else:
        #TODO: Implement non-loop case if needed
        pass
    
    return current_frame