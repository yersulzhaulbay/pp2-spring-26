import pygame
import sys
import os
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

playlist = [
    r"C:\Users\User\Downloads\Ернар Амандық - Кейіпкер-Keipker.mp3",
    r"C:\Users\User\Downloads\Ernar_Amandyq_Meni_kut.mp3",
    r"C:\Users\User\Downloads\Ernar Amandyq - Жақыным.mp3"
]

current_track = 0
is_playing = False
is_paused = False


def load_track(index):
    pygame.mixer.music.load(playlist[index])

def play():
    global is_playing, is_paused
    if is_paused:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.play()

    is_playing = True
    is_paused = False


def pause():
    global is_playing, is_paused
    pygame.mixer.music.pause()
    is_paused = True
    is_playing = False


def stop():
    global is_playing, is_paused
    pygame.mixer.music.stop()
    is_playing = False
    is_paused = False


def next_track():
    global current_track
    current_track = (current_track + 1) % len(playlist)
    load_track(current_track)
    play()


def prev_track():
    global current_track
    current_track = (current_track - 1) % len(playlist)
    load_track(current_track)
    play()

load_track(current_track)

running = True
while running:
    screen.fill((255, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                play()        
            elif event.key == pygame.K_p:
                pause()      
            elif event.key == pygame.K_n:
                next_track()
            elif event.key == pygame.K_b:
                prev_track()
            elif event.key == pygame.K_q:
                running = False

    track_name = os.path.basename(playlist[current_track])

    if is_paused:
        status = "Paused"
    elif is_playing:
        status = "Playing"
    else:
        status = "Stopped"

    pos = pygame.mixer.music.get_pos() / 1000
    time_text = f"Time: {round(pos, 1)}s"

    text1 = font.render(f"Track: {track_name}", True, (255, 255, 255))
    text2 = font.render(f"Status: {status}", True, (200, 200, 200))
    text3 = font.render(time_text, True, (180, 180, 180))
    text4 = font.render("R=Resume P=Pause N=Next B=Back Q=Quit", True, (150, 150, 150))

    screen.blit(text1, (20, 40))
    screen.blit(text2, (20, 90))
    screen.blit(text3, (20, 140))
    screen.blit(text4, (20, 220))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()