import pygame
def main():
    #инициализация
    pygame.init()
    #создание экрана
    screen = pygame.display.set_mode((650,500))
    clock = pygame.time.Clock()
    radius = 15
    x = 0
    y = 0
    mode = 'blue' #начальный цвет
    draw_mode = 'line' #режим рисования
    points = [] #список для хранения точек рисования

    #цикл игры
    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT] #проверка на то удерживается ли АЛТ
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL] #проверка на то удерживается ли СТРЛ
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #закрытие окна
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held: #закрытие по Ctrl+W
                    return
                if event.key == pygame.K_F4 and alt_held: #закрытие по Alt+F4
                    return
                if event.key == pygame.K_ESCAPE: #закрытие по ESC
                    return

                #выбор цвета
                if event.key == pygame.K_r: #если 'r' цвет - красный
                    mode = 'red'
                elif event.key == pygame.K_g: #если 'g' цвет - зеленый
                    mode = 'green'
                elif event.key == pygame.K_b:  #если 'b' цвет - синий
                    mode = 'blue'
                elif event.key == pygame.K_e: #если 'e' режим - ластик
                    draw_mode = 'eraser'
                elif event.key == pygame.K_c: #если 'c' режим - круг
                    draw_mode = 'circle'
                elif event.key == pygame.K_t: #если 't' режим - прямоугольник
                    draw_mode = 'rectangle'
                elif event.key == pygame.K_l: #если 'l' режим - линия
                    draw_mode = 'line'
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  #левая кнопка-увеличиваем радиус
                    radius = min(200, radius + 1)
                elif event.button == 3:  #правая кнопка-уменьшаем радиус
                    radius = max(1, radius - 1)
            
            if event.type == pygame.MOUSEMOTION:
                position = event.pos
                points.append((position, draw_mode))
                points = points[-256:]
                
        screen.fill((0, 0, 0)) #черный экран
        for i in range(len(points) - 1):
            drawShape(screen, i, points[i][0], points[i + 1][0], radius, mode, points[i][1])
        pygame.display.flip() #обновляем
        clock.tick(60)
def drawShape(screen, index, start, end, width, color_mode, draw_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))
    
    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)
    else:
        color = (255, 255, 255)  #юелый цвет по умольчанию
    
    if draw_mode == 'eraser':
        color = (0, 0, 0)  #ластик
    
    if draw_mode == 'line':
        pygame.draw.line(screen, color, start, end, width)
    elif draw_mode == 'circle':
        pygame.draw.circle(screen, color, start, width)
    elif draw_mode == 'rectangle':
        rect = pygame.Rect(start[0] - width, start[1] - width, width * 2, width * 2)
        pygame.draw.rect(screen, color, rect)

main()