################### events.py ####################
##                                              ##
## This file contain functions which will be    ##
## used to detect all the differents events     ##
## that the program will have to handle         ##
##                                              ##
## Ce fichier contient des fonctions utilisées  ##
## pour détecter tous les différents évènements ##
## que le programme aura à traiter              ##
##                                              ##
##################################################

import pygame, sys, os
from pygame.locals import *
from constants import *

def checkEvents(inGame):

    """
    Handle keyboard events in order to quit the program and toggle fullscreen
    Prend en charge les évènement clavier afin de quitter le programme et activer ou désactiver le plein écran
    """

    for event in pygame.event.get():

        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):

            if inGame:

                pass

                ## TODO: Pause and fade the game, draw box with options, resume and main menu  

            else:

                pygame.quit()
                sys.exit()

        elif event.type == KEYDOWN and event.key == KMOD_LALT|K_F4:

            pygame.quit()
            sys.exit()

        elif event.type == KEYDOWN and event.key == K_F11:

            pygame.display.set_mode(WINDOW_RES, window.get_flags()^FULLSCREEN)
