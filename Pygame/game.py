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
violet= (64, 0, 128)
BLUE = (0, 0, 255)
green = (0, 255, 0)

# BOLA ou tiro

BALL_COLOR = (0, 0, 255)
SHOOT_DELAY = 1000  # cooldown dos tiros (1 segundos)
BigSHOOT_DELAY = 10000 # cooldown dos tiros especiais(10 segundos)
# Tamanho da janela
WIDTH, HEIGHT = 800, 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_rect = screen.get_rect()
#Cenarios
bg1 = pygame.image.load("CENARIO1.png")
bg2 = pygame.image.load("CENARIO2.png")
bg3 = pygame.image.load("CENARIO3.jpeg")

# Fonte e tamanho
font = pygame.font.Font(None, 36)

# Variaveis de mouse 
mouse_x, mouse_y = 0, 0

#Variaveis de som
sound = True

#Pontos
pontuacoes = {}
pontFlag = 0

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
        self.damage = 1
        self.boss1 = 0
        self.boss2 = 0
        self.boss3 = 0

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.angle = math.atan2(mouse_y - self.rect.centery, mouse_x - self.rect.centerx)
        
        # Verificar se o personagem pode atirar novamente
        current_time = pygame.time.get_ticks()
        if pygame.mouse.get_pressed()[0] and current_time - self.last_shot_time >= SHOOT_DELAY:
            self.shoot()
            self.last_shot_time = current_time
  
    def shoot(self):
        ball  = Ball(self.rect.centerx, self.rect.centery, self.angle)
        Gsprites.add(ball)
        if sound == True:
            Cm = pygame.mixer.Sound("SONS/waterShot.wav")
            Cm.play()
            Cm.set_volume(0.4)
            
    def EspecialShoot(self):
        bball  = BigBall(self.rect.centerx, self.rect.centery, self.angle)
        Gsprites.add(bball)

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
        self.spawn_time = pygame.time.get_ticks()


    def update(self):
        self.rect.x += 16 * math.cos(self.angle)
        self.rect.y += 16 * math.sin(self.angle)

        lifetime = pygame.time.get_ticks() - self.spawn_time
        if lifetime >= 6000:  
            self.kill()

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
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x += 16 * math.cos(self.angle)
        self.rect.y += 16 * math.sin(self.angle)

        lifetime = pygame.time.get_ticks() - self.spawn_time
        if lifetime >= 6000:  
            self.kill()


