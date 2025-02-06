import unittest
import numpy as np

from src.board import Board, Connect4Game


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_initial_board_empty(self):
        """После инициализации все ячейки должны быть нулями."""
        self.assertTrue(np.all(self.board.board == 0), "Начальное поле должно быть пустым (нулевое)")

    def test_drop_piece(self):
        """Проверяем, что метод drop_piece корректно устанавливает фишку."""
        self.board.drop_piece(0, 0, 1)
        self.assertEqual(self.board.board[0][0], 1, "После установки фишки значение должно измениться")

    def test_is_valid_location(self):
        """Проверяем, что is_valid_location возвращает False для заполненного столбца."""
        # Изначально столбец 0 должен быть доступен
        self.assertTrue(self.board.is_valid_location(0))
        # Заполняем столбец 0
        for r in range(self.board.rows):
            self.board.drop_piece(r, 0, 1)
        self.assertFalse(self.board.is_valid_location(0), "Заполненный столбец должен быть недоступен для хода")

    def test_get_next_open_row(self):
        """Проверяем корректное получение следующей свободной строки."""
        # В пустом столбце следующий открытый ряд – 0
        self.assertEqual(self.board.get_next_open_row(0), 0)
        self.board.drop_piece(0, 0, 1)
        self.assertEqual(self.board.get_next_open_row(0), 1)

    def test_winning_move_horizontal(self):
        """Проверяем горизонтальное выигрышное условие."""
        # Устанавливаем 4 фишки по горизонтали в нижней строке (row 0)
        for col in range(4):
            self.board.drop_piece(0, col, 1)
        self.assertTrue(self.board.winning_move(1), "Горизонтальная комбинация должна считаться выигрышной")
        self.assertFalse(self.board.winning_move(2), "Неверная комбинация не должна давать выигрыш")

    def test_winning_move_vertical(self):
        """Проверяем вертикальное выигрышное условие."""
        # Устанавливаем 4 фишки по вертикали в столбце 0
        for row in range(4):
            self.board.drop_piece(row, 0, 1)
        self.assertTrue(self.board.winning_move(1), "Вертикальная комбинация должна считаться выигрышной")

    def test_winning_move_diagonal_positive(self):
        """Проверяем диагональное выигрышное условие с положительным наклоном (слева снизу направо вверх)."""
        # Прямое создание диагонали (без имитации «гравитации»)
        self.board.drop_piece(0, 0, 1)
        self.board.drop_piece(1, 1, 1)
        self.board.drop_piece(2, 2, 1)
        self.board.drop_piece(3, 3, 1)
        self.assertTrue(self.board.winning_move(1), "Диагональ с положительным наклоном должна считаться выигрышной")

    def test_winning_move_diagonal_negative(self):
        """Проверяем диагональное выигрышное условие с отрицательным наклоном (слева сверху направо вниз)."""
        # Прямое создание диагонали (без имитации гравитации)
        self.board.drop_piece(3, 0, 1)
        self.board.drop_piece(2, 1, 1)
        self.board.drop_piece(1, 2, 1)
        self.board.drop_piece(0, 3, 1)
        self.assertTrue(self.board.winning_move(1), "Диагональ с отрицательным наклоном должна считаться выигрышной")

class TestConnect4Game(unittest.TestCase):
    def setUp(self):
        self.game = Connect4Game()

    def test_make_move_valid(self):
        """Проверяем, что корректный ход выполняется и переключается игрок."""
        # Изначально текущий игрок – 1
        self.assertEqual(self.game.get_current_player(), 1)
        # Выполняем ход в столбце 0
        move_result = self.game.make_move(0)
        self.assertTrue(move_result, "Ход в свободный столбец должен выполняться успешно")
        # Проверяем, что фишка установилась
        self.assertEqual(self.game.board.board[0][0], 1)
        # После хода текущий игрок должен измениться
        self.assertEqual(self.game.get_current_player(), 2)

    def test_make_move_invalid(self):
        """Проверяем, что попытка хода в заполненный столбец не выполняется."""
        # Заполняем столбец 0
        for r in range(self.game.board.rows):
            self.game.board.drop_piece(r, 0, 1)
        move_result = self.game.make_move(0)
        self.assertFalse(move_result, "Ход в заполненный столбец должен быть невозможен")

    def test_game_over_after_win(self):
        """Проверяем, что игра завершается после победной комбинации.
        Для этого имитируем серию ходов, приводящую к горизонтальному выигрышу для игрока 1.
        При этом ходы игрока 2 выбираются так, чтобы не помешать победе.
        """
        # Схема ходов: игрок1: 0, игрок2: 6, игрок1: 1, игрок2: 6, игрок1: 2, игрок2: 6, игрок1: 3.
        moves = [0, 6, 1, 6, 2, 6, 3]
        for move in moves:
            self.game.make_move(move)
        self.assertTrue(self.game.game_over, "Игра должна завершиться после победной комбинации")
        # После победы ход переключается, поэтому текущий игрок становится 2
        self.assertEqual(self.game.get_current_player(), 2)

if __name__ == '__main__':
    unittest.main()
