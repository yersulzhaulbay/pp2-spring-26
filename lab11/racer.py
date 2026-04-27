import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Advanced")

clock = pygame.time.Clock()

car_img = pygame.image.load(r"C:\Users\User\Desktop\car.png")
coin_img = pygame.image.load(r"C:\Users\User\Desktop\coin.png")
enemy_img = pygame.image.load(r"C:\Users\User\Desktop\enemy.jpg")

car_img = pygame.transform.scale(car_img, (100, 100))
coin_img = pygame.transform.scale(coin_img, (45, 25))
enemy_img = pygame.transform.scale(enemy_img, (120, 100))
 
car_x = WIDTH // 2 - 25
car_y = HEIGHT - 120
car_speed = 5

coins = []
coin_timer = 0

enemy_x = random.randint(0, WIDTH - 50)
enemy_y = -200
enemy_speed = 4

score = 0
collected = 0

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
    if coin_timer > 40:
        size = random.choice([15, 20, 30])
        value = size // 10

        coins.append({
            "x": random.randint(0, WIDTH - size),
            "y": -20,
            "size": size,
            "value": value
        })

        coin_timer = 0

    for coin in coins:
        coin["y"] += 5

    car_rect = pygame.Rect(car_x, car_y, 50, 100)

    for coin in coins[:]:
        rect = pygame.Rect(coin["x"], coin["y"], coin["size"], coin["size"])

        if car_rect.colliderect(rect):
            score += coin["value"]
            collected += coin["value"]
            coins.remove(coin)

    enemy_y += enemy_speed

    if enemy_y > HEIGHT:
        enemy_y = -200
        enemy_x = random.randint(0, WIDTH - 50)

    enemy_rect = pygame.Rect(enemy_x, enemy_y, 50, 100)

    if car_rect.colliderect(enemy_rect):
        running = False

    if collected >= 5:
        enemy_speed += 1
        collected = 0

    screen.blit(car_img, (car_x, car_y))
    screen.blit(enemy_img, (enemy_x, enemy_y))

    for coin in coins:
        screen.blit(coin_img, (coin["x"], coin["y"]))

    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()