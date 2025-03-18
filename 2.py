import pygame
import os

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Simple Music Player")

mus_files = ["pp.mp3", "cc.mp3"]  

for mus_file in mus_files:
    if not os.path.exists(mus_file):
        print(f"Ошибка: Файл '{mus_file}' не найден!")
        exit()

track_index = 0

#воспроизведение музыки
def play_music():
    pygame.mixer.music.load(mus_files[track_index])
    pygame.mixer.music.play()
    print(f"Playing: {mus_files[track_index]}")

#остановка музыки
def stop_music():
    pygame.mixer.music.stop()
    print("Music Stopped")

def next_track():
    global track_index
    track_index = (track_index + 1) % len(mus_files)  
    play_music()

#переключение на предыдущий трек
def previous_track():
    global track_index
    track_index = (track_index - 1) % len(mus_files) 
    play_music()

is_playing = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  #p воспроизведение
                if not is_playing:
                    play_music()
                    is_playing = True
            elif event.key == pygame.K_s:  #s остановка
                stop_music()
                is_playing = False
            elif event.key == pygame.K_n:  #n следующий трек
                next_track()
            elif event.key == pygame.K_b:  #b предыдущий трек
                previous_track()

    pygame.display.flip()

pygame.quit()
