"""
Module for Camera Control in Pygame

This module provides a `Camera` class to handle camera movement and view adjustment 
in a Pygame-based game. It supports both automatic camera tracking of a target 
and manual movement using keyboard controls.
"""
import pygame
from settings import KEYBOARD_SPEED

class Camera:
    """
    Camera class to control the viewport in a Pygame game. The camera can follow a target
    and move according to keyboard inputs.
    """
    def __init__(self, game, width, height):
        """Initializes the Camera with game instance and screen dimensions."""
        self.game = game
        self.camera_rect = pygame.Rect(0, 0, width, height)
        self.offset = pygame.Vector2(0, 0)
        self.camera_borders = {'left': 200, 'right': 200, 'top': 200, 'bottom': 200}
        self.keyboard_speed = KEYBOARD_SPEED

    def box_target_camera(self, target):
        """Adjusts the camera's position to follow a target, ensuring the target stays within the defined borders.

        Args:
            target (pygame.sprite.Sprite): The target (typically a player) whose position the camera should follow.
        """
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
        """Allows the player to manually control the camera using the keyboard.

        Moves the camera's position based on the player's key input.
        """
        # Get the currently pressed keys
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]: self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_d]: self.camera_rect.x += self.keyboard_speed
        if keys[pygame.K_w]: self.camera_rect.y -= self.keyboard_speed
        if keys[pygame.K_s]: self.camera_rect.y += self.keyboard_speed
        
		# Update the offset to reflect the camera's new position
        self.offset.x = self.camera_rect.left
        self.offset.y = self.camera_rect.top