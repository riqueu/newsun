import pygame


def draw_text_box(screen, interaction_data):
    pygame.draw.rect(screen, (255, 255, 255), (600, 50, 200, 500))  # White box on the right
    font = pygame.font.Font(None, 36)
    if "name" in interaction_data:
        name_text = font.render(interaction_data["name"], True, (0, 0, 0))
        screen.blit(name_text, (610, 60))

    dialogue_text = font.render(interaction_data["dialogue"], True, (0, 0, 0))
    screen.blit(dialogue_text, (610, 100))

    for i, option in enumerate(interaction_data["options"]):
        option_text = font.render(option["text"], True, (0, 0, 0))
        screen.blit(option_text, (610, 200 + i * 50))  # Display each option spaced vertically


def handle_input(event, interaction_data, current_option, player):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_DOWN:
            # Move to the next option
            current_option = (current_option + 1) % len(interaction_data["options"])
        elif event.key == pygame.K_UP:
            # Move to the previous option
            current_option = (current_option - 1) % len(interaction_data["options"])
        elif event.key == pygame.K_RETURN:
            # Player selects an option
            selected_option = interaction_data["options"][current_option]["action"]
            return perform_action(selected_option, player)
    return None, current_option


def perform_action(action, player):
    if action == "wash_face":
        print("You washed your face.")
        player.reduce_sanity(10)  # Example action, reducing sanity by 10
    elif action == "leave":
        print("You left the sink.")
    elif action == "look_closer":
        print("You stare deeply into the mirror.")
    return None
