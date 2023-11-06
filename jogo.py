
import pygame
import sys
import math
import random
from pygame.locals import *

# Inicialize o Pygame
pygame.init()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
red = (255, 0, 0)

# BOLA ou tiro

BALL_COLOR = (0, 0, 255)
SHOOT_DELAY = 1000  # cooldown dos tiros (2 segundos)
BigSHOOT_DELAY = 10000 # cooldown dos tiros especiais(10 segundos)
# Tamanho da janela
WIDTH, HEIGHT = 800, 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_rect = screen.get_rect()

#Cenarios
bg3 = pygame.image.load("CENARIO3.jpeg")

# Fonte e tamanho
font = pygame.font.Font(None, 36)

# Variaveis de mouse 
mouse_x, mouse_y = 0, 0

#personagem BOB

class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("hero.png")
        self.rect = self.image.get_rect()
        self.rect.center = (800 // 2, 200)
        self.angle = 0
        self.last_shot_time = 0

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.angle = math.atan2(mouse_y - self.rect.centery, mouse_x - self.rect.centerx)
        
        # Verificar se o personagem pode atirar novamente
        current_time = pygame.time.get_ticks()
        if pygame.mouse.get_pressed()[0] and current_time - self.last_shot_time >= SHOOT_DELAY:
            self.shoot()
            self.last_shot_time = current_time
  
    def shoot(self):
        bball  = Ball(self.rect.centerx, self.rect.centery, self.angle)
        Gsprites.add(bball)

    def EspecialShoot(self):
        ball  = BigBall(self.rect.centerx, self.rect.centery, self.angle)
        Gsprites.add(ball)

#TIRO

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(BALL_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.angle = angle

    def update(self):
        self.rect.x += 16 * math.cos(self.angle)
        self.rect.y += 16 * math.sin(self.angle)

class BigBall(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((160, 40))
        self.image.fill(BALL_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.angle = angle

    def update(self):
        self.rect.x += 12 * math.cos(self.angle)
        self.rect.y += 12 * math.sin(self.angle)





#Insanciando e colocando em grupo
bob = Character()

Gsprites = pygame.sprite.Group()
Gsprites.add(bob)


# Opões do menu


ti_text = font.render("VULCANO", True, WHITE)
ti_rect = ti_text.get_rect()
ti_rect.center = (WIDTH // 2, 200)


play_text = font.render("Jogar", True, BLACK)
play_rect = play_text.get_rect()
play_rect.center = (800 // 2, 300)

sound_text = font.render("Som", True, WHITE)
sound_rect = sound_text.get_rect()
sound_rect.center = (800 // 2, 400)

score_text = font.render("Placar", True, WHITE)
score_rect = score_text.get_rect()
score_rect.center = (800 // 2, 500)


def jogo():

#Variavel de movimento
    move_up = False
    move_down = False 
    move_left = False
    move_right = False

    #tiro especial
    Biglast_shot_time = 0


#LOOP JOGO
    clock = pygame.time.Clock()
    running = True
    while running:
        
        pygame.display.update()
        pygame.display.set_caption("GAME")
        screen.fill(WHITE)
        screen.blit(bg3, (0, 0))
        
        Gsprites.update()
       
        Gsprites.draw(screen)

        current_timeE = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_w:
                    move_up = True
                    print("w")
                if event.key == K_s:
                    move_down = True
                    print("s")
                if event.key == K_a:
                    move_left = True
                    print("a")
                if event.key == K_d:
                    move_right = True
                    print("d")
                if event.key == K_q and current_timeE - Biglast_shot_time >= BigSHOOT_DELAY:
                        bob.EspecialShoot()
                        Biglast_shot_time = current_timeE
            if event.type == KEYUP:
                if event.key == K_w:
                    move_up = False
                if event.key == K_s:
                    move_down = False
                if event.key == K_a:
                    move_left = False
                if event.key == K_d:
                    move_right = False

            
            

        if move_up == True:
            bob.rect.y -= 10
        if move_down:
            bob.rect.y += 10
        if move_left:
            bob.rect.x -= 10 
        if move_right:
            bob.rect.x += 10

        
    # LIMITADOR DE TELA     
        bob.rect.clamp_ip(screen_rect)

    #Atualiza o mouse
    
        pygame.display.update()

        clock.tick(60)

def menu():
    while True:
        pygame.display.set_caption("Vulcano Menu")

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
            
                if play_rect.collidepoint(event.pos):
                    print("Você clicou em Jogar")
                    jogo()
                if sound_rect.collidepoint(event.pos):
                    print("Você clicou em Som")
                    
                if score_rect.collidepoint(event.pos):
                    print("Você clicou em Placar")
                    placar()
                    
        
        # Preenche a tela com fundo vermelho
        screen.fill(red)

        # Desenha o texto das opções na tela
        screen.blit(play_text, play_rect)
        screen.blit(sound_text, sound_rect)
        screen.blit(score_text, score_rect)
        screen.blit(ti_text, ti_rect)

        

        # Atualiza a tela
        pygame.display.update()

def placar():

    running = True
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        pygame.display.update()
       
menu()