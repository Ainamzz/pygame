#импорт
import pygame, sys
from pygame.locals import *
import random, time

#инициализация
pygame.init()

#FPS
FPS = 60
FramePerSec = pygame.time.Clock()

#создание цветов
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0  #счетчик
COINS_FOR_SPEEDUP = 5  #количество монет для увеличения скорости
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
            SCORE += 1 #когда появляется новый враг,счетчик увеличивается
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
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)  #левый
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)  #правый
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.value = random.choice([1, 2, 3])  #вес монеты (1, 2, 3)
        self.image = pygame.image.load("coin.png")
        size = 20 * self.value  
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-100, 0)) #монета появляется в верхней части экрана

    def move(self):
        self.rect.move_ip(0, SPEED // 2)  #монета падает медленнее, чем противник
        if self.rect.top > SCREEN_HEIGHT:  #если монета упадет вниз, она снова появится сверху
            self.reset_position()
    def reset_position(self):
        self.value = random.choice([1, 2, 3])  #новый вес
        size = 20 * self.value
        self.image = pygame.transform.scale(pygame.image.load("coin.png"), (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-100, 0))

#создание объектов
P1 = Player()
E1 = Enemy()
coins = pygame.sprite.Group() 

for _ in range(3):  
    coins.add(Coin())
#sprites group
enemies = pygame.sprite.Group()
enemies.add(E1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1)
all_sprites.add(*coins)

#увеличение скорости каждые 1000 миллисекунд
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
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

    #перемещение спрайтов
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

    for coin in coins:
        #проверяет взаимодействуют ли игрок и монета
        if pygame.sprite.collide_rect(P1, coin):
            COINS_COLLECTED += coin.value  
            coin.reset_position() 

            #увеличение скорости
            if COINS_COLLECTED % COINS_FOR_SPEEDUP == 0:
                SPEED += 1
    pygame.display.update()
    FramePerSec.tick(FPS)