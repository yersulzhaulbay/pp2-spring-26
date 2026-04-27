import pygame
import random
import json
import os

pygame.init()

WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
title_font = pygame.font.SysFont(None, 50)

SCORE_FILE = "scores.json"

def load_scores():
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, "r") as f:
                return json.load(f)
        except: return []
    return []

def save_scores(data):
    with open(SCORE_FILE, "w") as f:
        json.dump(data, f)

leaderboard = load_scores()

COIN_W, COIN_H = 45, 29
SQUARE_SIZE = 35

car_img = pygame.transform.scale(pygame.image.load(r"C:\Users\User\Desktop\pictures\car.png"), (110, 110))
coin_img = pygame.transform.scale(pygame.image.load(r"C:\Users\User\Desktop\pictures\coin.png"), (COIN_W, COIN_H))
enemy_img = pygame.transform.scale(pygame.image.load(r"C:\Users\User\Desktop\pictures\enemy.jpg"), (120, 100))
shield_img = pygame.transform.scale(pygame.image.load(r"C:\Users\User\Desktop\pictures\shield.jpg"), (40, 40))
nitro_img = pygame.transform.scale(pygame.image.load(r"C:\Users\User\Desktop\pictures\nitro.png"), (40, 40))

state = "menu"
username = ""
car_x = WIDTH // 2
car_y = HEIGHT - 140
base_speed = 5
car_speed = base_speed

coins = []
enemies = []
powerups = []
slow_zones = []

coin_timer = 0
enemy_timer = 0
power_timer = 0
zone_timer = 0

score = 0      
distance = 0   
pixel_accumulator = 0 
shield_active = False
nitro_end_time = 0
slow_end_time = 0

