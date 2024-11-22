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

class Video():
    def __init__(self, screen: pygame.surface.Surface, x: int, y: int, folder: str, delay: int = 180) -> None:
        """Initialize the Video object.

        Args:
            screen (pygame.surface.Surface): screen where the video will be drawn
            x (int): location of the video
            y (int): location of the video
            folder (str): directory with png sequence with [#####].png files
            delay (int, optional): Delay between each frame, i.e. animation speed. Defaults to 180.
        """
        self.screen = screen
        self.x, self.y = x, y
        self.sequence = load_png_sequence(folder)
        self.count = 0
        self.delay = delay # Animation Speed
        self.time = 0
    
    def animate(self) -> None:
        """Animates the video
        """
        currentTime =  pygame.time.get_ticks()
        if currentTime - self.time > self.delay:
            self.time = currentTime
            self.count += 1
            if self.count >= len(self.sequence):
                self.count = 0

    def draw(self, targetSurf: pygame.surface.Surface) -> None:
        """Draws the video

        Args:
            targetSurf (pygame.surface.Surface): the surface where the video will be drawn
        """
        targetSurf.blit(self.sequence[self.count], (self.x, self.y))
        

# Testing the Video class
if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((1050, 600))
    video = Video(screen, 0, 0, 'assets/ui/DialogueBox')
    video_in = Video(screen, 0, 0, 'assets/ui/DialogueBoxIn')
    video_out = Video(screen, 0, 0, 'assets/ui/DialogueBoxOut')
    
    roll_vid = Video(screen, 0, 0, 'assets/ui/Check', 50)
    pass_vid = Video(screen, 0, 0, 'assets/ui/Pass', 30)
    fail_vid = Video(screen, 0, 0, 'assets/ui/Fail', 50)
    
    in_played = False
    out_status = False
    
    running = True
    start_time = pygame.time.get_ticks()
    while running:
        screen.fill((0, 0, 0))
        
        if out_status:
            video_out.animate()
            if video_out.count == len(video_out.sequence) - 1:
                out_status = False
                pygame.time.delay(100)
                # video_in.count = 0
                in_played = False
                #pygame.time.delay(1000)
                #running = False
            video_out.draw(screen)
        elif not in_played:
            video_in.animate()
            if video_in.count == len(video_in.sequence) - 1:
                in_played = True
            video_in.draw(screen)
        else:
            video.animate()
            video.draw(screen)
        
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
        
        if roll_vid.count > 0:
            roll_vid.animate()
            roll_vid.draw(screen)
        if pass_vid.count > 0:
            pass_vid.animate()
            pass_vid.draw(screen)
        if fail_vid.count > 0:
            fail_vid.animate()
            fail_vid.draw(screen)
            
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    out_status = True
                    video_out.count = 0
                
                if event.key == pygame.K_c:
                    roll_vid.count = 1
                    
                if event.key == pygame.K_v:
                    pass_vid.count = 1
                    
                if event.key == pygame.K_b:
                    fail_vid.count = 1
                    
        clock.tick(60)
    pygame.quit()