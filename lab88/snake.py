#импорт
import pygame
import time
import random

snake_speed = 15

#размер окна
window_x = 720
window_y = 480

#создание цветов
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

#инициализация
pygame.init()

#инициализирование игрового окна
pygame.display.set_caption('Snake')
game_window = pygame.display.set_mode((window_x, window_y))

fps = pygame.time.Clock()

#определение положения змеи по умолчанию
snake_position = [100, 50]

#определение первых 4 блоков тела змеи
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ]

#fruit position(положение плода)
fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                  random.randrange(1, (window_y // 10)) * 10]

fruit_spawn = True

#установка направления змеи по умолчанию к право
direction = 'RIGHT'
change_to = direction

#начальная оценка
score = 0

fruit_time = 5

#отображение функции Score
def show_score(choice, color, font, size) :
    #создание объекта шрифта score_font
    score_font = pygame.font.SysFont(font, size)

    #создать объект поверхности отображения score_surface
    score_surface = score_font.render('Score : ' + str(score), True, color)

    #создаем прямоугольный объект для текста
    score_rect = score_surface.get_rect()

    game_window.blit(score_surface, score_rect)


#функция завершения игры
def game_over() :
    #создание объекта шрифта my_font
    my_font = pygame.font.SysFont('times new roman', 50)

    #создание текстовой поверхности, на которой текстбудет нарисовано
    game_over_surface = my_font.render(
        'Your Score is : ' + str(score), True, red)

    game_over_rect = game_over_surface.get_rect()

    #установка положения текста
    game_over_rect.midtop = (window_x / 2, window_y / 4)

    #нарисует текст на экране
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    #через 2 секунды мы выйдем из программы
    time.sleep(2)

    pygame.quit()

    quit()


#функция игры
while True :

    for event in pygame.event.get() :
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_UP :
                change_to = 'UP'
            if event.key == pygame.K_DOWN :
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT :
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT :
                change_to = 'RIGHT'

    #если две клавиши нажаты одновременно
    #мы не хотим, чтобы змея разделялась на две
    #направлений одновременно
    if change_to == 'UP' and direction != 'DOWN' :
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP' :
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT' :
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT' :
        direction = 'RIGHT'

    #перемещение змеи
    if direction == 'UP' :
        snake_position[1] -= 10
    if direction == 'DOWN' :
        snake_position[1] += 10
    if direction == 'LEFT' :
        snake_position[0] -= 10
    if direction == 'RIGHT' :
        snake_position[0] += 10

    #механизм роста тела змеи
    #если фрукты и змеи сталкиваются, то очки
    #будет увеличено на 10
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1] :
        score += 10
        fruit_spawn = False
    else :
        snake_body.pop()

    if not fruit_spawn :
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10]

    fruit_spawn = True
    game_window.fill(black)

    for pos in snake_body :
        pygame.draw.rect(game_window, green,
                         pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))

    #условия окончания игры
    if snake_position[0] < 0 or snake_position[0] > window_x - 10 :
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y - 10 :
        game_over()

    #прикасаясь к телу змеи
    for block in snake_body[1 :] :
        if snake_position[0] == block[0] and snake_position[1] == block[1] :
            game_over()

    #отображение результатов
    show_score(1, white, 'times new roman', 20)

    #обновление экрана
    pygame.display.update()
    fps.tick(snake_speed)