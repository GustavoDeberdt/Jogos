import pygame
import sys
import math
import random
from pygame.locals import *

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
        self.mask = pygame.mask.from_surface(self.image)
        self.life = 3
        self.level = 1
        self.points = 0

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
        self.mask = pygame.mask.from_surface(self.image)
        self.power = 1
        self.collided = False

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
        self.mask = pygame.mask.from_surface(self.image)
        self.collided = False

    def update(self):
        self.rect.x += 12 * math.cos(self.angle)
        self.rect.y += 12 * math.sin(self.angle)

#BRASA
class Brasa(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("brasa.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, WIDTH)
        self.rect.centery = random.randint(0, HEIGHT)
        self.speed = 10  #Velocidade das Brasas
        self.mask = pygame.mask.from_surface(self.image)
        self.life = 1
        self.spawn_time = pygame.time.get_ticks()
        self.collided = False

    def update(self):
        # Movimentação
        self.rect.x += random.randint(-self.speed, self.speed)
        self.rect.y += random.randint(-self.speed, self.speed)

        # Limitador de telas
        self.rect.x = max(0, min(self.rect.x, WIDTH))
        self.rect.y = max(0, min(self.rect.y, HEIGHT))



#Insanciando e colocando em grupo
bob = Character()

Gsprites = pygame.sprite.Group()
Enemies = pygame.sprite.Group()
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

#VIDA  HUD

life_text = font.render(f"Vida: {bob.life}", True, (95,159,159))
life_rect = life_text.get_rect()
life_rect.center = ( WIDTH -150, 35)

#Pontos  HUD

point_text = font.render(f"Vida: {bob.points}", True, (95,159,159))
point_rect = point_text.get_rect()
point_rect.center = ( WIDTH -300, 35)


def jogo():


#Variavel de movimento
    move_up = False
    move_down = False 
    move_left = False
    move_right = False

    #tiro especial
    Biglast_shot_time = 0


    #SPAWN DAS BRASAS            
    brasasNoMapa = 0
    brasa_spawn_time = 3000  # 6 segundos 
    lastBrasa_spawn_time = 0
    max_brasas = 2

    #reset de colisão com brasas 
    RESET_COLLIDED_EVENT = pygame.USEREVENT + 1
    reset_collided_time = 3000 # 3 sec
   
#LOOP JOGO
    clock = pygame.time.Clock()
    running = True
    while running:
        
        pygame.display.update()
        pygame.display.set_caption("GAME")
        screen.fill(WHITE)
        screen.blit(bg3, (0, 0))
        
        Gsprites.update()  
              
#COLISAO BRASAS
        for ball in Gsprites:
            if isinstance(ball, Ball) and not ball.collided:
                hits = pygame.sprite.spritecollide(ball, Enemies, False, pygame.sprite.collide_circle)
                for hit in hits:
                    if isinstance(hit, Brasa):
                            hit.life -= 1
                            if hit.life <= 0:
                                hit.kill()
                                bob.points += 4
                            ball.collided = True

#COLISAO BRASAS com especial
        for bball in Gsprites:
            if isinstance(bball, BigBall) and not bball.collided:
                hits = pygame.sprite.spritecollide(bball, Enemies, False, pygame.sprite.collide_circle)
                for hit in hits:
                    if isinstance(hit, Brasa):
                        hit.life -= 5
                        if hit.life <= 0:
                            hit.kill()
                            bob.points += 4
                        bball.collided = True
#Colisão brasa com player
        for brasinha in Enemies:
            if isinstance(brasinha, Brasa) and not brasinha.collided:
                current_timeS = pygame.time.get_ticks()
                if current_timeS - brasinha.spawn_time >= 3000:
                    hits = pygame.sprite.spritecollide(brasinha, Gsprites, False, pygame.sprite.collide_circle)
                    for hit in hits:
                        if isinstance(hit, Character):
                            hit.life -= 1
                            if hit.life <= 0:
                                hit.kill()
                                
                            brasinha.collided = True
                            if brasinha.collided == True:
                                pygame.time.set_timer(RESET_COLLIDED_EVENT, reset_collided_time)


#DESENHA O GRUPO COM SPRITES
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

           #evento para resetar colisão         
            if event.type == RESET_COLLIDED_EVENT:
                for brasinha in Enemies:
                    brasinha.collided = False

          #SPAWN DAS BRASAS 
        current_timeBrasa = pygame.time.get_ticks()
        if brasasNoMapa < max_brasas and current_timeBrasa - lastBrasa_spawn_time >= brasa_spawn_time:
            lastBrasa_spawn_time = current_timeBrasa
            brasasNoMapa = brasasNoMapa + 1
            brasinha = Brasa()
            brasinha.rect.clamp_ip(screen_rect)
            Gsprites.add(brasinha)
            Enemies.add(brasinha)

            
        #for brasinha in Enemies:
            #pygame.draw.rect(screen, (255, 0, 0), brasinha.rect, 2)

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
        

    #HUD de vida
        life_text = font.render(f"Vida: {bob.life}", True, (95, 159, 159))
        screen.blit(life_text, life_rect)
    
    #HUD de pontos
        point_text = font.render(f"Pontos: {bob.points}", True, (95, 159, 159))
        screen.blit(point_text, point_rect)

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
                    
        
        
        screen.fill(red)

        # Desenha menu
        screen.blit(play_text, play_rect)
        screen.blit(sound_text, sound_rect)
        screen.blit(score_text, score_rect)
        screen.blit(ti_text, ti_rect)

        

        
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