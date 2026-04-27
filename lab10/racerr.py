import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer with Coins")

clock = pygame.time.Clock()

car_img = pygame.image.load(r"C:\Users\User\Desktop\car.png")
coin_img = pygame.image.load(r"C:\Users\User\Desktop\coin.png")

car_img = pygame.transform.scale(car_img, (100, 100))
coin_img = pygame.transform.scale(coin_img, (50, 30))

car_x = WIDTH // 2 - 25
car_y = HEIGHT - 120
car_speed = 5

coins = []
coin_spawn_delay = 40
coin_timer = 0
score = 0

running = True
while running:
    screen.fill((240, 240, 240))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car_x -= car_speed
    if keys[pygame.K_RIGHT]:
        car_x += car_speed

    car_x = max(0, min(WIDTH - 50, car_x))

    coin_timer += 1
    if coin_timer >= coin_spawn_delay:
        coin_x = random.randint(0, WIDTH - 30)
        coins.append([coin_x, -30])
        coin_timer = 0

    for coin in coins:
        coin[1] += 5

    car_rect = pygame.Rect(car_x, car_y, 50, 100)

    for coin in coins[:]:
        coin_rect = pygame.Rect(coin[0], coin[1], 30, 30)
        if car_rect.colliderect(coin_rect):
            coins.remove(coin)
            score += 1

    screen.blit(car_img, (car_x, car_y))

    for coin in coins:
        screen.blit(coin_img, (coin[0], coin[1]))

    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Coins: {score}", True, (0, 0, 0))
    screen.blit(text, (WIDTH - 120, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()