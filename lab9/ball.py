import pygame
import sys
pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball Game")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)

radius = 50
x = WIDTH // 2
y = HEIGHT // 2

speed = 10

running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
            x -= speed

    if keys[pygame.K_RIGHT]:
            x += speed

    if keys[pygame.K_UP]:
            y -= speed

    if keys[pygame.K_DOWN]:
            y += speed
    pygame.draw.circle(screen, RED, (x, y), radius)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()