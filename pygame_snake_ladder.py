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
pygame.display.set_caption("Ular Tangga - OOP Version")

CLOCK = pygame.time.Clock()
FPS = 60

LADDERS = {3:22, 5:8, 11:26, 20:29, 27:56, 36:44, 51:67, 71:92}
SNAKES = {17:4, 19:7, 21:9, 43:34, 50:30, 62:18, 74:53, 89:68, 95:24, 99:78}


# ================= BASE CLASS =================
class GameObject:
    def __init__(self, position):
        self._position = position  

    def get_position(self):
        return self._position

    def set_position(self, pos):
        self._position = pos

    def draw(self, screen):
        pass   


# ================= PLAYER =================
class Player(GameObject):
    def __init__(self, name, color):
        super().__init__(1)
        self.name = name
        self.color = color

    def draw(self, screen, board, offset):
        x, y = board.get_coordinates(self._position)
        ox, oy = offset
        pygame.draw.circle(
            screen, self.color, (x + ox, y + oy), 14
        )


# ================= BOARD =================
class Board:
    def get_coordinates(self, pos):
        idx = pos - 1
        row = idx // 10
        col = idx % 10
        draw_row = 9 - row
        draw_col = col if row % 2 == 0 else 9 - col
        x = MARGIN_LEFT + draw_col * CELL + CELL // 2
        y = MARGIN_TOP + draw_row * CELL + CELL // 2
        return x, y

    def draw(self, screen):
        num = 100
        for r in range(10):
            for c in range(10):
                x = MARGIN_LEFT + c * CELL
                y = MARGIN_TOP + r * CELL
                pygame.draw.rect(screen, WHITE, (x, y, CELL, CELL))
                pygame.draw.rect(screen, BLACK, (x, y, CELL, CELL), 1)
                txt = FONT.render(str(num), True, BLACK)
                screen.blit(txt, (x + 5, y + 5))
                num -= 1

        for s, e in LADDERS.items():
            pygame.draw.line(
                screen, GREEN,
                self.get_coordinates(s),
                self.get_coordinates(e), 5
            )

        for s, e in SNAKES.items():
            pygame.draw.line(
                screen, RED,
                self.get_coordinates(s),
                self.get_coordinates(e), 5
            )


# ================= DICE =================
class Dice:
    def __init__(self):
        self.value = 1

    def roll(self):
        self.value = random.randint(1, 6)
        return self.value


# ================= GAME =================
class Game:
    def __init__(self):
        self.board = Board()
        self.dice = Dice()
        self.players = [
            Player("Player 1", BLUE),
            Player("Player 2", RED),
            Player("Player 3", ORANGE)
        ]
        self.current = 0
        self.move_queue = deque()
        self.game_over = False

        # tombol dice
        panel_x = MARGIN_LEFT + BOARD_SIZE + 30
        self.roll_btn = pygame.Rect(panel_x + 40, 180, 200, 50)

    def next_turn(self):
        self.current = (self.current + 1) % len(self.players)

    def handle_roll(self):
        if self.game_over or self.move_queue:
            return

        value = self.dice.roll()
        player = self.players[self.current]
        start = player.get_position()
        target = min(100, start + value)

        for p in range(start + 1, target + 1):
            self.move_queue.append(p)

    def update(self):
        if self.move_queue:
            player = self.players[self.current]
            player.set_position(self.move_queue.popleft())

            if not self.move_queue:
                pos = player.get_position()
                if pos in LADDERS:
                    player.set_position(LADDERS[pos])
                elif pos in SNAKES:
                    player.set_position(SNAKES[pos])

                if player.get_position() == 100:
                    self.game_over = True
                else:
                    self.next_turn()

    def draw(self):
        SCREEN.fill(BG)
        self.board.draw(SCREEN)

        offsets = [(-10, -8), (10, 8), (10, 2)]
        for i, p in enumerate(self.players):
            p.draw(SCREEN, self.board, offsets[i])

        # ===== PANEL KANAN =====
        panel_x = MARGIN_LEFT + BOARD_SIZE + 20
        pygame.draw.rect(SCREEN, (230, 230, 230), (panel_x, 20, 300, 600))

        turn = BIG_FONT.render("Giliran:", True, BLACK)
        SCREEN.blit(turn, (panel_x + 20, 40))

        name = BIG_FONT.render(
            self.players[self.current].name,
            True,
            self.players[self.current].color
        )
        SCREEN.blit(name, (panel_x + 20, 75))

        pygame.draw.rect(SCREEN, ORANGE, self.roll_btn, border_radius=8)
        txt = BIG_FONT.render("ROLL DICE", True, WHITE)
        SCREEN.blit(txt, (self.roll_btn.x + 25, self.roll_btn.y + 10))

        dice_txt = BIG_FONT.render(f"Dadu: {self.dice.value}", True, BLACK)
        SCREEN.blit(dice_txt, (panel_x + 60, 260))

        if self.game_over:
            win = BIG_FONT.render("MENANG!", True, GREEN)
            SCREEN.blit(win, (panel_x + 70, 320))

        pygame.display.update()

    def run(self):
        running = True
        while running:
            CLOCK.tick(FPS)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    self.handle_roll()

                if e.type == pygame.MOUSEBUTTONDOWN:
                    if self.roll_btn.collidepoint(e.pos):
                        self.handle_roll()

            self.update()
            self.draw()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()
