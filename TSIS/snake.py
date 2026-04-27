import pygame
import random
import math
import json
import os
import psycopg2
from datetime import datetime


DB_PARAMS = {
    "dbname": "snake",
    "user": "postgres",
    "password": "123456",
    "host": "127.0.0.1",
    "port": "5432"
}


pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Smooth & Timed")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 60)
small_font = pygame.font.SysFont(None, 20)


WHITE, BLACK, RED, GREEN = (255, 255, 255), (0, 0, 0), (200, 0, 0), (0, 200, 0)
GRAY, YELLOW, PURPLE = (150, 150, 150), (255, 200, 0), (128, 0, 128)
DARK_RED = (139, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)

POWERUP_COLORS = {"speed": YELLOW, "slow": PURPLE, "shield": CYAN}


DEFAULT_SETTINGS = {"snake_color": [0, 200, 0], "grid_on": True}

def load_settings():
    if os.path.exists("settings.json"):
        try:
            with open("settings.json", "r") as f: return json.load(f)
        except: return DEFAULT_SETTINGS
    return DEFAULT_SETTINGS

def save_settings(data):
    with open("settings.json", "w") as f: json.dump(data, f)

settings = load_settings()


def db_query(query, params=(), fetch=False):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute(query, params)
        res = cur.fetchall() if fetch else None
        conn.commit()
        cur.close()
        conn.close()
        return res
    except: return []

def get_personal_best(name):
    res = db_query("SELECT MAX(score) FROM game_sessions JOIN players ON players.id = game_sessions.player_id WHERE username = %s", (name,), True)
    return res[0][0] if res and res[0][0] else 0


BLOCK = 20
BASE_SPEED = 3.0 

def generate_pos(forbidden=[], snake_head=None, obstacles=[]):
    while True:
        pos = [random.randrange(0, WIDTH - BLOCK, BLOCK), random.randrange(0, HEIGHT - BLOCK, BLOCK)]
        if pos in forbidden: continue
        test_rect = pygame.Rect(pos[0], pos[1], BLOCK, BLOCK)
        if any(test_rect.colliderect(obs) for obs in obstacles): continue
        if snake_head:
            if math.hypot(pos[0] - snake_head[0], pos[1] - snake_head[1]) < 120: continue
        return pos

def reset_game(username):
    snake = [[200.0, 200.0]]
    for i in range(1, int((BLOCK*3)/BASE_SPEED)):
        snake.append([200.0 - i*BASE_SPEED, 200.0])
    return {
        "snake": snake,
        "target_dir": [1, 0],
        "food": {"pos": generate_pos(snake), "spawn_time": pygame.time.get_ticks(), "life": 7000, "val": random.randint(1, 3)},
        "poison": {"pos": generate_pos(snake), "spawn_time": pygame.time.get_ticks(), "life": 10000},
        "powerup": None,
        "obstacles": [],
        "score": 0,
        "level": 1,
        "grow": 0,
        "game_over": False,
        "pb": get_personal_best(username),
        "power_timer": 0,
        "shield": False,
        "speed_mod": 1.0
    }

