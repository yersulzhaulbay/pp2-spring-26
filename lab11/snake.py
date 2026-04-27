import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Advanced")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
YELLOW = (255, 200, 0)

BLOCK = 20
speed = 3

def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def generate_food():
    size = random.choice([10, 20, 30])
    value = size // 10
    lifetime = random.randint(180, 360)

    return {
        "pos": [
            random.randint(0, WIDTH - size),
            random.randint(0, HEIGHT - size)
        ],
        "size": size,
        "value": value,
        "life": lifetime
    }

def reset():
    snake = [[100.0, 100.0]]
    direction = [speed, 0]
    food = generate_food()
    score = 0
    game_over = False
    grow = 0
    return snake, direction, food, score, game_over, grow

snake, direction, food, score, game_over, grow = reset()

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if restart_btn.collidepoint(event.pos):
                snake, direction, food, score, game_over, grow = reset()

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            direction = [0, -speed]
        if keys[pygame.K_DOWN]:
            direction = [0, speed]
        if keys[pygame.K_LEFT]:
            direction = [-speed, 0]
        if keys[pygame.K_RIGHT]:
            direction = [speed, 0]

        head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
        snake.insert(0, head)

        food["life"] -= 1

        if food["life"] <= 0:
            food = generate_food()

        if distance(head, food["pos"]) < food["size"]:
            score += food["value"]
            grow += food["value"] * 3
            food = generate_food()

        if grow > 0:
            grow -= 1
        else:
            snake.pop()

        if head[0] < 0 or head[0] > WIDTH or head[1] < 0 or head[1] > HEIGHT:
            game_over = True

        for part in snake[5:]:
            if distance(head, part) < 10:
                game_over = True

    for part in snake:
        pygame.draw.rect(screen, GREEN, (part[0], part[1], BLOCK, BLOCK))

    pygame.draw.rect(screen, RED, (*food["pos"], food["size"], food["size"]))

    pygame.draw.rect(screen, YELLOW, (food["pos"][0], food["pos"][1] - 5, food["life"] // 5, 3))

    font = pygame.font.SysFont(None, 30)
    screen.blit(font.render(f"Score: {score}", True, BLACK), (10, 10))

    if game_over:
        big = pygame.font.SysFont(None, 60)
        screen.blit(big.render("GAME OVER", True, RED), (WIDTH//2 - 150, HEIGHT//2 - 80))

        restart_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 50)
        pygame.draw.rect(screen, GRAY, restart_btn)

        screen.blit(font.render("Restart", True, BLACK), (restart_btn.x + 55, restart_btn.y + 12))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()