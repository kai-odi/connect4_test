import numpy as np
import pygame
import sys

from board import Connect4Game
from gui_connector import Connect4GUI


def main() -> None:
    # Главный цикл приложения: после завершения игры спрашиваем,
    # хочет ли пользователь начать новую игру.
    while True:
        game = Connect4Game()
        gui = Connect4GUI(game)
        gui.run()
        if not gui.ask_restart():
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    main()
