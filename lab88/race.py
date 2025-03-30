#импорт
import pygame, sys
from pygame.locals import *
import random, time

#инициализация
pygame.init()


FPS = 60
FramePerSec = pygame.time.Clock()

#создание цветов
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#размер экрана
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

#скорость
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0  #новый счетчик

#шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

#задний фон
background = pygame.image.load("AnimatedStreet.png")

#белый экран
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

#enemy(вражеский класс)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1  #когда появляется новый враг,счетчик увеличивается
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

#player(класс игрока)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

#coin(класс монет)
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coin.png")  
        self.image = pygame.transform.scale(self.image, (30, 30))  #уменьшаем размер монеты
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-100, 0))  #монета появляется в верхней части экрана

    def move(self):
        self.rect.move_ip(0, SPEED // 2)  #монета падает медленне чем противник
        if self.rect.top > SCREEN_HEIGHT:  #iесли монета упадет вниз, она снова появится сверху
            self.rect.top = random.randint(-100, 0)
            self.rect.centerx = random.randint(40, SCREEN_WIDTH - 40)

#setting up sprites
P1 = Player()
E1 = Enemy()
C1 = Coin()

#sprites group
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

#отсчет времени для увеличения скорости
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

#game loop(цикл игры)
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5  #увеличивающаяся скорость
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

   
    DISPLAYSURF.blit(background, (0, 0))

    #отображение счетчика в верхнем левом углу
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    #отображение количества монет в правом верхнем углу
    coins_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - 100, 10))

  
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    #проверяет взаимодействуют ли враг и игрок
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)

        
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()
        time.sleep(2)

        pygame.quit()
        sys.exit()

    #проверяет взаимодействуют ли игрок и монета
    if pygame.sprite.spritecollideany(P1, coins):
        COINS_COLLECTED += 1 
        C1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(50, 500))  # Перемещение монеты

    #обновление экрана
    pygame.display.update()
    FramePerSec.tick(FPS)