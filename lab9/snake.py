#импорт
import pygame
import random
import sys

#инициализация
pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#настройка змеи
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_direction = "RIGHT"
change_to = snake_direction
speed = 10
game_score = 0
level = 1

#список возможных значений продуктов питания
food_types = [
    {"color": RED, "points": 1, "time_to_live": 7000},   
    {"color": BLUE, "points": 3, "time_to_live": 5000},  
    {"color": YELLOW, "points": 5, "time_to_live": 4000} 
]

#производство продуктов питания
def spawn_food():
    while True:
        food = {
            "pos": [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10],
            "type": random.choice(food_types),  
            "spawn_time": pygame.time.get_ticks()  
        }
        if food["pos"] not in snake_body:  
            return food
#первая еда
food = spawn_food()
isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != "DOWN":
                change_to = "UP"
            if event.key == pygame.K_DOWN and snake_direction != "UP":
                change_to = "DOWN"
            if event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                change_to = "LEFT"
            if event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                change_to = "RIGHT"

    #движение змейки
    snake_direction = change_to
    if snake_direction == "UP":
        snake_pos[1] -= 10
    elif snake_direction == "DOWN":
        snake_pos[1] += 10
    elif snake_direction == "LEFT":
        snake_pos[0] -= 10
    elif snake_direction == "RIGHT":
        snake_pos[0] += 10
    #новая голова
    snake_body.insert(0, list(snake_pos))

    #проверяет съела ли змейка еду
    if snake_pos == food["pos"]:
        game_score += food["type"]["points"]  #добавляет баллы
        food = spawn_food()  #создает новую еду
        #повышает уровень через каждые 4 очка
        if game_score % 4 == 0:
            level += 1
            speed += 2
    else:
        snake_body.pop()  #змейка не растет
    #проверяет не вышла ли змея за пределы границы
    if snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT:
        isRunning = False
    for block in snake_body[1:]:
        if snake_pos == block:
            isRunning = False

    #проверяет может ли еда еще отображаться на экране
    if pygame.time.get_ticks() - food["spawn_time"] > food["type"]["time_to_live"]:
        food = spawn_food()  #создает новую еду если время истекло

    screen.fill(BLACK)  
    #рисуем змейку
    for p in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(p[0], p[1], 10, 10))
    #еда
    pygame.draw.rect(screen, food["type"]["color"], pygame.Rect(food["pos"][0], food["pos"][1], 10, 10))
    score_text = font.render(f"Score: {game_score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (20, 20))
    screen.blit(level_text, (20, 50))

    pygame.display.update()
    clock.tick(speed)

game_over_text = font.render("GAME OVER", True, WHITE)
game_over_rect = game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
screen.fill(BLACK)
screen.blit(game_over_text, game_over_rect)
pygame.display.update()
pygame.time.wait(2000)  #пауза перед выходом