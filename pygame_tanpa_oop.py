import pygame
import random
import sys
from collections import deque

pygame.init()

# ================= KONFIGURASI =================
WIDTH, HEIGHT = 900, 650
BOARD_SIZE = 480
CELL = BOARD_SIZE // 10
MARGIN_TOP = 20
MARGIN_LEFT = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (40, 120, 220)
RED = (220, 60, 60)
GREEN = (60, 170, 80)
ORANGE = (255, 140, 0)
BG = (245, 245, 245)

FONT = pygame.font.SysFont("Arial", 16)
BIG_FONT = pygame.font.SysFont("Arial", 26)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ular Tangga - Non OOP Version")

CLOCK = pygame.time.Clock()
FPS = 60

LADDERS = {3:22, 5:8, 11:26, 20:29, 27:56, 36:44, 51:67, 71:92}
SNAKES = {17:4, 19:7, 21:9, 43:34, 50:30, 62:18, 74:53, 89:68, 95:24, 99:78}

# ================= DATA GAME =================
players = [
    {"name": "Player 1", "color": BLUE, "pos": 1},
    {"name": "Player 2", "color": RED, "pos": 1}
]

current_player = 0
dice_value = 1
move_queue = deque()
game_over = False

panel_x = MARGIN_LEFT + BOARD_SIZE + 30
roll_btn = pygame.Rect(panel_x + 40, 180, 200, 50)

# ================= FUNGSI =================
def get_coordinates(pos):
    idx = pos - 1
    row = idx // 10
    col = idx % 10
    draw_row = 9 - row
    draw_col = col if row % 2 == 0 else 9 - col
    x = MARGIN_LEFT + draw_col * CELL + CELL // 2
    y = MARGIN_TOP + draw_row * CELL + CELL // 2
    return x, y

def draw_board():
    num = 100
    for r in range(10):
        for c in range(10):
            x = MARGIN_LEFT + c * CELL
            y = MARGIN_TOP + r * CELL
            pygame.draw.rect(SCREEN, WHITE, (x, y, CELL, CELL))
            pygame.draw.rect(SCREEN, BLACK, (x, y, CELL, CELL), 1)
            txt = FONT.render(str(num), True, BLACK)
            SCREEN.blit(txt, (x + 5, y + 5))
            num -= 1

    for s, e in LADDERS.items():
        pygame.draw.line(SCREEN, GREEN, get_coordinates(s), get_coordinates(e), 5)

    for s, e in SNAKES.items():
        pygame.draw.line(SCREEN, RED, get_coordinates(s), get_coordinates(e), 5)

def draw_players():
    offsets = [(-10, -8), (10, 8)]
    for i, p in enumerate(players):
        x, y = get_coordinates(p["pos"])
        ox, oy = offsets[i]
        pygame.draw.circle(SCREEN, p["color"], (x + ox, y + oy), 14)

def roll_dice():
    global dice_value
    dice_value = random.randint(1, 6)
    return dice_value

def handle_roll():
    global move_queue
    if game_over or move_queue:
        return

    value = roll_dice()
    player = players[current_player]
    start = player["pos"]
    target = min(100, start + value)

    for p in range(start + 1, target + 1):
        move_queue.append(p)

def update_game():
    global current_player, game_over

    if move_queue:
        players[current_player]["pos"] = move_queue.popleft()

        if not move_queue:
            pos = players[current_player]["pos"]

            if pos in LADDERS:
                players[current_player]["pos"] = LADDERS[pos]
            elif pos in SNAKES:
                players[current_player]["pos"] = SNAKES[pos]

            if players[current_player]["pos"] == 100:
                game_over = True
            else:
                current_player = (current_player + 1) % len(players)

def draw_ui():
    SCREEN.fill(BG)
    draw_board()
    draw_players()

    pygame.draw.rect(SCREEN, (230, 230, 230), (panel_x - 10, 20, 300, 600))

    turn = BIG_FONT.render("Giliran:", True, BLACK)
    SCREEN.blit(turn, (panel_x + 10, 40))

    name = BIG_FONT.render(
        players[current_player]["name"],
        True,
        players[current_player]["color"]
    )
    SCREEN.blit(name, (panel_x + 10, 75))

    pygame.draw.rect(SCREEN, ORANGE, roll_btn, border_radius=8)
    txt = BIG_FONT.render("ROLL DICE", True, WHITE)
    SCREEN.blit(txt, (roll_btn.x + 25, roll_btn.y + 10))

    dice_txt = BIG_FONT.render(f"Dadu: {dice_value}", True, BLACK)
    SCREEN.blit(dice_txt, (panel_x + 50, 260))

    if game_over:
        win = BIG_FONT.render("MENANG!", True, GREEN)
        SCREEN.blit(win, (panel_x + 60, 320))

    pygame.display.update()

# ================= MAIN LOOP =================
def main():
    running = True
    while running:
        CLOCK.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                handle_roll()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if roll_btn.collidepoint(e.pos):
                    handle_roll()

        update_game()
        draw_ui()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
