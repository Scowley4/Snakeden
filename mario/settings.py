# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
MEDGREY = (70, 70, 70)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
HEIGHT = 960  # 16 * 48 or 32 * 24 or 64 * 12
MID_X = WIDTH / 2
MID_Y = HEIGHT / 2

# In original pixels
# 256 wide by 240 high

# 16 pixel blocks
# WIDTH = 256 # 16 blocks
# HEIGHT = 240 # 15 blocks


FPS = 60
TITLE = ""



#GRIDWIDTH = WIDTH / TILESIZE
#GRIDHEIGHT = HEIGHT / TILESIZE

# Could scale up or down with this???
SIZE = 1

# Each pixel in the image turns into this many pixels in the game
PIXELSIZE = 2

# The ammount to scale each image
SCALE = int(SIZE * PIXELSIZE)

# Tiles are 16x16 pixels
TILESIZE = int(SIZE * PIXELSIZE * 16)

# Screen is 16 tiles wide
TILE_W = 16

# Screen is 15 tiles tall
TILE_H = 15

# Total width and height of the screen (in modern pixels)
WIDTH = int(TILE_W * TILESIZE)
HEIGHT = int(TILE_H * TILESIZE)


# starting platforms
# Specified by tiles
                #   x,  y,  w,  h
PLATFORM_LIST = [
                 (  0,  14, 160,  1),
                 (  5,  12,  3,  1),
                 (  7,  10,  3,  1),
                 (  9,   8,  3,  1),
                 ]
PLATFORM_TILES = [tuple(val*TILESIZE for val in plat) for plat in PLATFORM_LIST]


# mario properties
SIZE_MULTIPLIER = 2.5
MARIO_ACC = 0.5
MARIO_FRICTION = -0.12
GRAVITY = PIXELSIZE * 7/16
MAX_DOWN = 4.5 * PIXELSIZE
DOWN_RESET = 4 * PIXELSIZE