def draw_button(text, x, y, w, h):
    pygame.draw.rect(screen, (200, 200, 200), (x, y, w, h), border_radius=5)
    t = font.render(text, True, (0, 0, 0))
    rect = t.get_rect(center=(x + w//2, y + h//2))
    screen.blit(t, rect)
    return pygame.Rect(x, y, w, h)

def reset_game():
    global car_x, score, distance, coins, enemies, powerups, slow_zones, pixel_accumulator
    global shield_active, car_speed, nitro_end_time, slow_end_time
    car_x = WIDTH // 2
    score = 0
    distance = 0
    pixel_accumulator = 0
    coins.clear()
    enemies.clear()
    powerups.clear()
    slow_zones.clear()
    shield_active = False
    car_speed = base_speed
    nitro_end_time = 0
    slow_end_time = 0

running = True
while running:
    screen.fill((240, 240, 240))
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN and state == "name":
            if event.key == pygame.K_RETURN and username.strip() != "":
                state = "game"
                reset_game()
            elif event.key == pygame.K_BACKSPACE:
                username = username[:-1]
            else:
                if len(username) < 10:
                    username += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            m_pos = event.pos
            if state == "menu":
                if pygame.Rect(220, 250, 160, 50).collidepoint(m_pos):
                    state = "name" if username == "" else "game"
                    if state == "game": reset_game()
                if pygame.Rect(220, 320, 160, 50).collidepoint(m_pos): state = "leaderboard"
                if pygame.Rect(220, 390, 160, 50).collidepoint(m_pos): running = False
            elif state == "gameover":
                if pygame.Rect(220, 350, 160, 50).collidepoint(m_pos): 
                    state = "game"
                    reset_game()
                if pygame.Rect(220, 420, 160, 50).collidepoint(m_pos): state = "menu"
            elif state == "leaderboard":
                if pygame.Rect(220, 650, 160, 50).collidepoint(m_pos): state = "menu"

    if state == "menu":
        screen.blit(title_font.render("RACER PRO", True, (0,0,0)), (210, 150))
        draw_button("PLAY", 220, 250, 160, 50)
        draw_button("LEADERBOARD", 220, 320, 160, 50)
        draw_button("QUIT", 220, 390, 160, 50)

    elif state == "name":
        screen.blit(font.render("ENTER YOUR NAME:", True, (0,0,0)), (210, 300))
        screen.blit(font.render(username + "|", True, (0,0,255)), (250, 350))
        screen.blit(font.render("Press Enter to Start", True, (150,150,150)), (210, 450))

    elif state == "game":
        difficulty = score // 10 
        current_base = base_speed + (difficulty * 0.3)
        
        if now < nitro_end_time:
            car_speed = current_base * 2
            shield_active = False 
        elif now < slow_end_time:
            car_speed = current_base * 0.5
        else:
            car_speed = current_base

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > 0: car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x < WIDTH - 110: car_x += car_speed

        pixel_accumulator += car_speed
        if pixel_accumulator >= 50:
            distance += int(pixel_accumulator // 50)
            pixel_accumulator %= 50

        car_rect = pygame.Rect(car_x + 30, car_y + 10, 50, 90)

        coin_timer += 1
        if coin_timer > 40:
            val = random.choices([1, 2, 3], weights=[70, 20, 10])[0]
            coins.append({"rect": pygame.Rect(random.randint(0, WIDTH - COIN_W), -50, COIN_W, COIN_H), "value": val})
            coin_timer = 0
        
        enemy_timer += 1
        if enemy_timer > max(15, 60 - difficulty * 2):
            enemies.append({"rect": pygame.Rect(random.randint(0, WIDTH-100), -120, 100, 80), "speed": random.randint(4, 8) + difficulty})
            enemy_timer = 0

        power_timer += 1
        if power_timer > 400:
            p_type = random.choice(["shield", "nitro"])
            powerups.append({"rect": pygame.Rect(random.randint(0, WIDTH-40), -50, 40, 40), "type": p_type})
            power_timer = 0

        zone_timer += 1
        if zone_timer > 300:
            slow_zones.append(pygame.Rect(random.randint(0, WIDTH-100), -100, 100, 100))
            zone_timer = 0

        for z in slow_zones[:]:
            z.y += 4
            s = pygame.Surface((z.width, z.height), pygame.SRCALPHA)
            s.fill((0, 0, 255, 80)) 
            screen.blit(s, (z.x, z.y))
            if car_rect.colliderect(z): slow_end_time = now + 100 
            if z.y > HEIGHT: slow_zones.remove(z)

        for c in coins[:]:
            c["rect"].y += car_speed
            screen.blit(coin_img, (c["rect"].x, c["rect"].y))

            if c["value"] >= 2:
                center_x = c["rect"].centerx
                center_y = c["rect"].centery
                border_rect = pygame.Rect(0, 0, SQUARE_SIZE, SQUARE_SIZE)
                border_rect.center = (center_x, center_y)
                
                color = (255, 215, 0) if c["value"] == 3 else (192, 192, 192)
                pygame.draw.rect(screen, color, border_rect, 2)
                
            if car_rect.colliderect(c["rect"]):
                score += c["value"]
                coins.remove(c)
            elif c["rect"].y > HEIGHT: coins.remove(c)

        for e in enemies[:]:
            e["rect"].y += e["speed"]
            screen.blit(enemy_img, (e["rect"].x, e["rect"].y))
            if car_rect.colliderect(e["rect"]):
                if shield_active:
                    shield_active = False
                    enemies.remove(e)
                else:
                    leaderboard.append({"name": username, "score": score, "distance": distance})
                    leaderboard.sort(key=lambda x: x["score"], reverse=True)
                    save_scores(leaderboard[:10])
                    state = "gameover"
            elif e["rect"].y > HEIGHT: enemies.remove(e)

        for p in powerups[:]:
            p["rect"].y += 5
            img = shield_img if p["type"] == "shield" else nitro_img
            screen.blit(img, (p["rect"].x, p["rect"].y))
            if car_rect.colliderect(p["rect"]):
                if p["type"] == "shield":
                    shield_active = True
                    nitro_end_time = 0 
                else:
                    nitro_end_time = now + 3000 
                    shield_active = False 
                powerups.remove(p)
            elif p["rect"].y > HEIGHT: powerups.remove(p)

        screen.blit(car_img, (car_x, car_y))

        if shield_active:
            surf = pygame.Surface((150, 150), pygame.SRCALPHA)
            pygame.draw.circle(surf, (0, 255, 255, 100), (75, 75), 65, 5)
            screen.blit(surf, (car_x - 20, car_y - 20))
        
        screen.blit(font.render(f"Score: {score}", True, (0,0,0)), (10, 10))
        screen.blit(font.render(f"Distance: {distance}", True, (0,0,0)), (10, 40))
        
        if now < nitro_end_time:
            time_left = (nitro_end_time - now) // 1000 + 1
            screen.blit(font.render(f"NITRO: {time_left}s", True, (255, 69, 0)), (10, 70))
        elif shield_active:
            screen.blit(font.render("SHIELD: READY", True, (0, 150, 255)), (10, 70))

    elif state == "gameover":
        screen.blit(title_font.render("CRASHED!", True, (200, 0, 0)), (220, 200))
        screen.blit(font.render(f"Final Score: {score}", True, (0,0,0)), (200, 260))
        screen.blit(font.render(f"Distance: {distance}", True, (0,0,0)), (200, 290))
        draw_button("RETRY", 220, 350, 160, 50)
        draw_button("MENU", 220, 420, 160, 50)

    elif state == "leaderboard":
        screen.blit(title_font.render("TOP 10", True, (0,0,0)), (240, 100))
        y = 180
        for i, s in enumerate(leaderboard[:10]):
            txt = f"{i+1}. {s['name']} | Score: {s['score']} | Dist: {s['distance']}"
            screen.blit(font.render(txt, True, (50,50,50)), (120, y))
            y += 40
        draw_button("BACK", 220, 650, 160, 50)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()