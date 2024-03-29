from pathlib import Path
import os

SCREEN_WIDTH = 560 + 300
SCREEN_HEIGHT = 480
FPS = 60

UDP_PORT = 5000
TCP_PORT = 5000

root_path = Path(os.path.dirname(__file__)).parent

PLAYER1 = 1
PLAYER2 = 2
class Color:
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    DARK_GRAY = (50, 50, 50)
    INDIAN_RED = (205, 92, 92)
    PALE_GREEN = (152, 251, 152)
    LIGHT_BLUE = (106, 159, 181)
    DARK_GREEN = (0, 100, 0, 255)
    DARK_RED = (139, 0, 0, 255)
    LIGHT_SLATE_GRAY = (119, 136, 153, 255)
    DARK_GRAY_2 =  (169, 169, 169, 255)
    
