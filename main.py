import pygame
from src.config import *
from src.sprites import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_spritesheet = SpriteSheet('./img/characters/characters.png')
        self.camera = Camera(self, WIN_WIDTH, WIN_HEIGHT)
    
    def draw_player(self):
        self.player = Player(self, (WIN_WIDTH-ROOM_WIDHT)//2 + 120, (WIN_HEIGHT-ROOM_HEIGHT)//2 + 240)


    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.Group()

        self.room = Room(self, (WIN_WIDTH-ROOM_WIDHT)//2, (WIN_HEIGHT-ROOM_HEIGHT)//2)
        self.room_door = RoomDoor(self, self.room, 'down')
        self.all_sprites.add(self.room)
        self.doors.add(self.room_door)
        self.all_sprites.add(self.room_door)

        self.draw_player()
    
    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    # Verifica se o jogador está perto de alguma porta
                    for door in self.doors:
                        if door.rect.colliderect(self.player.rect):  # Verifica se o jogador está dentro do alcance da porta
                            door.interact_with_door()
            
    def update(self):
        # game loop updates
        self.all_sprites.update()
        self.camera.box_target_camera(self.player)
        self.camera.keyboard_control()

    def draw(self):
        # game loop draw
        self.screen.fill((35, 14, 13))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect.topleft - self.camera.offset)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        # game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        pass

class Camera:
    def __init__(self, game, width, height):
        self.game = game
        self.camera_rect = pygame.Rect(0, 0, width, height)
        self.offset = pygame.Vector2(0, 0)
        self.camera_borders = {'left': 200, 'right': 200, 'top': 300, 'bottom': 300}
        self.keyboard_speed = 5

    def box_target_camera(self, target):
        if target.rect.left < self.camera_rect.left + self.camera_borders['left']:
            self.camera_rect.left = target.rect.left - self.camera_borders['left']

        # Verificar se o jogador ultrapassou a borda direita da tela
        if target.rect.right > self.camera_rect.right - self.camera_borders['right']:
            self.camera_rect.right = target.rect.right + self.camera_borders['right']

        # Verificar se o jogador ultrapassou a borda superior da tela
        if target.rect.top < self.camera_rect.top + self.camera_borders['top']:
            self.camera_rect.top = target.rect.top - self.camera_borders['top']

        # Verificar se o jogador ultrapassou a borda inferior da tela
        if target.rect.bottom > self.camera_rect.bottom - self.camera_borders['bottom']:
            self.camera_rect.bottom = target.rect.bottom + self.camera_borders['bottom']

        # Atualiza o deslocamento da câmera para o movimento da tela
        self.offset.x = self.camera_rect.left 
        self.offset.y = self.camera_rect.top

    def keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_d]: self.camera_rect.x += self.keyboard_speed
        if keys[pygame.K_w]: self.camera_rect.y -= self.keyboard_speed
        if keys[pygame.K_s]: self.camera_rect.y += self.keyboard_speed

        self.offset.x = self.camera_rect.left
        self.offset.y = self.camera_rect.top

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()