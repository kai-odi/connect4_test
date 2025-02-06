import math
import sys

import pygame

from board import Connect4Game
from constants import BLUE, BLACK, YELLOW, RED, WHITE, BUTTON_WIDTH, BUTTON_HEIGHT
from settings import SQUARESIZE, SCREEN_TITLE, WIN_WAIT_TIME, FPS, FONT_SIZE


class Connect4GUI:
    """
    Класс, отвечающий за графический интерфейс игры с использованием pygame.
    """

    def __init__(self, game: Connect4Game):
        self.game = game
        pygame.init()
        self.width = self.game.board.columns * SQUARESIZE
        self.height = (self.game.board.rows + 1) * SQUARESIZE  # Дополнительная область для отображения хода
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(SCREEN_TITLE)
        self.myfont = pygame.font.SysFont("monospace", FONT_SIZE)
        self.clock = pygame.time.Clock()

    def draw_board(self) -> None:
        """Отрисовывает текущее состояние игрового поля."""
        board_array = self.game.board.board
        # Рисуем поле: синие прямоугольники и черные кружки для пустых ячеек
        for c in range(self.game.board.columns):
            for r in range(self.game.board.rows):
                pygame.draw.rect(
                    self.screen,
                    BLUE,
                    (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE)
                )
                pygame.draw.circle(
                    self.screen,
                    BLACK,
                    (int(c * SQUARESIZE + SQUARESIZE / 2),
                     int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                    int(SQUARESIZE / 2 - 5)
                )

        # Отрисовка фишек игроков
        for c in range(self.game.board.columns):
            for r in range(self.game.board.rows):
                if board_array[r][c] == 1:
                    pygame.draw.circle(
                        self.screen,
                        RED,
                        (int(c * SQUARESIZE + SQUARESIZE / 2),
                         self.height - int(r * SQUARESIZE + SQUARESIZE / 2)),
                        int(SQUARESIZE / 2 - 5)
                    )
                elif board_array[r][c] == 2:
                    pygame.draw.circle(
                        self.screen,
                        YELLOW,
                        (int(c * SQUARESIZE + SQUARESIZE / 2),
                         self.height - int(r * SQUARESIZE + SQUARESIZE / 2)),
                        int(SQUARESIZE / 2 - 5)
                    )
        pygame.display.update()

    def display_winner(self, winner: int) -> None:
        """Отображает сообщение о победе."""
        label = self.myfont.render(
            f"Player {winner} win!",
            True,
            RED if winner == 1 else YELLOW
        )
        self.screen.blit(label, (40, 10))
        pygame.display.update()
        pygame.time.wait(WIN_WAIT_TIME)

    def ask_restart(self) -> bool:
        """
        После завершения игры выводит сообщение "Start a new game?" и рисует две кнопки – "Yes" и "No".
        Ожидает клика мышью: если нажата кнопка "Yes", возвращает True, если "No" – False.
        """
        # Очищаем экран
        self.screen.fill(BLACK)

        # Используем шрифт меньшего размера для запроса и кнопок
        prompt_font = pygame.font.SysFont("monospace", 50)
        prompt_text = "Start a new game?"
        prompt_surface = prompt_font.render(prompt_text, True, WHITE)
        prompt_rect = prompt_surface.get_rect(center=(self.width / 2, self.height / 2 - 100))
        self.screen.blit(prompt_surface, prompt_rect)

        # Задаём размеры кнопок


        # Кнопка "Yes"
        yes_button_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
        yes_button_rect.center = (self.width / 2 - BUTTON_WIDTH, self.height / 2 + 50)
        pygame.draw.rect(self.screen, BLUE, yes_button_rect)
        yes_text_surface = prompt_font.render("Yes", True, WHITE)
        yes_text_rect = yes_text_surface.get_rect(center=yes_button_rect.center)
        self.screen.blit(yes_text_surface, yes_text_rect)

        # Кнопка "No"
        no_button_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
        no_button_rect.center = (self.width / 2 + BUTTON_WIDTH, self.height / 2 + 50)
        pygame.draw.rect(self.screen, BLUE, no_button_rect)
        no_text_surface = prompt_font.render("No", True, WHITE)
        no_text_rect = no_text_surface.get_rect(center=no_button_rect.center)
        self.screen.blit(no_text_surface, no_text_rect)

        pygame.display.flip()  # Обновляем экран

        # Ожидание клика мышью по одной из кнопок, с регулярной задержкой
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if yes_button_rect.collidepoint(pos):
                        return True
                    elif no_button_rect.collidepoint(pos):
                        return False
            self.clock.tick(FPS)  # Обеспечиваем плавную работу цикла

    def run(self) -> None:
        """Основной цикл игры: обработка событий, отрисовка и логика игры."""
        self.draw_board()
        while not self.game.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    # Отрисовка движущейся фишки в верхней области (подсказка для игрока)
                    pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, SQUARESIZE))
                    posx = event.pos[0]
                    if self.game.turn == 0:
                        pygame.draw.circle(
                            self.screen,
                            RED,
                            (posx, int(SQUARESIZE / 2)),
                            int(SQUARESIZE / 2 - 5)
                        )
                    else:
                        pygame.draw.circle(
                            self.screen,
                            YELLOW,
                            (posx, int(SQUARESIZE / 2)),
                            int(SQUARESIZE / 2 - 5)
                        )
                    pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Очищаем верхнюю область экрана
                    pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, SQUARESIZE))
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if self.game.board.is_valid_location(col):
                        row = self.game.board.get_next_open_row(col)
                        piece = 1 if self.game.turn == 0 else 2
                        self.game.board.drop_piece(row, col, piece)

                        if self.game.board.winning_move(piece):
                            self.draw_board()
                            self.display_winner(1 if piece == 1 else 2)
                            self.game.game_over = True

                        # Переключение игрока
                        self.game.turn = (self.game.turn + 1) % 2
                        self.draw_board()

            self.clock.tick(FPS)  # Ограничение FPS
