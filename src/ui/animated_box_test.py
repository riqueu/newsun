"""TEMP. TESTING FILE FOR ANIMATED DIALOGUE BOXES"""
import pygame
from pygamevideo import Video
import time

# Screen dimensions
WIDTH = 1050
HEIGHT = 600
FPS = 60

box_width = 400
box_height = 600

box_x = (7 * (WIDTH - box_width)) // 8
box_y = (HEIGHT - box_height) // 2

started = True
ended = False

pygame.init()

# print(pygame.font.Font("assets/fonts/NotoSerif-Regular.ttf", 26))
clock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT))

# in and out videos
video_in = Video("assets/ui/DialogueBoxIn.mp4")
video_out = Video("assets/ui/DialogueBoxOut.mp4")

# Load the video from the specified dir
video = Video("assets/ui/DialogueBox.mp4")

# Start the video
video.play(loop=True)

# Main loop
while True:
    # Play video_in once
    video_in.play()
    while video_in.is_playing:
        video_in.draw_to(window, (box_x, box_y))
        pygame.display.flip()

    # Play video for 5 seconds
    video.play(loop=True)
    start_time = time.time()
    while time.time() - start_time < 2:
        video.draw_to(window, (box_x, box_y))
        pygame.display.flip()

    # Play video_out once
    video_out.play()
    while video_out.is_playing:
        video_out.draw_to(window, (box_x, box_y))
        pygame.display.flip()
        
    clock.tick(FPS)
    pygame.quit()
