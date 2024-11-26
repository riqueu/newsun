import pygame
from src.config import *
import math
import random

class SpriteSheet():
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, widht, height):
        sprite = pygame.Surface([widht, height])
        sprite.blit(self.sheet, (0,0), (x*widht, y*height, widht, height))
        sprite.set_colorkey(BLUE)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = 48
        self.height = 72

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(1, 0, self.width, self.height)
        
        self.image_hitbox = pygame.image.load('./img/player_hitbox.png').convert_alpha()

        self.mask = pygame.mask.from_surface(self.image_hitbox)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.door_side = "top"
    
    def update(self):
        previous_x = self.rect.x
        previous_y = self.rect.y

        # Executar o movimento do jogador
        self.movement()
        self.animate()

        # Tentar mover horizontalmente, se possível
        self.rect.x += self.x_change
        if self.colisao_com_paredes(self.game.all_sprites):
            self.rect.x = previous_x  # Reverter o movimento horizontal se houver colisão

        # Tentar mover verticalmente, se possível
        self.rect.y += self.y_change
        if self.colisao_com_paredes(self.game.all_sprites):
            self.rect.y = previous_y  # Reverter o movimento vertical se houver colisão

        # Resetar as mudanças no movimento após cada atualização
        self.x_change = 0
        self.y_change = 0

    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(1, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(2, 0, self.width, self.height)]

        up_animations = [self.game.character_spritesheet.get_sprite(1, 3, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(0, 3, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(2, 3, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(1, 1, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(0, 1, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(2, 1, self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite(1, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(0, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(2, 2, self.width, self.height)]
        
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 0, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 3, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 1, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 2, self.width, self.height)
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


    def colisao_com_paredes(self, outros_sprites):
        for sprite in outros_sprites:
            if not isinstance(sprite, Player):  # Verifique colisão com o fundo do quarto
                # Verifique colisões
                offset = (self.rect.x - sprite.rect.x, self.rect.y - sprite.rect.y)
                if sprite.mask.overlap(self.mask, offset):
                    return True  # Colidiu com a parede horizontalmente
        return False


class Room(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x 
        self.y = y 
        self.width = ROOM_WIDHT
        self.height = ROOM_HEIGHT

        self.image = pygame.image.load('./img/room_full.png').convert_alpha()
        self.image.set_colorkey(BLUE)

        self.image_colision = pygame.image.load('./img/room_colision.png').convert_alpha()
        self.image_colision.set_colorkey(BLUE)

        self.mask = pygame.mask.from_surface(self.image_colision)


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def update(self):
        # Atualiza o sprite do quarto se necessário
        pass

class Hall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x 
        self.y = y 
        self.width =  HALL_WIDHT # Largura do corredor
        self.height = HALL_HEIGHT  # Altura do corredor

        self.image = pygame.image.load('./img/hall_full.png').convert_alpha()
        self.image.set_colorkey(BLUE)

        self.image_colision = pygame.image.load('./img/hall_colision.png').convert_alpha()
        self.image_colision.set_colorkey(BLUE)

        self.mask = pygame.mask.from_surface(self.image_colision)


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def update(self):
        # Atualiza o sprite do corredor se necessário
        pass

class RoomDoor(pygame.sprite.Sprite):
    def __init__(self, game, room, destination_direction):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((54, 9))
        self.image.fill((255, 255, 0))  # Cor amarela para visualização da porta
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.Mask(self.image.get_size(), fill=False)

        # Posicionando a porta no lado inferior do quarto
        self.rect.topleft = (room.rect.topleft[0] + 688, room.rect.topleft[1] + 400)

        self.destination_side = destination_direction  # Direção para o outro lado da porta (ex: "esquerda" ou "direita")

    def interact_with_door(self):
        if self.game.player.door_side == "top":
            # Posiciona o jogador abaixo da porta e altera o estado para "bottom"
            self.game.player.rect.x = self.rect.centerx - self.game.player.rect.width // 2  # Centraliza o jogador na porta
            self.game.player.rect.y = self.rect.bottom + 10  # Coloca o jogador logo abaixo da porta
            self.game.player.door_side = "bottom"  # Muda o estado do jogador para "bottom"

            # Cria e desenha o Hall
            self.game.hall = Hall(self.game, self.game.room.rect.topleft[0], self.game.room.rect.topleft[1] + 220)  # Coloca o Hall abaixo do Room
            self.game.all_sprites.add(self.game.hall)  # Adiciona o novo ambiente (Hall) aos sprites

            # Muda o quarto atual de Room para Hall
            if hasattr(self.game, 'room'):  # Verifica se a Room ainda existe
                self.game.all_sprites.remove(self.game.room)  # Remove o quarto atual
                self.game.room = None  # Limpa a referência à sala atual


        elif self.game.player.door_side == "bottom":
            # Posiciona o jogador acima da porta e altera o estado para "top"
            self.game.player.rect.x = self.rect.centerx - self.game.player.rect.width // 2  # Centraliza o jogador na porta
            self.game.player.rect.y = self.rect.top - self.game.player.rect.height - 10  # Coloca o jogador logo acima da porta
            self.game.player.door_side = "top"  # Muda o estado do jogador para "top"

            # Muda de volta para o Room
            if hasattr(self.game, 'hall'):  # Verifica se o Hall existe
                self.game.all_sprites.remove(self.game.hall)  # Remove o corredor
                self.game.hall = None  # Limpa a referência ao corredor

            # Cria e desenha o Room
            self.game.room = Room(self.game, (WIN_WIDTH - ROOM_WIDHT) // 2, (WIN_HEIGHT - ROOM_HEIGHT) // 2)
            self.game.all_sprites.add(self.game.room)  # Adiciona o novo ambiente (Room) aos sprites

    def update(self):
        # Aqui podemos atualizar algo relacionado à porta, se necessário
        pass
