import sys
import pygame
from pygame.locals import *
from classes import *

pygame.init()
img = pygame.image.load("Sprites/BBS.png")
pygame.display.set_icon(img)
fenetre = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Bros Bomb Squad", "BBS")

niveau = Niveau(fenetre, 1)
niveau.afficher(fenetre)
bomberman = Personnage(1, "Bomberman", niveau)
bomberman.afficher(fenetre)
pygame.display.flip()
pygame.event.set_grab(False)
key1 = key2 = 0
pygame.display.flip()
fullscreen = 0


# Boucle de traitement des évènements

while 1:
    
    for event in pygame.event.get():    # On vérifie chacun des nouveaux évènements (cette fonction purge la liste d'évènement à chaque appel)

        # On quitte le jeu si l'utilisateur ferme la fenêtre, ou s'il appuie sur ECHAP ou ALT+F4
        if (event.type == QUIT) or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == KMOD_LALT|K_F4)):
            pygame.draw.rect(fenetre, (0,0,255), (100, 100, 600, 400))
            while 1:
                pygame.display.flip()
                for event in pygame.event.get():    # On vérifie chacun des nouveaux évènements (cette fonction purge la liste d'évènement à chaque appel)

                        # On quitte le jeu si l'utilisateur ferme la fenêtre, ou s'il appuie sur ECHAP ou ALT+F4
                        if (event.type == KEYDOWN and event.key == KMOD_LALT|K_F4):

                            pygame.quit()
                            sys.exit()
        elif event.type == KEYDOWN and event.key == K_F11:
            pygame.display.toggle_fullscreen()
            print("togle!!!")
            
            if fullscreen == 0:
                fenetre = pygame.display.set_mode((800, 600), FULLSCREEN|HWSURFACE|DOUBLEBUF)
            else:
                fenetre = pygame.display.set_mode((800, 600))
            fullscreen = 1 - fullscreen
        # TODO: Fenêtre pop-up de confirmation

    keys_pressed = pygame.key.get_pressed()  # On récupère une liste de toutes les touches pressées
    directional_keys = [K_UP, K_DOWN, K_LEFT, K_RIGHT]

    # Selon les touches pressées, on actualise key1 et key2
    for key in directional_keys:
        if keys_pressed[key]:
            if key1 == 0:
                key1 = key
            elif key1 != key and key2 == 0:
                key2 = key
        else:
            if key1 == key:
                key1, key2 = key2, 0
            if key2 == key:
                key2 = 0
    
    if key2 != 0:
        pass
        #bomberman.direction = key2
        #bomberman.deplacer(key1, key2)
    elif key1 != 0:
        pass
        #bomberman.direction = key1
        #bomberman.deplacer(key1, key2)

    niveau.afficher(fenetre)
    bomberman.afficher(fenetre)
    pygame.display.flip()

