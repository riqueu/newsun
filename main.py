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

        self.character_spritesheet = SpriteSheet('C:\\Users\\guguo\\OneDrive\\Área de Trabalho\\FGV\\LP\\pygame\\newsun\\img\\character.png')
        self.camera = Camera(self, WIN_WIDTH, WIN_HEIGHT)

    def draw_player(self):
        Quarto(self, (WIN_WIDTH-ROOM_WIDHT)//2, (WIN_HEIGHT-ROOM_HEIGH)//2)
        self.player = Player(self, (WIN_WIDTH-ROOM_WIDHT)//2 + 100, (WIN_HEIGHT-ROOM_HEIGH)//2 + 200)

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        # self.blocks = pygame.sprite.LayeredUpdates()
        # self.enemies = pygame.sprite.LayeredUpdates()
        # self.atacks = pygame.sprite.LayeredUpdates()

        self.draw_player()
    
    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        # game loop updates
        self.all_sprites.update()
        self.camera.box_target_camera(self.player)

    def draw(self):
        # game loop draw
        self.screen.fill((35, 14, 13))
        self.all_sprites.draw(self.screen)
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
        self.camera_borders = {'left': 100, 'right': 100, 'top': 50, 'bottom': 50}
        self.keyboard_speed = 5

    def box_target_camera(self, target):
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_d]: self.camera_rect.x += self.keyboard_speed
        if keys[pygame.K_w]: self.camera_rect.y -= self.keyboard_speed
        if keys[pygame.K_s]: self.camera_rect.y += self.keyboard_speed

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()