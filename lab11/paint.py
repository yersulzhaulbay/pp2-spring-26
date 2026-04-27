import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Full")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen.fill(WHITE)

drawing = False
start_pos = None
color = BLACK
mode = "brush"

def draw_circle(surf, start, end, color):
    radius = int(((end[0]-start[0])**2 + (end[1]-start[1])**2) ** 0.5)
    pygame.draw.circle(surf, color, start, radius, 2)

def draw_rect(surf, start, end, color):
    rect = pygame.Rect(start[0], start[1], end[0]-start[0], end[1]-start[1])
    pygame.draw.rect(surf, color, rect, 2)

def draw_square(surf, start, end, color):
    size = min(abs(end[0]-start[0]), abs(end[1]-start[1]))
    rect = pygame.Rect(start[0], start[1], size, size)
    pygame.draw.rect(surf, color, rect, 2)

def draw_right_triangle(surf, start, end, color):
    points = [start, (start[0], end[1]), end]
    pygame.draw.polygon(surf, color, points, 2)

def draw_equilateral_triangle(surf, start, end, color):
    x1, y1 = start
    x2, y2 = end
    side = abs(x2 - x1)
    height = side * math.sqrt(3) / 2
    points = [
        (x1, y1),
        (x2, y1),
        ((x1 + x2) / 2, y1 - height)
    ]
    pygame.draw.polygon(surf, color, points, 2)

def draw_rhombus(surf, start, end, color):
    x1, y1 = start
    x2, y2 = end
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    points = [
        (cx, y1),
        (x2, cy),
        (cx, y2),
        (x1, cy)
    ]
    pygame.draw.polygon(surf, color, points, 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_b:
                mode = "brush"
            if event.key == pygame.K_e:
                mode = "eraser"

            if event.key == pygame.K_r:
                mode = "rect"
            if event.key == pygame.K_c:
                mode = "circle"

            if event.key == pygame.K_s:
                mode = "square"
            if event.key == pygame.K_t:
                mode = "triangle"
            if event.key == pygame.K_y:
                mode = "right_triangle"
            if event.key == pygame.K_h:
                mode = "rhombus"

            if event.key == pygame.K_1:
                color = (255, 0, 0)
            if event.key == pygame.K_2:
                color = (0, 255, 0)
            if event.key == pygame.K_3:
                color = (0, 0, 255)

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            if mode == "rect":
                draw_rect(screen, start_pos, end_pos, color)

            elif mode == "circle":
                draw_circle(screen, start_pos, end_pos, color)

            elif mode == "square":
                draw_square(screen, start_pos, end_pos, color)

            elif mode == "triangle":
                draw_equilateral_triangle(screen, start_pos, end_pos, color)

            elif mode == "right_triangle":
                draw_right_triangle(screen, start_pos, end_pos, color)

            elif mode == "rhombus":
                draw_rhombus(screen, start_pos, end_pos, color)

    if drawing:
        mouse = pygame.mouse.get_pos()

        if mode == "brush":
            pygame.draw.circle(screen, color, mouse, 5)

        elif mode == "eraser":
            pygame.draw.circle(screen, WHITE, mouse, 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()