class EvilBall(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((60, 60))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.angle = angle
        self.mask = pygame.mask.from_surface(self.image)
        self.power = 1
        self.collided = False
        self.lifetime = 6000
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x += 16 * math.cos(self.angle)
        self.rect.y += 16 * math.sin(self.angle)

        lifetime = pygame.time.get_ticks() - self.spawn_time
        if lifetime >= 6000:  
            self.kill()

class FBall(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(violet)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.angle = angle
        self.mask = pygame.mask.from_surface(self.image)
        self.power = 1
        self.collided = False
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x += 10 * math.cos(self.angle)
        self.rect.y += 10 * math.sin(self.angle)


        lifetime = pygame.time.get_ticks() - self.spawn_time
        if lifetime >= 6000:  
            self.kill()


#BRASA
class Brasa(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("brasa.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, WIDTH)
        self.rect.centery = random.randint(0, HEIGHT)
        self.speed = 12 #Velocidade das Brasas
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

#FOGAREIROS
class Fogareiro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Fogareiro.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, WIDTH)
        self.rect.centery = random.randint(0, HEIGHT)
        self.speed = 10  
        self.mask = pygame.mask.from_surface(self.image)
        self.life = 6
        self.spawn_time = pygame.time.get_ticks()
        self.collided = False
        self.last_shot_time = 0  
        self.angle = 0
        self.shoot_delay = 1000
        self.shoot_enabled = False

    def update(self):
        # Movimentação
        self.rect.x += random.randint(-self.speed, self.speed)
        self.rect.y += random.randint(-self.speed, self.speed)

        # Limitador de telas
        self.rect.x = max(0, min(self.rect.x, WIDTH))
        self.rect.y = max(0, min(self.rect.y, HEIGHT))

        current_time = pygame.time.get_ticks()

        #cooldown de nascer 
        if not self.shoot_enabled and current_time - self.spawn_time >= 1000:
            self.shoot_enabled = True

        #ATIRAR
         
        if self.shoot_enabled and current_time - self.last_shot_time >= 3000:
            self.shoot()
            if sound == True:
                enemyShotSound = pygame.mixer.Sound("SONS/enemy.wav") 
                enemyShotSound.play()
                enemyShotSound.set_volume(0.3)
            self.last_shot_time = current_time

    def shoot(self):
        # mirar no bob
        dx = bob.rect.centerx - self.rect.centerx
        dy = bob.rect.centery - self.rect.centery
        self.angle = math.atan2(dy, dx)

        fball = FBall(self.rect.centerx, self.rect.centery, self.angle)
        Gsprites.add(fball)
        Enemies.add(fball)


class Carvoeiro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("carvoeiro.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, WIDTH)
        self.rect.centery = random.randint(0, HEIGHT)
        self.speed = 10  
        self.mask = pygame.mask.from_surface(self.image)
        self.life = 20
        self.spawn_time = pygame.time.get_ticks()
        self.collided = False
        self.last_shot_time = 0  
        self.angle = 0

    def update(self):

        # Limitador de telas
        self.rect.x = max(0, min(self.rect.x, WIDTH))
        self.rect.y = max(0, min(self.rect.y, HEIGHT))

        #ATIRAR
         
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= 2000:
            self.shoot()
            if sound == True:
                enemyShotSound = pygame.mixer.Sound("SONS/enemy.wav") 
                enemyShotSound.play()
                enemyShotSound.set_volume(0.3)
            self.last_shot_time = current_time
        

    def shoot(self):
        # mirar no bob
        dx = bob.rect.centerx - self.rect.centerx
        dy = bob.rect.centery - self.rect.centery
        self.angle = math.atan2(dy, dx)

        fball = FBall(self.rect.centerx, self.rect.centery, self.angle)
        Gsprites.add(fball)
        Enemies.add(fball)


class Boss1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bosstree.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, WIDTH)
        self.rect.centery = random.randint(0, HEIGHT)
        self.speed = 15  #Velocidade das Brasas
        self.mask = pygame.mask.from_surface(self.image)
        self.life = 20
        self.spawn_time = pygame.time.get_ticks()
        self.collided = False
        self.last_shot_time = 0  
        self.angle = 0
        

    def update(self):
        # Movimentação
        self.rect.x += random.randint(-self.speed, self.speed)
        self.rect.y += random.randint(-self.speed, self.speed)

        # Limitador de telas
        self.rect.x = max(0, min(self.rect.x, WIDTH))
        self.rect.y = max(0, min(self.rect.y, HEIGHT))

        #ATIRAR
         
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= 1000:
            self.shoot()
            if sound == True:
                enemyShotSound = pygame.mixer.Sound("SONS/enemy.wav") 
                enemyShotSound.play()
                enemyShotSound.set_volume(0.3)
            self.last_shot_time = current_time

    def shoot(self):
        # mirar no bob
        dx = bob.rect.centerx - self.rect.centerx
        dy = bob.rect.centery - self.rect.centery
        self.angle = math.atan2(dy, dx)

        eball = EvilBall(self.rect.centerx, self.rect.centery, self.angle)
        Gsprites.add(eball)
        Enemies.add(eball)
    

class Boss2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("boss2.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, WIDTH)
        self.rect.centery = random.randint(0, HEIGHT)
        self.speed = 15  #Velocidade das Brasas
        self.mask = pygame.mask.from_surface(self.image)
        self.life = 30
        self.spawn_time = pygame.time.get_ticks()
        self.collided = False
        self.last_shot_time = 0  
        self.angle = 0
        

    def update(self):
        # Movimentação
        self.rect.x += random.randint(-self.speed, self.speed)
        self.rect.y += random.randint(-self.speed, self.speed)

        # Limitador de telas
        self.rect.x = max(0, min(self.rect.x, WIDTH))
        self.rect.y = max(0, min(self.rect.y, HEIGHT))

        #ATIRAR
         
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= 3000:
            self.shoot()
            if sound == True:
                enemyShotSound = pygame.mixer.Sound("SONS/enemy.wav") 
                enemyShotSound.play()
                enemyShotSound.set_volume(0.3)
            self.last_shot_time = current_time

    def shoot(self):
        # mirar no bob
        dx = bob.rect.centerx - self.rect.centerx
        dy = bob.rect.centery - self.rect.centery
        self.angle = math.atan2(dy, dx)

        beball = BEvilBall(self.rect.centerx, self.rect.centery, self.angle)
        Gsprites.add(beball)
        Enemies.add(beball)

class Boss3(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("DG.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, WIDTH)
        self.rect.centery = random.randint(0, HEIGHT)
        self.speed = 15  #Velocidade das Brasas
        self.mask = pygame.mask.from_surface(self.image)
        self.life = 50
        self.spawn_time = pygame.time.get_ticks()
        self.collided = False
        self.last_shot_time = 0
        self.shot_cooldown = 3000  
        self.angle = 0
        self.shotType = 1

    def shoot1(self):
        # mirar no bob
        dx = bob.rect.centerx - self.rect.centerx
        dy = bob.rect.centery - self.rect.centery
        self.angle = math.atan2(dy, dx)

        eball = EvilBall(self.rect.centerx, self.rect.centery, self.angle)
        Gsprites.add(eball)
        Enemies.add(eball)


    def shoot2(self):
        # mirar no bob
        dx = bob.rect.centerx - self.rect.centerx
        dy = bob.rect.centery - self.rect.centery
        self.angle = math.atan2(dy, dx)

        beball = BEvilBall(self.rect.centerx, self.rect.centery, self.angle)
        Gsprites.add(beball)
        Enemies.add(beball)

    def update(self):
        # Movimentação
        self.rect.x += random.randint(-self.speed, self.speed)
        self.rect.y += random.randint(-self.speed, self.speed)

        # Limitador de telas
        self.rect.x = max(0, min(self.rect.x, WIDTH))
        self.rect.y = max(0, min(self.rect.y, HEIGHT))

        #ATIRAR
         
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shot_cooldown:
            if self.shotType == 1:
                self.shoot1()
                if sound == True:
                    enemyShotSound = pygame.mixer.Sound("SONS/enemy.wav") 
                    enemyShotSound.play()
                    enemyShotSound.set_volume(0.3)
                self.shotType = 2
            elif self.shotType == 2:
                self.shoot2()
                if sound == True:
                    enemyShotSound = pygame.mixer.Sound("SONS/enemy.wav") 
                    enemyShotSound.play()
                    enemyShotSound.set_volume(0.3)
                self.shotType = 1
            self.last_shot_time = current_time


class BEvilBall(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((260, 60))
        self.image.fill(violet)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.angle = angle
        self.mask = pygame.mask.from_surface(self.image)
        self.power = 1
        self.collided = False
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x += 12 * math.cos(self.angle)
        self.rect.y += 12 * math.sin(self.angle)

        lifetime = pygame.time.get_ticks() - self.spawn_time
        if lifetime >= 6000:  
            self.kill()




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

sound_text = font.render("Som", True, green)
sound_rect = sound_text.get_rect()
sound_rect.center = (800 // 2, 400)

score_text = font.render("Placar", True, WHITE)
score_rect = score_text.get_rect()
score_rect.center = (800 // 2, 500)

inst_text = font.render("Instruções", True, WHITE)
inst_rect = inst_text.get_rect()
inst_rect.center = (800 // 2, 600)


#VIDA  HUD

life_text = font.render(f"Vida: {bob.life}", True, (95,159,159))
life_rect = life_text.get_rect()
life_rect.center = ( WIDTH -150, 35)

#Pontos  HUD

point_text = font.render(f"Pontos: {bob.points}", True, (95,159,159))
point_rect = point_text.get_rect()
point_rect.center = ( WIDTH -300, 35)

#Level HUD

level_text = font.render(f"Level: {bob.level}", True, (95,159,159))
level_rect = level_text.get_rect()
level_rect.center = ( WIDTH -450, 35)

#Level HUD

fase_text = font.render(f"Fase: {bob.level}", True, (95,159,159))
fase_rect = fase_text.get_rect()
fase_rect.center = ( WIDTH -600, 35)

def reset_game_state():
    global boss1_spawned, boss2_spawned, boss3_spawned, inimigosMortos, fase, fase2start, fase3start, restart2, restart3, restart3f, max_brasas, max_fogareiros, max_carvoeiros, pontFlag
    boss1_spawned = False
    boss2_spawned = False
    boss3_spawned = False
    inimigosMortos = 0
    fase = 1
    fase2start = False
    fase3start = False
    restart2 = 0
    restart3 = 0
    restart3f = 0
    max_brasas = 15
    max_fogareiros = 10
    max_carvoeiros = 10
    bob.life = 3
    bob.level = 1
    bob.points = 0
    bob.damage = 1
    bob.boss1 = 0
    bob.boss2 = 0
    bob.boss3 = 0
    pontFlag = 0
    Gsprites.empty()
    Enemies.empty()
    Gsprites.add(bob) 



def jogo():


#Variavel da fase
    fase = 1
#Variavel de movimento
    move_up = False
    move_down = False 
    move_left = False
    move_right = False

    #tiro especial
    Biglast_shot_time = 0


    #SPAWN DAS BRASAS            
    brasasNoMapa = 0
    brasa_spawn_time = 2000  # 2 segundos 
    lastBrasa_spawn_time = 0
    max_brasas = 15

    #SPAWN DOS FOGAREIROS           
    fogareirosNoMapa = 0
    fogareiro_spawn_time = 6000  # 8 6egundos 
    lastFogareiro_spawn_time = 0
    max_fogareiros = 10

    #SPAWN DOS CARVOEIROS          
    carvoeirosNoMapa = 0
    carvoeiro_spawn_time = 12000  # 9 segundos 
    lastCarvoeiro_spawn_time = 0
    max_carvoeiros = 10

    #reset de colisão com inimigos 
    RESET_COLLIDED_EVENT = pygame.USEREVENT + 1
    reset_collided_time = 3000 # 3 sec

    #numero de inimigos
    inimigosMortos = 0

    #boss spawn 
    boss_warning_time = None
    boss1_spawned = False
    boss2_spawned = False
    boss3_spawned = False
    

    #fase2
    fase2start = False
    começoDeFase = None
    restart2 = 0
    começoDeUltimaFase = None

    #fase3
    fase3start = False
    restart3 = 0
    restart3f = 0

    #over
    gameOver = False
    Over = None

    #vitoria
    Victory = False
    Vic = None
    #Musica
    isPlaying = 0
    overPlaying = 0
    lvFlag = 0
    vicFlag = 0
    
   
#LOOP JOGO
    clock = pygame.time.Clock()
    running = True
    while running:
        
        pygame.display.update()
        pygame.display.set_caption("GAME")
        screen.fill(WHITE)
        
        screen.blit(bg1, (0, 0))
            
        if fase == 2:
            screen.blit(bg2, (0, 0))
            current_timef2 = pygame.time.get_ticks() 
            if começoDeFase == None:
                bob.points = bob.points + (bob.life * 50)
                começoDeFase = current_timef2
                bob.life += 3
            if current_timef2 - começoDeFase < 5000:
                warning_text = font.render("INICIO DA FASE 2 !!!", True, BLACK)
                warning_rect = warning_text.get_rect()
                warning_rect.center = (WIDTH // 2, HEIGHT // 2)
                screen.blit(warning_text, warning_rect)
            else:
                if current_timef2 - começoDeFase >= 5000:
                    fase2start = True


        if fase == 3:
            screen.blit(bg3, (0, 0))
            current_timef3 = pygame.time.get_ticks()
            if começoDeUltimaFase == None:
                bob.points = bob.points + (bob.life * 50)
                começoDeUltimaFase = current_timef3
                bob.life += 3
            if current_timef3 - começoDeUltimaFase < 5000:
                warning_text = font.render("INICIO DA FASE 3 !!!", True, WHITE)
                warning_rect = warning_text.get_rect()
                warning_rect.center = (WIDTH // 2, HEIGHT // 2)
                screen.blit(warning_text, warning_rect)
            else:
                if current_timef3 - começoDeUltimaFase >= 5000:
                    fase3start = True    
#Derrota
        if gameOver == True:
            screen.fill(BLACK)
            current_timeGO = pygame.time.get_ticks()
            if Over == None:
                Over = current_timeGO
            if current_timeGO - Over < 5000:
                if sound == True and isPlaying ==1:
                    Mhit.stop()
                if sound == True and overPlaying == 0:
                    Overhit = pygame.mixer.Sound("SONS/gameOver.wav") 
                    Overhit.play()
                    Overhit.set_volume(0.5)
                    overPlaying = 1
                warning_text = font.render("FIM DE JOGO", True, red)
                warning_rect = warning_text.get_rect()
                warning_rect.center = (WIDTH // 2, HEIGHT // 2)
                screen.blit(warning_text, warning_rect)
            else:
                if current_timeGO - Over >=5000:
                    global pontFlag
                    while pontFlag == 0:
                        nome_jogador = input("Digite seu nome: ")
                        pontuacoes[nome_jogador] = bob.points
                        pontFlag = 1
                    running = False
                    placar()
#VITORIA
        if Victory == True:
            
            if sound == True and isPlaying ==1:
                    Mhit.stop()
            while vicFlag == 0:
                if bob.life == 9:
                    bob.points = bob.points + (bob.life * 100)
                else:
                    bob.points = bob.points + (bob.life * 50)
                if sound == True:
                    vicSound = pygame.mixer.Sound("SONS/win.wav") 
                    vicSound.play()
                    vicSound.set_volume(0.5)
                vicFlag = 1 
            screen.fill(WHITE)
            current_timeGO = pygame.time.get_ticks()
            if Vic == None:
                Vic = current_timeGO
            if current_timeGO - Vic < 8000:
                warning_text = font.render("VITÓRIA", True, violet)
                warning_rect = warning_text.get_rect()
                warning_rect.center = (WIDTH // 2, HEIGHT // 2)
                screen.blit(warning_text, warning_rect)
            else:
                if current_timeGO - Vic >=8000:

                    while pontFlag == 0:
                        nome_jogador = input("Digite seu nome: ")
                        pontuacoes[nome_jogador] = bob.points
                        pontFlag = 1
                    running = False
                    placar()

        if sound == True and isPlaying == 0:
            Mhit = pygame.mixer.Sound("SONS/backm.wav")
            Mhit.play(-1)
            Mhit.set_volume(0.03)
            isPlaying = 1
        elif sound == False and isPlaying == 1:
            Mhit.stop()
            isPlaying = 0
                              
 
        Gsprites.update()  

#Upgrades dds

        if bob.points >=100:
            while lvFlag == 0:
                if sound == True:
                    levelUpSound = pygame.mixer.Sound("SONS/levelUp.wav") 
                    levelUpSound.play()
                    levelUpSound.set_volume(0.3)
                lvFlag = 1
            bob.level = 2
            bob.damage = 2
        if bob.points >= 350:
            while lvFlag == 1:
                if sound == True:
                    levelUpSound = pygame.mixer.Sound("SONS/levelUp.wav") 
                    levelUpSound.play()
                    levelUpSound.set_volume(0.3)
                lvFlag = 2
            bob.level = 3
            bob.damage = 3
        if bob.points >= 420:
            while lvFlag == 2:
                if sound == True:
                    levelUpSound = pygame.mixer.Sound("SONS/levelUp.wav") 
                    levelUpSound.play()
                    levelUpSound.set_volume(0.3)
                lvFlag = 3
            bob.level = 4
            bob.damage = 4
        

#COLISAO INIMIGOS com tiro
        for ball in Gsprites:
            if isinstance(ball, Ball) and not ball.collided:
                hits = pygame.sprite.spritecollide(ball, Enemies, False, pygame.sprite.collide_circle)
                for hit in hits:
                    if sound == True:
                        hitsound = pygame.mixer.Sound("SONS/marker.wav") 
                        hitsound.play()
                        hitsound.set_volume(0.3)
                    if isinstance(hit, Brasa):
                            hit.life -= bob.damage
                            ball.collided = True
                            if hit.life <= 0:
                                hit.kill()
                                bob.points += 4
                                inimigosMortos += 1
                
                    if isinstance(hit, Boss1):
                            hit.life -= bob.damage
                            ball.collided = True
                            if hit.life <= 0:
                                hit.kill()
                                fase = 2
                                print(fase)
                    
                    if isinstance(hit, Fogareiro):
                            hit.life -= bob.damage
                            ball.collided = True
                            if hit.life <= 0:
                                hit.kill()
                                inimigosMortos += 1
                                bob.points += 8
                    
                    if isinstance(hit, Boss2):
                            hit.life -= bob.damage
                            ball.collided = True
                            if hit.life <= 0:
                                hit.kill()
                                fase = 3
                                print(fase)

                    if isinstance(hit, Carvoeiro):
                            hit.life -= bob.damage
                            ball.collided = True
                            if hit.life <= 0:
                                hit.kill()
                                inimigosMortos += 1
                                bob.points += 16
                    
                    if isinstance(hit, Boss3):
                            hit.life -= bob.damage
                            ball.collided = True
                            if hit.life <= 0:
                                hit.kill()
                                Victory = True

                            

#COLISAO INIMIGOS com especial
        for bball in Gsprites:
            if isinstance(bball, BigBall) and not bball.collided:
                hits = pygame.sprite.spritecollide(bball, Enemies, False, pygame.sprite.collide_circle)
                for hit in hits:
                    if sound == True:
                        hitsound = pygame.mixer.Sound("SONS/marker.wav") 
                        hitsound.play()
                        hitsound.set_volume(0.3)
                    if isinstance(hit, Brasa):
                        hit.life -= 5
                        bball.collided = True
                        if hit.life <= 0:
                            hit.kill()
                            bob.points += 4
                            inimigosMortos += 1
                       
                    if isinstance(hit, Boss1):
                            hit.life -= 5
                            bball.collided = True
                            if hit.life <= 0:
                                hit.kill()
                                fase = 2
                                print(fase)

                    if isinstance(hit, Fogareiro):
                            hit.life -= 5
                            bball.collided = True
                            if hit.life <= 0:
                                bob.points += 8
                                inimigosMortos += 1
                                hit.kill()
                    
                    if isinstance(hit, Boss2):
                            hit.life -= 5
                            bball.collided = True
                            if hit.life <= 0:
                                hit.kill()
                                fase = 3
                                print(fase)
                    
                    if isinstance(hit, Carvoeiro):
                            hit.life -= 5
                            bball.collided = True
                            if hit.life <= 0:
                                hit.kill()
                                inimigosMortos += 1
                                bob.points += 16
                    
                    if isinstance(hit, Boss3):
                            hit.life -= 5
                            bball.collided = True
                            if hit.life <= 0:
                                hit.kill()
                                Victory = True
                                
                            

#Colisão brasa com player
        for brasinha in Enemies:
            if isinstance(brasinha, Brasa) and not brasinha.collided:
                current_timeS = pygame.time.get_ticks()
                if current_timeS - brasinha.spawn_time >= 3000:
                    hits = pygame.sprite.spritecollide(brasinha, Gsprites, False, pygame.sprite.collide_circle)
                    for hit in hits:
                        if isinstance(hit, Character):
                            if sound ==True:
                                lostSound = pygame.mixer.Sound("SONS/dano.wav") 
                                lostSound.play()
                                lostSound.set_volume(0.3)
                            hit.life -= 1
                            if hit.life <= 0:
                                hit.kill()
                                gameOver = True
                            brasinha.collided = True
                            if brasinha.collided == True:
                                pygame.time.set_timer(RESET_COLLIDED_EVENT, reset_collided_time)
#Colisão com fogo do chefe1

        for eball in Enemies:
            if isinstance(eball, EvilBall) and not eball.collided:
                hits = pygame.sprite.spritecollide(eball, Gsprites, False, pygame.sprite.collide_circle)
                for hit in hits:
                    if isinstance(hit, Character):
                            if sound ==True:
                                lostSound = pygame.mixer.Sound("SONS/dano.wav") 
                                lostSound.play()
                                lostSound.set_volume(0.3)
                            hit.life -= 1
                            if hit.life <= 0:
                                hit.kill()
                                gameOver = True
                            eball.collided = True
#Colisão com fogo do fogareiro

        for fball in Enemies:
            if isinstance(fball, FBall) and not fball.collided:
                hits = pygame.sprite.spritecollide(fball, Gsprites, False, pygame.sprite.collide_circle)
                for hit in hits:
                    if isinstance(hit, Character):
                            if sound ==True:
                                lostSound = pygame.mixer.Sound("SONS/dano.wav") 
                                lostSound.play()
                                lostSound.set_volume(0.3)
                            hit.life -= 1
                            if hit.life <= 0:
                                hit.kill()
                                gameOver = True
                            fball.collided = True
        
#Colisão com fogo do Boss2(chandelure)

        for beball in Enemies:
            if isinstance(beball, BEvilBall) and not beball.collided:
                hits = pygame.sprite.spritecollide(beball, Gsprites, False, pygame.sprite.collide_circle)
                for hit in hits:
                    if isinstance(hit, Character):
                            if sound ==True:
                                lostSound = pygame.mixer.Sound("SONS/dano.wav") 
                                lostSound.play()
                                lostSound.set_volume(0.3)
                            hit.life -= 1
                            if hit.life <= 0:
                                hit.kill()
                                gameOver = True
                            beball.collided = True


#DESENHA O GRUPO COM SPRITES
        Gsprites.draw(screen)

        current_timeE = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    move_up = True
                    
                if event.key == K_s:
                    move_down = True
                    
                if event.key == K_a:
                    move_left = True
                    bob.image = pygame.image.load("left-hero.png")
                    
                if event.key == K_d:
                    move_right = True
                    bob.image = pygame.image.load("right-hero.png")
                    
                if event.key == K_q and current_timeE - Biglast_shot_time >= BigSHOOT_DELAY:
                        bob.EspecialShoot()
                        Biglast_shot_time = current_timeE
                        
                        if sound == True:
                            bc = pygame.mixer.Sound("SONS/onda.wav")
                            bc.play()
                            bc.set_volume(0.2)
                            
                       

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
#RESET DO SPAWN DAS BRASAS PARA A FASE 2
        if fase == 2 and fase2start == True and restart2 == 0:
            brasasNoMapa = 0
            max_brasas = 10
            inimigosMortos = 0
            restart2 = 1
#RESET DO SPAWN DAS BRASAS PARA A FASE 3
        if fase == 3 and fase3start == True and restart3 == 0:
            brasasNoMapa = 0
            max_brasas = 5
            inimigosMortos = 0
            restart3 = 1




        #Spawn do boss

        if not boss1_spawned and inimigosMortos == max_brasas and fase == 1:
            current_timeb1 = pygame.time.get_ticks()
            if boss_warning_time is None:
                boss_warning_time = current_timeb1
            if current_timeb1 - boss_warning_time < 5000:
                warning_text = font.render("O CHEFE ESTÁ VINDO, FURIA FLAMEJANTE DA FLORESTA !!!!!", True, BLACK)
                warning_rect = warning_text.get_rect()
                warning_rect.center = (WIDTH // 2, HEIGHT // 2)
                screen.blit(warning_text, warning_rect)
            else:
                if current_timeb1 - boss_warning_time >= 5000:
                    boss1_spawned = True
                    if bob.boss1 == 0:
                        furia = Boss1()
                        furia.rect.clamp_ip(screen_rect)
                        Gsprites.add(furia)
                        Enemies.add(furia)
                        bob.boss1 = 1
                    boss_warning_time = None
                    
        
         #SPAWN Dos Fogareiros
        if fase == 2 and fase2start == True:
            current_timeFogareiro = pygame.time.get_ticks()
            if fogareirosNoMapa < max_fogareiros and current_timeFogareiro - lastFogareiro_spawn_time >= fogareiro_spawn_time:
                lastFogareiro_spawn_time = current_timeFogareiro
                fogareirosNoMapa = fogareirosNoMapa + 1
                foguinho = Fogareiro()
                foguinho.rect.clamp_ip(screen_rect)
                Gsprites.add(foguinho)
                Enemies.add(foguinho)
        if fase == 3 and fase3start == True:
            current_timeFogareiro = pygame.time.get_ticks()
            if fogareirosNoMapa < max_fogareiros and current_timeFogareiro - lastFogareiro_spawn_time >= fogareiro_spawn_time:
                lastFogareiro_spawn_time = current_timeFogareiro
                fogareirosNoMapa = fogareirosNoMapa + 1
                foguinho = Fogareiro()
                foguinho.rect.clamp_ip(screen_rect)
                Gsprites.add(foguinho)
                Enemies.add(foguinho)
            #RESET DO SPAWN DOS Fogareiros PARA A FASE 3
            if fase == 3 and fase3start == True and restart3f == 0:
                fogareirosNoMapa = 0
                max_fogareiros = 5
                restart3f = 1

        #Spawn do boss 2

        if not boss2_spawned and inimigosMortos == max_brasas + max_fogareiros and fase == 2:
            current_timeb1 = pygame.time.get_ticks()
            if boss_warning_time is None:
                boss_warning_time = current_timeb1
            if current_timeb1 - boss_warning_time < 5000:
                warning_text = font.render("O CHEFE ESTÁ VINDO, CHANDELURE O ESPIRITO DO DESERTO !!!!!", True, BLACK)
                warning_rect = warning_text.get_rect()
                warning_rect.center = (WIDTH // 2, HEIGHT // 2)
                screen.blit(warning_text, warning_rect)
            else:
                if current_timeb1 - boss_warning_time >= 5000:
                    boss2_spawned = True
                    if bob.boss2 == 0:
                        chandelure = Boss2()
                        chandelure.rect.clamp_ip(screen_rect)
                        Gsprites.add(chandelure)
                        Enemies.add(chandelure)
                        bob.boss2 = 1
                    boss_warning_time = None
        
         #SPAWN Dos Carvoeiros
        if fase == 3 and fase3start == True:
            current_timeCarvoeiro = pygame.time.get_ticks()
            if carvoeirosNoMapa < max_carvoeiros and current_timeCarvoeiro - lastCarvoeiro_spawn_time >= carvoeiro_spawn_time:
                lastCarvoeiro_spawn_time = current_timeCarvoeiro
                carvoeirosNoMapa = carvoeirosNoMapa + 1
                carvão = Carvoeiro()
                carvão.rect.clamp_ip(screen_rect)
                Gsprites.add(carvão)
                Enemies.add(carvão)   
        

        #Spawn do boss 3

        if not boss3_spawned and inimigosMortos == max_brasas + max_fogareiros + max_carvoeiros and fase == 3:
            current_timeb1 = pygame.time.get_ticks()
            if boss_warning_time is None:
                boss_warning_time = current_timeb1
            if current_timeb1 - boss_warning_time < 5000:
                warning_text = font.render("O CHEFE FINAL ESTÁ VINDO, ACABE COM O PRESIDENTE DG !!!!!", True, WHITE)
                warning_rect = warning_text.get_rect()
                warning_rect.center = (WIDTH // 2, HEIGHT // 2)
                screen.blit(warning_text, warning_rect)
            else:
                if current_timeb1 - boss_warning_time >= 5000:
                    boss3_spawned = True
                    if bob.boss3 == 0:
                        DG = Boss3()
                        DG.rect.clamp_ip(screen_rect)
                        Gsprites.add(DG)
                        Enemies.add(DG)
                        bob.boss3 = 1
                    boss_warning_time = None


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
        life_text = font.render(f"Vida: {bob.life}", True, (255, 0, 128))
        screen.blit(life_text, life_rect)
    
    #HUD de pontos
        point_text = font.render(f"Pontos: {bob.points}", True, (0, 255, 255))
        screen.blit(point_text, point_rect)

    #HUD de Nivel
        level_text = font.render(f"Level: {bob.level}", True, (64, 0, 128))
        screen.blit(level_text, level_rect)
    
    #HUD de Fase
        fase_text = font.render(f"Fase: {fase}", True, (0, 64, 128))
        screen.blit(fase_text, fase_rect)


    #Atualiza o mouse
    
        pygame.display.update()

        clock.tick(60)

def menu():
    global sound
    global sound_text
    while True:
        pygame.display.set_caption("Vulcano Menu")

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:

                #Jogar          
                if play_rect.collidepoint(event.pos):

                    if sound == True:
                        clicksound = pygame.mixer.Sound("SONS/click.wav") 
                        clicksound.play()
                        clicksound.set_volume(1.0)

                    print("Você clicou em Jogar")
                    jogo()
                    reset_game_state()
                #som                               
                if sound_rect.collidepoint(event.pos):
                    print("Você clicou em Som")
                   
                    if sound == True:
                        sound = False
                        clicksound = pygame.mixer.Sound("SONS/click.wav") 
                        clicksound.play()
                        clicksound.set_volume(1.0)
                        sound_text = font.render("Som", True, WHITE)
                    elif sound == False:
                        sound = True
                        sound_text = font.render("Som", True, green)
                    print(sound)

                    if sound == True:
                        clicksound = pygame.mixer.Sound("SONS/click.wav") 
                        clicksound.play()
                        clicksound.set_volume(1.0)
                #placar
                if score_rect.collidepoint(event.pos):
                    print("Você clicou em Placar")
                    if sound == True:
                        clicksound = pygame.mixer.Sound("SONS/click.wav") 
                        clicksound.play()
                        clicksound.set_volume(1.0)
                    placar()
                
                #instruções
                if inst_rect.collidepoint(event.pos):
                    print("Você clicou em Instruções")
                    if sound == True:
                        clicksound = pygame.mixer.Sound("SONS/click.wav") 
                        clicksound.play()
                        clicksound.set_volume(1.0)
                    howToPlay()
                    
        
        
        screen.fill(red)

        # Desenha menu
        screen.blit(play_text, play_rect)
        screen.blit(sound_text, sound_rect)
        screen.blit(score_text, score_rect)
        screen.blit(ti_text, ti_rect)
        screen.blit(inst_text, inst_rect)

        

        
        pygame.display.update()

def placar():

    #pontos
    sorted_pontuacoes = None

    running = True
    while running:
        screen.fill(BLUE)
        pygame.display.set_caption('PLACAR')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        #Normal
        
        sorted_pontuacoes = {k: v for k, v in sorted(pontuacoes.items(), key=lambda item: item[1], reverse=True)}
        y = 50
        for nome, pontos in sorted_pontuacoes.items():
            text = font.render(f"{nome}: {pontos} pontos", True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
            y += 40    
        pygame.display.update()

def howToPlay():

    #pontos
    como_jogar = [
    "Use W A S D para se mover",
    "Botão esquerdo do mouse para atirar",
    "Tecla Q para disparar um super ataque",
    "Derrote todos os inimigos para enfrentar o chefe",
    "Ganhe 3 vidas a cada fase",
    "Comece com apenas 3 vidas",
    "Ganhe pontos derrotando inimigos para subir de nível",
    "No final do jogo, escreva seu nome no console para salvar",
    "a Pontuação"
]

    running = True
    while running:
        screen.fill(violet)
        pygame.display.set_caption('Instruções do Jogo')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        #Normal
        
        for i, line in enumerate(como_jogar):
            text = font.render(line, True, WHITE)
            screen.blit(text, (10, 50 + i * 80))


        pygame.display.update()
       
menu()