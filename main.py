# main.py
import pygame
import random
from pygame.locals import (
    RLEACCEL,
    QUIT,
    MOUSEBUTTONDOWN
)
from src.player import Player
from src.zombie import Zombie
from src.cloud import Cloud
from src.config import ALTURA_PULO_PERSONAGEM

pygame.init()

screen = pygame.display.set_mode([750, 500])
bg = pygame.image.load("Background.png")
bg = pygame.transform.scale(bg, (750, 500))
bg_rect = bg.get_rect()

ADDCLOUD = pygame.USEREVENT + 1
pygame.time.set_timer(ADDCLOUD, 2000)
ADDZOMBIE = pygame.USEREVENT + 2
pygame.time.set_timer(ADDZOMBIE, random.randint(3000, 5000))

player = Player()

clouds = pygame.sprite.Group()
zombies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)
button_text = font.render('Start Game', True, (0, 0, 0))
button_rect = button_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

score = 0
score_text = font.render(f'Score: {score}', True, (0, 0, 0))
score_rect = score_text.get_rect(topleft=(10, 10))

top_score = 0
with open('top_score.txt', 'r') as f:
    top_score = int(f.read())

top_score_text = font.render(f'Recorde: {top_score}', True, (0, 0, 0))
top_score_rect = top_score_text.get_rect(topleft=(10, 50))

gameRunning = False
while True:
    while not gameRunning:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                gameRunning = True

        screen.blit(bg, bg_rect)
        screen.blit(button_text, button_rect)
        screen.blit(top_score_text, top_score_rect)

        pygame.display.flip()

    score = 0  # Resetar a pontuação ao iniciar o jogo

    # Resetar os grupos de sprites
    clouds.empty()
    zombies.empty()
    all_sprites.empty()
    all_sprites.add(player)

    # Reiniciar as variáveis do jogo
    player.rect.x = 5
    player.rect.y = 350
    player.jump_speed = ALTURA_PULO_PERSONAGEM

    # Reiniciar o timer para adicionar nuvens e zumbis
    pygame.time.set_timer(ADDCLOUD, 2000)
    pygame.time.set_timer(ADDZOMBIE, random.randint(3000, 5000))

    # Reiniciar o loop do jogo
    while gameRunning:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            elif event.type == ADDCLOUD:
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)

            elif event.type == ADDZOMBIE:
                new_zombie = Zombie()
                zombies.add(new_zombie)
                all_sprites.add(new_zombie)

        clouds.update()
        zombies.update()

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        screen.blit(bg, bg_rect)

        for entity in all_sprites:
            try:
                screen.blit(entity.surf, entity.rect)
            except AttributeError:
                screen.blit(entity.curr_image, entity.rect)

        collisions = pygame.sprite.spritecollide(player, zombies, True)
        if collisions:
            player.kill()
            gameRunning = False

            # Atualizar o top score
            if score > top_score:
                top_score = score
                with open('top_score.txt', 'w') as f:
                    f.write(str(top_score))

        # Atualizar a pontuação em tempo real
        score += 1

        # Atualizar a exibição da pontuação
        score_text = font.render(f'Score: {score}', True, (255, 255, 0))
        screen.blit(score_text, score_rect)

        pygame.display.flip()
        clock.tick(30)

    # Renderizar novamente o top score fora do loop do jogo
    top_score_text = font.render(f'Recorde: {top_score}', True, (0, 0, 0))
    screen.blit(bg, bg_rect)
    screen.blit(button_text, button_rect)
    screen.blit(top_score_text, top_score_rect)
    pygame.display.flip()
