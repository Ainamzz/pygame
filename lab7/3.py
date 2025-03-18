import pygame

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ball")

ball_radius = 25
ball_x = screen_width // 2  
ball_y = screen_height // 2

#red color
ball_color = (255, 0, 0)

#white
bg_color = (255, 255, 255)

speed = 20

running = True
while running:
    screen.fill(bg_color)  

    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        if ball_y - ball_radius > 0:  #чтобы мяч не выходил за верхней границей
            ball_y -= speed
    if keys[pygame.K_DOWN]:
        if ball_y + ball_radius < screen_height:  #чтобы мяч не выходил за нижней границей
            ball_y += speed
    if keys[pygame.K_LEFT]:
        if ball_x - ball_radius > 0:  #левая граница
            ball_x -= speed
    if keys[pygame.K_RIGHT]:
        if ball_x + ball_radius < screen_width:  #правая граница
            ball_x += speed

    pygame.display.flip()

    pygame.time.Clock().tick(60)
pygame.quit()
