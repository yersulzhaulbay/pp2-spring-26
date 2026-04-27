import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint App")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen.fill(WHITE)

drawing = False
color = BLACK
mode = "brush"  
start_pos = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                mode = "brush"
            if event.key == pygame.K_r:
                mode = "rect"
            if event.key == pygame.K_c:
                mode = "circle"
            if event.key == pygame.K_e:
                mode = "eraser"
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
                pygame.draw.rect(screen, color, (*start_pos, end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]), 2)
            elif mode == "circle":
                radius = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)**0.5)
                pygame.draw.circle(screen, color, start_pos, radius, 2)

    if drawing:
        mouse_pos = pygame.mouse.get_pos()
        if mode == "brush":
            pygame.draw.circle(screen, color, mouse_pos, 5)
        elif mode == "eraser":
            pygame.draw.circle(screen, WHITE, mouse_pos, 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()