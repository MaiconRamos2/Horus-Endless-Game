# src/zombie.py
import pygame
from pygame.locals import RLEACCEL
import random
from src.config import VELOCIDADE_ZUMBI

class Zombie(pygame.sprite.Sprite):
    def load_image(self, image):
        curr_image_zombie = pygame.image.load(image)
        curr_image_zombie.set_colorkey((0, 0, 0), RLEACCEL)
        curr_image_zombie = pygame.transform.scale(curr_image_zombie, (100, 100))
        curr_image_zombie = pygame.transform.flip(curr_image_zombie, True, False)
        return curr_image_zombie

    def __init__(self):
        super(Zombie, self).__init__()
        self.images_walking = []
        self.iw = 1
        while self.iw < 11:
            self.iw_str = "Zombie/Walk (" + str(self.iw) + ").png"
            self.images_walking.append(self.load_image(self.iw_str))
            self.iw = self.iw + 1
        self.index_walking = 0
        self.image_walking = self.images_walking[self.index_walking]
        self.curr_image = self.image_walking
        self.rect = pygame.Rect(650, 350, 100, 100)

        # Configuração de velocidade do zumbi
        self.speed = VELOCIDADE_ZUMBI

    def update(self):
        self.index_walking = self.index_walking + 1
        if self.index_walking >= len(self.images_walking):
            self.index_walking = 0
        self.image_walking = self.images_walking[self.index_walking]
        self.curr_image = self.image_walking

        # Movimento do zumbi com base na velocidade definida
        self.rect.move_ip(-self.speed, 0)

        if self.rect.right < 0:
            self.kill()
