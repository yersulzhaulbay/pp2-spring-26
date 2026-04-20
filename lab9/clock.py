import pygame
import sys
from datetime import datetime
pygame.init()

WIDTH, HEIGHT = 700, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()

CENTER = (WIDTH // 2, HEIGHT // 2)

bg = pygame.image.load(r"C:\Users\User\Downloads\mickey_body.jpeg").convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

minute_hand = pygame.image.load(r"C:\Users\User\Downloads\hand_right_centered.png").convert_alpha()
second_hand = pygame.image.load(r"C:\Users\User\Downloads\hand_left_centered.png").convert_alpha()

minute_hand = pygame.transform.smoothscale(
    minute_hand,
    (minute_hand.get_width() // 3, minute_hand.get_height() // 3)
)

second_hand = pygame.transform.smoothscale(
    second_hand,
    (second_hand.get_width() // 3, second_hand.get_height() // 3)
)

def rotate_from_edge(image, angle, center):
    rotated = pygame.transform.rotate(image, -angle)

    rect = rotated.get_rect()

    pivot_offset = pygame.math.Vector2(0, rect.height // 2.5)

    rotated_offset = pivot_offset.rotate(angle)

    rect.center = (center[0] - rotated_offset.x,
                   center[1] - rotated_offset.y)

    return rotated, rect

def get_time_angles():
    now = datetime.now()

    seconds = now.second + now.microsecond / 1_000_000
    minutes = now.minute + seconds / 60

    sec_angle = (seconds / 30) * 360
    min_angle = (minutes / 60) * 360

    return sec_angle, min_angle

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(bg, (0, 0))

    sec_angle, min_angle = get_time_angles()

    sec_img, sec_rect = rotate_from_edge(second_hand, sec_angle, CENTER)
    min_img, min_rect = rotate_from_edge(minute_hand, min_angle, CENTER)

    screen.blit(min_img, min_rect)
    screen.blit(sec_img, sec_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()