#################### config.py ###################
##                                              ##
## This file set differents constants           ##
##                                              ##
## Ce fichier initialise différentes constantes ##
##                                              ##
##################################################

import os
from pygame.locals import *

WINDOW_ICON_PATH = os.path.join("Pictures", "Icon.png")
WINDOW_CAPTION = "Bros. Bomb Squad"
WINDOW_FLAGS = HWSURFACE|DOUBLEBUF
WINDOW_X_RES = 272
WINDOW_Y_RES = 240
WINDOW_RES = (WINDOW_X_RES, WINDOW_Y_RES)
SPRITE_SIZE = 16
BOMB_TIMEOUT = 2.
EXPLOSION_TIMEOUT = 1.5

# Item types
NOTHING =0
EXPLOSION = 1
BONUS = 2
BOMB = 3
BREAKABLE = 4
WALL = 5

# Directions
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)
DIRECTIONS = [LEFT, RIGHT, UP, DOWN]

# Bonus types
BOMB_BONUS = 0
POWER_BONUS = 1
SPEED_BONUS = 2

# Explosion types
CENTER = 0
TUBEVERT = 1
TUBEHOR = 2
ENDUP = 3
ENDLEFT = 4
ENDDOWN = 5
ENDRIGHT = 6

# Player keys
SPEED_INIT = 1.
BOMBSMAX_INIT = 1
POWER_INIT = 2
KEYS_1 = [K_UP, K_DOWN, K_LEFT, K_RIGHT, K_KP_ENTER]
KEYS_2 = [K_w, K_s, K_a, K_d, K_SPACE]
KEYS = [KEYS_1, KEYS_2]

