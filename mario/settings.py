# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
MID_X = WIDTH / 2
MID_Y = HEIGHT / 2
# 256 wide by 240 high

# 16 pixel blocks
# WIDTH = 256 # 16 blocks
# HEIGHT = 240 # 15 blocks


FPS = 60
TITLE = ""

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# starting platforms
PLATFORM_LIST = [(0, HEIGHT - 200, WIDTH * 1/3, 30),
                 (WIDTH * 1/3, HEIGHT - 300, WIDTH * 1/3, 30),
                 (WIDTH * 2/3, HEIGHT - 200, WIDTH * 1/3, 30),
                 (WIDTH * 1/3, HEIGHT - 400, WIDTH * 1/20, 30),
                 (WIDTH * 1/3 + 100, HEIGHT - 400, WIDTH * 1/20, 30),
                 (WIDTH * 1/3 + 200, HEIGHT - 400, WIDTH * 1/20, 30)]

# mario properties
SIZE_MULTIPLIER = 2.5
MARIO_ACC = 0.5
MARIO_FRICTION = -0.12
GRAVITY = 0.5
