import pygame
from settings import KEYBOARD_SPEED

class Camera:
    def __init__(self, game, width, height):
        self.game = game
        self.camera_rect = pygame.Rect(0, 0, width, height)
        self.offset = pygame.Vector2(0, 0)
        self.camera_borders = {'left': 200, 'right': 200, 'top': 200, 'bottom': 200}
        self.keyboard_speed = KEYBOARD_SPEED

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