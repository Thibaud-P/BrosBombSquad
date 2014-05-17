#################### main.py #####################
##                                              ##
## In this file there are the differents steps  ##
##  of the game. It's the file you will have to ##
##  launch in order to launch the game          ##
##                                              ##
## Il y a dans ce fichier les différentes       ##
##  étapes du jeu. C'est le fichier que vous    ##
##  devez exécuter pour lancer le jeu           ##
##                                              ##
##################################################

import pygame, sys, os, time
from pygame.locals import *
from classes import *
from config import *

def init():
    """
    Initialize pygame, the program's window and the clock to limit fps
    Initialise pygame, la fenêtre de programme et l'horloge pour limiter les fps
    """
    
    pygame.init()

    pygame.display.set_icon(pygame.image.load(WINDOW_ICON_PATH))
    pygame.display.set_caption(WINDOW_CAPTION)
    window = pygame.display.set_mode(WINDOW_RES, WINDOW_FLAGS)
    
    clock = pygame.time.Clock()

    return(window, clock)


def checkEvents(window, level, inGame):
    """
    Handle keyboard events in order to quit the program and toggle fullscreen
    Prend en charge les évènement clavier afin de quitter le programme et activer ou désactiver le plein écran
    """

    test = 0

    # We take the events in the queue one by one
    # On prend les évènements dans la queue un par un
    for event in pygame.event.get():

        if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == KMOD_LALT|K_F4)):

            pygame.quit()
            sys.exit()
            
        elif event.type == KEYDOWN and event.key == K_F11:

            # We get the windows currents flags, and with ^, which stands for xor, we enable fullscreen if it is off and vice versa
            # On reprends les options de la fenêtre, et avec ^ qui signifie xor, on active le plein écran s'il est éteint et inversement
            pygame.display.set_mode(WINDOW_RES, window.get_flags()^FULLSCREEN)

            # As the window changed, we repaint the level on all the window's surface
            # Comme la fenêtre a changée, on réaffiche le niveau sur la surface de la fenêtre
            level.repaint_rect(window.get_rect())

        elif event.type == KEYDOWN and event.key == K_F1:

            test = 1

    return(test)

    
def main():
    """
    Launch the game
    Démarre le jeu
    """

    window, clock = init()

    # We load and launch the music, and make it loop forever with loops = -1
    # On charge et lance la musique, et on la fait se répéter indéfiniment avec loops = -1
    pygame.mixer.music.load(os.path.join("Sounds", "GameMusic.mp3"))
    pygame.mixer.music.play(loops = -1)

    ## TODO: MENU
    
    numLevel = 1
    numPlayers = 1
    inGame = True
    test = True
    
    # Creation of the level and the players
    # Création du niveau et des joueurs
    level = Level(window, numLevel, numPlayers)
    
    # Game's loop
    # Boucle de jeu
    while inGame:

        test = checkEvents(window, level, inGame)

        # We update game's elements (bombers sprite group is included in level sprite group)
        #   So level.update(level) call each sprite's update method with level as argument
        # On met à jour les éléments du jeu (le groupe de sprite bombers est inclut dans le groupe de sprite level)
        #   Donc level.update(level) appelle la méthode update de chaque objet avec level comme argument
        level.update(level, time.time())

        # level sprite group is LayeredDirty, that's mean that a sprite must have is attribute dirty set to 1 or 2 to be updated on screen
        #   Same thing here, we call each sprite's draw method to update the VRAM, and we take back the list of rects to be flipped on screen
        # Le groupe de sprite level est LayeredeDirty, ce qui signifie que seuls les sprites ayant l'attribut dirty à 1 ou 2 seront mis à jour à l'écran
        #   Même chose ici, on appele la méhode draw de chaque sprite pour mettre à jour la VRAM, et on récupère la liste des rects à réafficher
        rectlist = level.draw(window)
        pygame.display.update(rectlist)

        # We limit the exécution of this loop at 60Hz to fit with the screen refresh rate.
        #   Clock.tick_busy_loop() provide a very stable rate, but use more CPU time than Clock.tick()
        # On limite l'exécution de cette boucle à 60Hz pour coller avec la fréquence de rafraîchissement de l'écran
        #   Clock.tick_busy_loop() donne une fréquence très stable mais utilise plus de temps CPU que Clock.tick()
        clock.tick_busy_loop(60)

        if test:

            for i in range(level.width):

                print(i, level.itemTable[i][1])

        
if __name__ == "__main__":

    main()
