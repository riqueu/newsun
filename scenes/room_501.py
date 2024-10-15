import pygame

class Room501:
    def __init__(self, interactions):
        self.background = pygame.image.load("assets/images/backgrounds/room_501_background.png")
        self.interactions = interactions
        self.objects = [
            {"name": "Sink", "rect": pygame.Rect(100, 100, 50, 50)},
            {"name": "Mirror", "rect": pygame.Rect(200, 100, 50, 50)}
        ]

    def check_interaction(self, player_position):
        for obj in self.objects:
            if obj["rect"].collidepoint(player_position):
                return self.interactions.get(obj["name"], None)
        return None
    
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Space to advance dialogue
                self.current_line += 1
                if self.current_line >= len(self.dialogue_data['dialogue']):
                    self.current_line = 0  # Loop back to start (for simplicity)
                    
    def draw_background(self, screen):
        screen.blit(self.background, (0, 0))
