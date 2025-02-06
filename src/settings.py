import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Константы, считываемые из .env (с дефолтными значениями)
ROW_COUNT = int(os.environ.get("ROW_COUNT", 6))
COLUMN_COUNT = int(os.environ.get("COLUMN_COUNT", 7))
SQUARESIZE = int(os.environ.get("SQUARESIZE", 100))
WIN_WAIT_TIME = int(os.environ.get("WIN_WAIT_TIME", 3000))
FPS = int(os.environ.get("FPS", 60))
SCREEN_TITLE = os.environ.get("SCREEN_TITLE", "Connect 4")
FONT_SIZE = int(os.environ.get("FONT_SIZE", 75))
