#################### main.py #####################
##                                              ##
## This file launch the differents steps of the ##
## game. It's the file you will have to launch  ##
## in order to launch the game                  ##
##                                              ##
## Ce fichier lance les différentes étapes du   ##
## jeu. C'est le fichier que vous devez         ##
## exécuter pour lancer le jeu                  ##
##                                              ##
##################################################

import pygame, sys, os
from pygame.locals import *
from classes import *
from config import *

def init():
    """
    Initialize pygame, the program's window, the buffer and he clock to limit fps
    Initialise pygame, la fenêtre de programme, le buffer et l'horloge pour limiter les fps
    """
    
    pygame.init()

    pygame.display.set_icon(pygame.image.load(WINDOW_ICON_PATH))
    pygame.display.set_caption(WINDOW_CAPTION)
    global window
    window = pygame.display.set_mode(WINDOW_RES, WINDOW_FLAGS)
    global clock
    clock = pygame.time.Clock()


def checkEvents(inGame):
    """
    Handle keyboard events in order to quit the program and toggle fullscreen
    Prend en charge les évènement clavier afin de quitter le programme et activer ou désactiver le plein écran
    """

    for event in pygame.event.get():

        if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == KMOD_LALT|K_F4)):

            pygame.quit()
            sys.exit()
            
        elif event.type == KEYDOWN and event.key == K_F11:

            pygame.display.set_mode(WINDOW_RES, window.get_flags()^FULLSCREEN)
            level.repaint_rect(window.get_rect())

    
def main():

    init()

    ## TODO: MENU
    
    numLevel = 1
    numPlayer = 1
    inGame = True
    global level
    level = Level(window, numLevel)
    bombers = Bombers(window, level, numPlayer)

    # Boucle de traitement des évènements
    while inGame:

        checkEvents(inGame)
        bombers.action(level)
        level.update()
        rectlist = level.draw(window) + bombers.draw(window)
        pygame.display.update(rectlist)
        clock.tick_busy_loop(60)

main()