def update_level(g):
    new_level = (g["score"] // 5) + 1
    if new_level > g["level"]:
        g["level"] = new_level
        if g["level"] >= 3:
            for _ in range(2):
                w, h = (BLOCK * 5, BLOCK // 2) if random.random() > 0.5 else (BLOCK // 2, BLOCK * 5)
                pos = generate_pos(g["snake"], g["snake"][0], g["obstacles"])
                g["obstacles"].append(pygame.Rect(pos[0], pos[1], w, h))

def main_menu(saved_name=""):
    name = saved_name
    while True:
        screen.fill(WHITE)
        screen.blit(big_font.render("SNAKE SMOOTH", True, BLACK), (WIDTH//2-150, 80))
        name_txt = font.render(f"Enter Name: {name}|", True, BLUE)
        screen.blit(name_txt, (WIDTH//2-100, 160))
        btns = [
            (pygame.Rect(WIDTH//2-100, 220, 200, 40), "PLAY"),
            (pygame.Rect(WIDTH//2-100, 280, 200, 40), "LEADERBOARD"),
            (pygame.Rect(WIDTH//2-100, 340, 200, 40), "SETTINGS"),
            (pygame.Rect(WIDTH//2-100, 400, 200, 40), "QUIT")
        ]
        for btn, text in btns:
            pygame.draw.rect(screen, GRAY, btn)
            txt_surf = font.render(text, True, BLACK)
            screen.blit(txt_surf, (btn.x + (btn.w - txt_surf.get_width())//2, btn.y + 10))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE: name = name[:-1]
                elif event.key == pygame.K_RETURN and name: return ("game", name)
                elif len(name) < 15 and event.unicode.isalnum(): name += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btns[0][0].collidepoint(event.pos) and name: return ("game", name)
                if btns[1][0].collidepoint(event.pos): return ("leaderboard", name)
                if btns[2][0].collidepoint(event.pos): return ("settings", name)
                if btns[3][0].collidepoint(event.pos): return None

def game_over_screen(g):
    while True:
        screen.fill(WHITE)
        screen.blit(big_font.render("GAME OVER", True, RED), (WIDTH//2-130, 100))
        stats = [f"Score: {g['score']}", f"Level: {g['level']}", f"Best: {max(g['score'], g['pb'])}"]
        for i, t in enumerate(stats): screen.blit(font.render(t, True, BLACK), (WIDTH//2-60, 180 + i*40))
        b_retry = pygame.Rect(WIDTH//2-110, 330, 220, 40)
        b_menu = pygame.Rect(WIDTH//2-110, 390, 220, 40)
        pygame.draw.rect(screen, GRAY, b_retry); pygame.draw.rect(screen, GRAY, b_menu)
        screen.blit(font.render("RETRY", True, BLACK), (b_retry.x+75, b_retry.y+10))
        screen.blit(font.render("MAIN MENU", True, BLACK), (b_menu.x+55, b_menu.y+10))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b_retry.collidepoint(event.pos): return "retry"
                if b_menu.collidepoint(event.pos): return "menu"

def leaderboard_screen(user):
    top = db_query("SELECT p.username, s.score, s.level_reached FROM game_sessions s JOIN players p ON p.id = s.player_id ORDER BY score DESC LIMIT 10", fetch=True)
    while True:
        screen.fill(WHITE)
        screen.blit(big_font.render("LEADERBOARD", True, BLACK), (WIDTH//2-160, 50))
        btn_back = pygame.Rect(WIDTH//2-100, 500, 200, 40)
        pygame.draw.rect(screen, GRAY, btn_back)
        screen.blit(font.render("BACK", True, BLACK), (btn_back.x+75, btn_back.y+10))
        for i, r in enumerate(top):
            screen.blit(font.render(f"{i+1}. {r[0][:12]:<12} {r[1]:<5} Lvl:{r[2]}", True, BLACK), (150, 140+i*30))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and btn_back.collidepoint(event.pos): return "menu"

def settings_screen(user):
    global settings
    colors = {"Green": [0,200,0], "Blue": [0,0,200], "Red": [200,0,0], "Cyan": [0,200,200]}
    c_list = list(colors.keys())
    while True:
        screen.fill(WHITE)
        screen.blit(big_font.render("SETTINGS", True, BLACK), (WIDTH//2-110, 50))
        b_grid = pygame.Rect(WIDTH//2-100, 150, 200, 40)
        b_color = pygame.Rect(WIDTH//2-100, 220, 200, 40)
        b_save = pygame.Rect(WIDTH//2-100, 350, 200, 40)
        pygame.draw.rect(screen, GRAY if settings["grid_on"] else RED, b_grid)
        pygame.draw.rect(screen, GRAY, b_color); pygame.draw.rect(screen, GREEN, b_save)
        screen.blit(font.render(f"Grid: {'ON' if settings['grid_on'] else 'OFF'}", True, BLACK), (b_grid.x+20, b_grid.y+10))
        curr_c = next((k for k, v in colors.items() if v == settings["snake_color"]), "Custom")
        screen.blit(font.render(f"Color: {curr_c}", True, BLACK), (b_color.x+20, b_color.y+10))
        screen.blit(font.render("SAVE & BACK", True, BLACK), (b_save.x+40, b_save.y+10))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b_grid.collidepoint(event.pos): settings["grid_on"] = not settings["grid_on"]
                if b_color.collidepoint(event.pos):
                    idx = (c_list.index(curr_c) + 1) % len(c_list) if curr_c in c_list else 0
                    settings["snake_color"] = colors[c_list[idx]]
                if b_save.collidepoint(event.pos): save_settings(settings); return "menu"


def play_game(username):
    g = reset_game(username)
    while not g["game_over"]:
        now = pygame.time.get_ticks()
        screen.fill(WHITE)
        if settings.get("grid_on", True):
            for x in range(0, WIDTH, BLOCK): pygame.draw.line(screen, (240, 240, 240), (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, BLOCK): pygame.draw.line(screen, (240, 240, 240), (0, y), (WIDTH, y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return None

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and g["target_dir"] != [0, 1]: g["target_dir"] = [0, -1]
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and g["target_dir"] != [0, -1]: g["target_dir"] = [0, 1]
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and g["target_dir"] != [1, 0]: g["target_dir"] = [-1, 0]
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and g["target_dir"] != [-1, 0]: g["target_dir"] = [1, 0]

        speed = BASE_SPEED * g["speed_mod"]
        head = [g["snake"][0][0] + g["target_dir"][0] * speed, g["snake"][0][1] + g["target_dir"][1] * speed]
        h_rect = pygame.Rect(head[0]+4, head[1]+4, BLOCK-8, BLOCK-8) 
        
        if head[0] < 0 or head[0] > WIDTH-BLOCK or head[1] < 0 or head[1] > HEIGHT-BLOCK:
            if g["shield"]: g["shield"] = False; head = [WIDTH//2, HEIGHT//2]
            else: g["game_over"] = True

        for obs in g["obstacles"]:
            if h_rect.colliderect(obs):
                if g["shield"]: g["shield"] = False; g["obstacles"].remove(obs)
                else: g["game_over"] = True


        neck_offset = int(BLOCK * 2.5 / speed) 
        for p in g["snake"][neck_offset:]:
            if h_rect.colliderect(pygame.Rect(p[0], p[1], BLOCK-2, BLOCK-2)):
                if g["shield"]: g["shield"] = False; break
                else: g["game_over"] = True

        g["snake"].insert(0, head)

        
        for item, color in [(g["food"], RED), (g["poison"], DARK_RED)]:
            elapsed = now - item["spawn_time"]
            percent = max(0, (item["life"] - elapsed) / item["life"])
            pygame.draw.rect(screen, color, (*item["pos"], BLOCK, BLOCK))
            pygame.draw.rect(screen, GRAY, (item["pos"][0], item["pos"][1]-8, BLOCK, 4))
            pygame.draw.rect(screen, color, (item["pos"][0], item["pos"][1]-8, int(BLOCK * percent), 4))

        if h_rect.colliderect(pygame.Rect(*g["food"]["pos"], BLOCK, BLOCK)):
            g["score"] += g["food"]["val"]; g["grow"] += int((BLOCK/speed)*g["food"]["val"])
            g["food"] = {"pos": generate_pos(g["snake"], None, g["obstacles"]), "spawn_time": now, "life": 7000, "val": random.randint(1,3)}
            update_level(g)
        
        if h_rect.colliderect(pygame.Rect(*g["poison"]["pos"], BLOCK, BLOCK)):
            rem = int((BLOCK*2)/speed)
            if len(g["snake"]) <= rem + 10: g["game_over"] = True
            else: g["snake"] = g["snake"][:-rem]; g["grow"] = 0
            g["poison"] = {"pos": generate_pos(g["snake"], None, g["obstacles"]), "spawn_time": now, "life": 10000}

        if now - g["food"]["spawn_time"] > g["food"]["life"]:
            g["food"] = {"pos": generate_pos(g["snake"], None, g["obstacles"]), "spawn_time": now, "life": 7000, "val": random.randint(1,3)}
        if now - g["poison"]["spawn_time"] > g["poison"]["life"]:
            g["poison"] = {"pos": generate_pos(g["snake"], None, g["obstacles"]), "spawn_time": now, "life": 10000}

        if g["grow"] > 0: g["grow"] -= 1
        else: g["snake"].pop()

        if not g["powerup"] and random.random() < 0.005:
            g["powerup"] = {"pos": generate_pos(g["snake"], None, g["obstacles"]), "type": random.choice(["speed", "slow", "shield"]), "end": now + 8000}
        if g["powerup"]:
            pygame.draw.circle(screen, POWERUP_COLORS[g["powerup"]["type"]], (g["powerup"]["pos"][0]+10, g["powerup"]["pos"][1]+10), 10)
            if h_rect.colliderect(pygame.Rect(*g["powerup"]["pos"], BLOCK, BLOCK)):
                if g["powerup"]["type"] == "speed": g["speed_mod"] = 1.7; g["power_timer"] = now + 5000
                elif g["powerup"]["type"] == "slow": g["speed_mod"] = 0.6; g["power_timer"] = now + 5000
                else: g["shield"] = True
                g["powerup"] = None
            elif now > g["powerup"]["end"]: g["powerup"] = None
        if g["speed_mod"] != 1.0 and now > g["power_timer"]: g["speed_mod"] = 1.0

        for obs in g["obstacles"]: pygame.draw.rect(screen, BLACK, obs)
        for i, p in enumerate(g["snake"]):
            if i % 4 == 0: pygame.draw.rect(screen, settings["snake_color"], (p[0], p[1], BLOCK-2, BLOCK-2))
        
        screen.blit(font.render(f"Score: {g['score']} | Lvl: {g['level']}", True, BLACK), (10, 10))
        if g["shield"]: pygame.draw.circle(screen, CYAN, (int(g["snake"][0][0])+10, int(g["snake"][0][1])+10), 15, 2)
        pygame.display.flip()
        clock.tick(60)

    res = db_query("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO UPDATE SET username=EXCLUDED.username RETURNING id", (username,), True)
    if res: db_query("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)", (res[0][0], g["score"], g["level"]))
    return g

def start():
    state, user = "menu", ""
    stats = None
    while True:
        if state == "menu":
            res = main_menu(user)
            if not res: break
            state, user = res
        elif state == "game":
            stats = play_game(user)
            if not stats: break
            state = "gameover"
        elif state == "gameover":
            c = game_over_screen(stats)
            state = "menu" if c == "menu" else ("game" if c == "retry" else "quit")
            if state == "quit": break
        elif state == "leaderboard": state = leaderboard_screen(user)
        elif state == "settings": state = settings_screen(user)
    pygame.quit()

if __name__ == "__main__":
    start()