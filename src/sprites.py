import pygame
from src.config import *
import math
import random

class SpriteSheet():
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, widht, height):
        sprite = pygame.Surface([widht, height])
        sprite.blit(self.sheet, (0,0), (x, y, widht, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
        
        self.image_hitbox = pygame.image.load('img/player_hitbox.png').convert_alpha()

        self.mask = pygame.mask.from_surface(self.image_hitbox)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update(self):
        previous_x = self.rect.x
        previous_y = self.rect.y

        # Executar o movimento do jogador
        self.movement()
        self.animate()

        # Tentar mover horizontalmente, se possível
        self.rect.x += self.x_change
        if self.colisao_com_paredes_horizontal(self.game.all_sprites):
            self.rect.x = previous_x  # Reverter o movimento horizontal se houver colisão

        # Tentar mover verticalmente, se possível
        self.rect.y += self.y_change
        if self.colisao_com_paredes_vertical(self.game.all_sprites):
            self.rect.y = previous_y  # Reverter o movimento vertical se houver colisão

        # Resetar as mudanças no movimento após cada atualização
        self.x_change = 0
        self.y_change = 0

    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)]

        up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]
        
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            # for sprite in self.game.all_sprites:
            #     sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            # for sprite in self.game.all_sprites:
            #     sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            # for sprite in self.game.all_sprites:
            #     sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            # for sprite in self.game.all_sprites:
            #     sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'


    def colisao_com_paredes_horizontal(self, outros_sprites):
        for sprite in outros_sprites:
            if isinstance(sprite, Quarto):  # Verifique colisão com o fundo do quarto
                # Verifique colisões horizontais
                offset = (self.rect.x - sprite.rect.x, self.rect.y - sprite.rect.y)
                if sprite.mask.overlap(self.mask, offset):
                    return True  # Colidiu com a parede horizontalmente
        return False

    def colisao_com_paredes_vertical(self, outros_sprites):
        for sprite in outros_sprites:
            if isinstance(sprite, Quarto):  # Verifique colisão com o fundo do quarto
                # Verifique colisões verticais
                offset = (self.rect.x - sprite.rect.x, self.rect.y - sprite.rect.y)
                if sprite.mask.overlap(self.mask, offset):
                    return True  # Colidiu com a parede verticalmente
        return False


class Quarto(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x 
        self.y = y 
        self.width = ROOM_WIDHT
        self.height = ROOM_HEIGH

        self.image = pygame.image.load('img/room.png').convert_alpha()
        self.image.set_colorkey(BLUE)

        self.image_colision = pygame.image.load('img/room_colision.png').convert_alpha()
        self.image_colision.set_colorkey(BLUE)

        self.mask = pygame.mask.from_surface(self.image_colision)


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def update(self):
        # Atualiza o sprite do quarto se necessário
        pass