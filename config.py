#################### config.py ###################
##                                              ##
## This file set differents constants           ##
##                                              ##
## Ce fichier initialise différentes constantes ##
##                                              ##
##################################################

import os
from pygame.locals import *

WINDOW_ICON_PATH = os.path.join("Images", "Icon.png")
WINDOW_CAPTION = "Bros. Bomb Squad"
WINDOW_FLAGS = HWSURFACE|DOUBLEBUF
WINDOW_X_RES = 320
WINDOW_Y_RES = 240
WINDOW_RES = (WINDOW_X_RES, WINDOW_Y_RES)
SPRITE_SIZE = 16
BOMB_TIMEOUT = 3.

NOTHING =0
EXPLOSION = 1
BONUS = 2
BOMB = 3
BREAKABLE = 4
WALL = 5

UP = 2
DOWN = 0
LEFT = 3
RIGHT = 1
