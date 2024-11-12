import pygame
import sys
import random
import json


# Inicialização
pygame.init()
screen_width, screen_height = 900, 500
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Game
COLLISION = True

# Jogador
player_size = 50
player_color = (255, 0, 0)
player_pos = [screen_width // 2, screen_height // 2]  # Começa no centro da tela
speed = 1.5
player_word = [800,400]

# Read json maps
with open('mapas.json', 'r') as arquivo:
	mapas = json.load(arquivo)
	
# player
player_import = pygame.image.load("player.png")
palyer = pygame.transform.scale(player_import, (player_size, player_size))
# mapa
background_import = pygame.image.load(mapas["quarto"]["img"])
background = pygame.transform.scale(background_import, (900, 500))

# # Função de detecção de colisão
def check_collision(player_rect, obstacles):
	for obstacle in obstacles:
		if player_rect.colliderect(obstacle["rect"]):
			return True
	return False

# Função para adicionar obstáculos
def add_square(position, dimension):
	return pygame.Rect(position["x"], position["y"], dimension[0], dimension[1])

quarto_obstacles = mapas["quarto"]["obstacles"]

# Adiciona obstáculos a partir do JSON
obstacles = []

for obstacles_type in quarto_obstacles:
	print("obstacles_type: ", obstacles_type)
	for obstacle in quarto_obstacles[obstacles_type]:
		print("obstacle: ", obstacle)
		rect = add_square(obstacle["position"], (obstacle["width"], obstacle["height"]))
		
		obs = {
			"type": obstacles_type,
			"rect": rect,
		}

		if "border_radius" in obstacle:
			obs["border_radius"] = obstacle["border_radius"]

		obstacles.append(obs)

# Loop principal
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()	

	# Controle do Jogador
	keys = pygame.key.get_pressed()
	player_movement = [0, 0]

	if keys[pygame.K_LEFT]:
		player_movement[0] -= speed
	if keys[pygame.K_RIGHT]:
		player_movement[0] += speed
	if keys[pygame.K_UP]:
		player_movement[1] -= speed
	if keys[pygame.K_DOWN]:
		player_movement[1] += speed

	# Calcular nova posição do jogador no mundo
	player_word_test = [player_word[0] + player_movement[0], player_word[1] + player_movement[1]]
	player_rect_test = pygame.Rect(player_word_test[0]+7, player_word_test[1]+32, player_size-20, player_size-30)

	
	# Verificar colisão
	if check_collision(player_rect_test, obstacles):
		continue
	
	# Seta a nova posição do jogador no mundo
	player_word = [player_word[0] + player_movement[0], player_word[1] + player_movement[1]]

	# Desenhar retângulo ao redor do jogador para mostrar a área de colisão
	player_rect = pygame.Rect(player_word[0], player_word[1], player_size, player_size)
	pygame.draw.rect(screen, (0, 0, 255), player_rect, 2)  # Borda azul ao redor do jogador

	# Limpar a tela
	# screen.fill(mapas.quarto.src)  # Verde para o fundo
	screen.blit(background, (0,0))
		
	screen.blit(palyer, player_word)
	
	if COLLISION:
		for obstacle in obstacles:
			# print(obstacle)
			if obstacle["type"] == "wall":
				if "border_radius" in obstacle:
					pygame.draw.rect(screen, (255, 0, 0), obstacle["rect"], 3, border_radius=obstacle["border_radius"])
				else:
					pygame.draw.rect(screen, (255, 0, 0), obstacle["rect"], 3)
				
			elif obstacle["type"] == "object":
				pygame.draw.rect(screen, (255, 255, 0), obstacle["rect"], 3, border_radius=5)

		pygame.draw.rect(screen, player_color, player_rect_test, 1, border_radius=10)


	# Atualizar a tela
	pygame.display.flip()
	clock.tick(60)  # 60 FPS