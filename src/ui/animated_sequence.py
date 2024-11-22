"""Module with Functions for Animated Sequences"""

import os
import pygame
from settings import WIDTH, HEIGHT

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
        # TODO: Implement delay before starting animation
        
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

        
vid_roll = Video(screen, 0, 0, 'assets/ui/Check', 50)
vid_pass = Video(screen, 0, 0, 'assets/ui/Pass', 30, 50)
vid_fail = Video(screen, 0, 0, 'assets/ui/Fail', 50, 50)

black_bg = Video(screen, 0, 0, 'assets/ui/BlackBG', status=True, loop=True)

skill_desc = Video(screen, 450, 100, 'assets/ui/SkillDesc', status=True, loop=True)
dialogue_box_left = Video(screen, 0, 0, 'assets/ui/DialogueBox', status=True, loop=True)

# Testing the Video class
if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((1050, 600))
    video = Video(screen, 0, 0, 'assets/ui/DialogueBox', status=True, loop=True)
    video_in = Video(screen, 0, 0, 'assets/ui/DialogueBoxIn', status=True)
    video_out = Video(screen, 0, 0, 'assets/ui/DialogueBoxOut')
    
    roll_vid = Video(screen, 0, 0, 'assets/ui/Check', 50)
    pass_vid = Video(screen, 0, 0, 'assets/ui/Pass', 30, 50)
    fail_vid = Video(screen, 0, 0, 'assets/ui/Fail', 50, 50)
    
    running = True
    start_time = pygame.time.get_ticks()
    while running:
        screen.fill((0, 0, 0))
        
        if video_out.status:
            video_out.draw(screen)
            video_out.animate()
            if video_out.count == len(video_out.sequence) - 1:

                video_in.status = True

        elif video_in.status:
            video_in.draw(screen)

        else:
            video.draw(screen)
            video.animate()
        
        lines = ["Lorem ipsum dolor sit amet,", "amet odio. Nullam nec nisl ", "libero lacinia ultricies. Nullam", "libero lacinia ultricies.", "nec libero lacinia ultricies."]
        
        # Animate text scrolling
        font = pygame.font.Font(None, 36)
        text_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        text_surface.fill((0, 0, 0, 0))
        
        text_speed = 10  # Adjust this value to change text speed (lower is faster)
        elapsed_time = pygame.time.get_ticks() - start_time
        total_chars = sum(len(line) for line in lines)
        max_chars = min((pygame.time.get_ticks() - start_time) // text_speed, total_chars)
        current_chars = 0
        
        for line in lines:
            if current_chars + len(line) < max_chars:
                rendered_line = font.render(line, True, (255, 255, 255))
                text_surface.blit(rendered_line, (20, 50 + lines.index(line) * 40))
                current_chars += len(line)
            else:
                rendered_line = font.render(line[:max_chars - current_chars], True, (255, 255, 255))
                text_surface.blit(rendered_line, (20, 50 + lines.index(line) * 40))
                break
        
        screen.blit(text_surface, (0, 0))
        
        if roll_vid.status:
            roll_vid.draw(screen)
            roll_vid.animate()
        if pass_vid.status:
            pass_vid.draw(screen)
            pass_vid.animate()
        if fail_vid.status:
            fail_vid.draw(screen)
            fail_vid.animate()
            
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    video_out.status = True
                
                if event.key == pygame.K_c:
                    roll_vid.status = True
                    
                if event.key == pygame.K_v:
                    pass_vid.status = True
                    
                if event.key == pygame.K_b:
                    fail_vid.status = True
                    
        clock.tick(60)
    pygame.quit()