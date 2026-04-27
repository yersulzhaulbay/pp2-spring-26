import pygame
import math
from collections import deque
from datetime import datetime

pygame.init()

WIDTH, HEIGHT = 800, 600
PALETTE_HEIGHT = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Full")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

colors = [
    (0,0,0), (255,255,255), (255,0,0), (0,255,0), (0,0,255),
    (255,255,0), (255,165,0), (128,0,128), (0,255,255), (128,128,128)
]

color = BLACK

screen.fill(WHITE)

drawing = False
start_pos = None
last_pos = None
mode = "pencil"
brush_size = 5

font = pygame.font.SysFont(None, 30)
text_mode = False
text_input = ""
text_pos = (0, 0)

preview_surface = pygame.Surface((WIDTH, HEIGHT))
preview_surface.fill(BLACK)

undo_stack = []

def save_state():
    if len(undo_stack) > 20:
        undo_stack.pop(0)
    undo_stack.append(preview_surface.copy())

def draw_palette():
    for i, col in enumerate(colors):
        rect = pygame.Rect(i*50, 0, 50, PALETTE_HEIGHT)
        pygame.draw.rect(screen, col, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

def draw_circle(surf, start, end, color, width):
    radius = int(((end[0]-start[0])**2 + (end[1]-start[1])**2) ** 0.5)
    pygame.draw.circle(surf, color, start, radius, width)

def draw_rect(surf, start, end, color, width):
    rect = pygame.Rect(start[0], start[1], end[0]-start[0], end[1]-start[1])
    pygame.draw.rect(surf, color, rect, width)

def draw_square(surf, start, end, color, width):
    size = min(abs(end[0]-start[0]), abs(end[1]-start[1]))
    rect = pygame.Rect(start[0], start[1], size, size)
    pygame.draw.rect(surf, color, rect, width)

def draw_line(surf, start, end, color, width):
    pygame.draw.line(surf, color, start, end, width)

def draw_right_triangle(surf, start, end, color, width):
    points = [(start[0], start[1]+PALETTE_HEIGHT),
              (start[0], end[1]),
              (end[0], end[1])]
    pygame.draw.polygon(surf, color, points, width)

def draw_equilateral_triangle(surf, start, end, color, width):
    x1, y1 = start
    x2, y2 = end
    side = abs(x2 - x1)
    height = side * math.sqrt(3) / 2

    points = [
        (x1, y1),
        (x2, y1),
        ((x1 + x2) / 2, y1 - height)
    ]
    pygame.draw.polygon(surf, color, points, width)

def draw_rhombus(surf, start, end, color, width):
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
    pygame.draw.polygon(surf, color, points, width)

def flood_fill(surface, x, y, new_color):
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return

    queue = deque([(x, y)])
    while queue:
        px, py = queue.popleft()

        if px < 0 or px >= WIDTH or py < PALETTE_HEIGHT or py >= HEIGHT:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), new_color)

        queue.append((px+1, py))
        queue.append((px-1, py))
        queue.append((px, py+1))
        queue.append((px, py-1))


running = True
while running:
    screen.fill(WHITE)
    screen.blit(preview_surface, (0, 0))

    draw_palette()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: mode = "pencil"
            if event.key == pygame.K_l: mode = "line"
            if event.key == pygame.K_e: mode = "eraser"
            if event.key == pygame.K_i: mode = "picker"
            if event.key == pygame.K_f: mode = "fill"
            if event.key == pygame.K_t: mode = "text"

            if event.key == pygame.K_r: mode = "rect"
            if event.key == pygame.K_c: mode = "circle"
            if event.key == pygame.K_q: mode = "square"
            if event.key == pygame.K_y: mode = "right_triangle"
            if event.key == pygame.K_u: mode = "equilateral_triangle"
            if event.key == pygame.K_h: mode = "rhombus"

            if event.key == pygame.K_1: brush_size = 2
            if event.key == pygame.K_2: brush_size = 5
            if event.key == pygame.K_3: brush_size = 10

            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                filename = datetime.now().strftime("drawing_%Y%m%d_%H%M%S.png")
                pygame.image.save(preview_surface, filename)

            if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if undo_stack:
                    preview_surface = undo_stack.pop()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if y < PALETTE_HEIGHT:
                index = x // 50
                if index < len(colors):
                    color = colors[index]
                continue

            drawing = True
            start_pos = event.pos
            last_pos = event.pos

            save_state()

            if mode == "picker":
                color = preview_surface.get_at(event.pos)

            if mode == "fill":
                flood_fill(preview_surface, x, y, color)

            if mode == "text":
                text_mode = True
                text_input = ""
                text_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            if mode == "line":
                draw_line(preview_surface, start_pos, end_pos, color, brush_size)
            elif mode == "rect":
                draw_rect(preview_surface, start_pos, end_pos, color, brush_size)
            elif mode == "circle":
                draw_circle(preview_surface, start_pos, end_pos, color, brush_size)
            elif mode == "square":
                draw_square(preview_surface, start_pos, end_pos, color, brush_size)
            elif mode == "right_triangle":
                draw_right_triangle(preview_surface, start_pos, end_pos, color, brush_size)
            elif mode == "equilateral_triangle":
                draw_equilateral_triangle(preview_surface, start_pos, end_pos, color, brush_size)
            elif mode == "rhombus":
                draw_rhombus(preview_surface, start_pos, end_pos, color, brush_size)

    if drawing:
        mouse = pygame.mouse.get_pos()

        if mode == "pencil":
            pygame.draw.line(preview_surface, color, last_pos, mouse, brush_size)
            last_pos = mouse

        elif mode == "eraser":
            pygame.draw.circle(preview_surface, WHITE, mouse, brush_size)

        elif mode == "line":
            screen.blit(preview_surface, (0, 0))
            draw_line(screen, start_pos, mouse, color, brush_size)

        elif mode == "rect":
            screen.blit(preview_surface, (0, 0))
            draw_rect(screen, start_pos, mouse, color, brush_size)

        elif mode == "circle":
            screen.blit(preview_surface, (0, 0))
            draw_circle(screen, start_pos, mouse, color, brush_size)

        elif mode == "square":
            screen.blit(preview_surface, (0, 0))
            draw_square(screen, start_pos, mouse, color, brush_size)

        elif mode == "right_triangle":
            screen.blit(preview_surface, (0, 0))
            draw_right_triangle(screen, start_pos, mouse, color, brush_size)

        elif mode == "equilateral_triangle":
            screen.blit(preview_surface, (0, 0))
            draw_equilateral_triangle(screen, start_pos, mouse, color, brush_size)

        elif mode == "rhombus":
            screen.blit(preview_surface, (0, 0))
            draw_rhombus(screen, start_pos, mouse, color, brush_size)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()