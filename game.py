import pygame
from scenes.room_101 import Room101
from ui.interaction import load_interactions
from ui.dialogue import draw_text_box, handle_input
from characters.player import Player
from settings import WIDTH, HEIGHT, FPS



def main():
    pygame.init()
    pygame.display.set_caption("Newsun")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    # Load interactions
    interactions = load_interactions('scripts/room_101.json')
    current_scene = Room101(interactions)
    player = Player()
    
    running = True
    current_option = 0
    interaction_data = None

    while running:
        screen.fill((0, 0, 0))  # Clear screen
        
        # Draw the background
        current_scene.draw_background(screen)
        
        # Update player position
        player_position = player.get_position()
        
        # Draw the player
        player.draw(screen)
        player.handle_movement()
        
        # Check for interactions
        # interaction_data = current_scene.check_interaction(player_position)

        if interaction_data:
            draw_text_box(screen, interaction_data)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if interaction_data:
                selected_option, current_option = handle_input(event, interaction_data, current_option, player)
                if selected_option:
                    print(f"Player chose: {selected_option}")  # Handle action here
            # current_scene.handle_events(event)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()


if __name__ == '__main__':
    main()
