import numpy as np

from settings import ROW_COUNT, COLUMN_COUNT


class Board:
    """
    Класс, отвечающий за состояние игрового поля.
    """

    def __init__(self, rows: int = None, columns: int = None):
        # Если не переданы значения, берем их из настроек
        if rows is None:
            rows = ROW_COUNT
        if columns is None:
            columns = COLUMN_COUNT
        self.rows = rows
        self.columns = columns
        self.board = np.zeros((self.rows, self.columns))

    def is_valid_location(self, col: int) -> bool:
        """Проверяет, можно ли сделать ход в столбце col (верхняя ячейка должна быть пуста)."""
        return self.board[self.rows - 1][col] == 0

    def get_next_open_row(self, col: int) -> int:
        """Находит первую свободную строку (снизу) в столбце col."""
        for r in range(self.rows):
            if self.board[r][col] == 0:
                return r
        raise ValueError("Столбец заполнен")

    def drop_piece(self, row: int, col: int, piece: int) -> None:
        """Устанавливает фишку (обозначенную числом piece) в ячейку (row, col)."""
        self.board[row][col] = piece

    def winning_move(self, piece: int) -> bool:
        """Проверяет, собрал ли игрок с фишкой piece 4 подряд по горизонтали, вертикали или диагонали."""
        # Проверка по горизонтали
        for c in range(self.columns - 3):
            for r in range(self.rows):
                if (self.board[r][c] == piece and
                        self.board[r][c + 1] == piece and
                        self.board[r][c + 2] == piece and
                        self.board[r][c + 3] == piece):
                    return True

        # Проверка по вертикали
        for c in range(self.columns):
            for r in range(self.rows - 3):
                if (self.board[r][c] == piece and
                        self.board[r + 1][c] == piece and
                        self.board[r + 2][c] == piece and
                        self.board[r + 3][c] == piece):
                    return True

        # Проверка по диагонали (с положительным наклоном)
        for c in range(self.columns - 3):
            for r in range(self.rows - 3):
                if (self.board[r][c] == piece and
                        self.board[r + 1][c + 1] == piece and
                        self.board[r + 2][c + 2] == piece and
                        self.board[r + 3][c + 3] == piece):
                    return True

        # Проверка по диагонали (с отрицательным наклоном)
        for c in range(self.columns - 3):
            for r in range(3, self.rows):
                if (self.board[r][c] == piece and
                        self.board[r - 1][c + 1] == piece and
                        self.board[r - 2][c + 2] == piece and
                        self.board[r - 3][c + 3] == piece):
                    return True

        return False

    def reset(self) -> None:
        """Сбрасывает игровое поле в исходное состояние."""
        self.board = np.zeros((self.rows, self.columns))


class Connect4Game:
    """
    Класс, реализующий логику игры Connect 4.
    """

    def __init__(self):
        self.board = Board()
        self.game_over = False
        self.turn = 0  # 0 – игрок 1, 1 – игрок 2

    def make_move(self, col: int) -> bool:
        """
        Выполняет ход текущего игрока в столбце col.
        Если ход выполнен успешно, обновляет игровое поле и переключает игрока.
        Возвращает True, если ход был успешен, иначе False.
        """
        if not self.board.is_valid_location(col):
            return False

        row = self.board.get_next_open_row(col)
        piece = 1 if self.turn == 0 else 2
        self.board.drop_piece(row, col, piece)
        if self.board.winning_move(piece):
            self.game_over = True
        # Переключение игрока
        self.turn = (self.turn + 1) % 2
        return True

    def get_current_player(self) -> int:
        """Возвращает номер текущего игрока (1 или 2)."""
        return 1 if self.turn == 0 else 2
