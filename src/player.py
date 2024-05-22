# src/player.py
import pygame
from pygame.locals import RLEACCEL, K_LEFT, K_RIGHT, K_SPACE
from src.config import ALTURA_PULO_PERSONAGEM, ACELERACAO_GRAVIDADE

class Player(pygame.sprite.Sprite):
    def load_image(self, image):
        curr_image = pygame.image.load(image)
        curr_image.set_colorkey((0, 0, 0), RLEACCEL)
        curr_image = pygame.transform.scale(curr_image, (100, 100))
        return curr_image

    def __init__(self):
        super(Player, self).__init__()
        self.images_running = []
        self.images_jumping = []

        self.ir = 0
        while self.ir < 10:
            self.ir_num = "Player/Run__00" + str(self.ir) + ".png"
            self.images_running.append(self.load_image(self.ir_num))
            self.ir = self.ir + 1

        self.ij = 0
        while self.ij < 10:
            self.ij_num = "Player/Jump__00" + str(self.ij) + ".png"
            self.images_jumping.append(self.load_image(self.ij_num))
            self.ij = self.ij + 1

        self.index_running = 0
        self.image_running = self.images_running[self.index_running]

        self.index_jumping = 0
        self.image_jumping = self.images_jumping[self.index_jumping]

        self.curr_image = self.image_running
        self.rect = pygame.Rect(5, 350, 100, 100)

        # Velocidade vertical inicial do pulo
        self.jump_speed = ALTURA_PULO_PERSONAGEM

    def update(self, pressed_keys):
        self.index_running = self.index_running + 1
        if self.index_running >= len(self.images_running):
            self.index_running = 0
        self.image_running = self.images_running[self.index_running]
        self.curr_image = self.image_running

        # Aplicar a gravidade se o jogador não estiver pulando
        if not pressed_keys[K_SPACE]:
            if self.rect.top < 350:
                self.rect.y += self.jump_speed
                # Aplicar a aceleração devida à gravidade
                self.jump_speed += ACELERACAO_GRAVIDADE
            else:
                self.rect.y = 350
                self.jump_speed = ALTURA_PULO_PERSONAGEM

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if pressed_keys[K_SPACE]:
            self.index_jumping = self.index_jumping + 1
            if self.index_jumping >= len(self.images_jumping):
                self.index_jumping = 0
            self.image_jumping = self.images_jumping[self.index_jumping]
            self.curr_image = self.image_jumping

            self.rect.move_ip(0, -ALTURA_PULO_PERSONAGEM)
        if not pressed_keys[K_SPACE]:
            if self.rect.top < 350:
                self.rect.y += self.jump_speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 750:
            self.rect.right = 750
