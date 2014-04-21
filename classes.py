################### classes.py ###################
##                                              ##
## This file contain classes wich will be used  ##
## to create UI objects such as windows,        ##
## buttons, and game objects such as maps,      ##
## characters                                   ##
##                                              ##
## Ce fichier contient les classes utilisées    ##
## pour créer les objets d'interface comme les  ##
## fenêtres, les buttons, et les objets du jeu  ##
## comme les maps, les personnages              ##
##                                              ##
##################################################

import pygame
from pygame.locals import *

class Window(window, rect)

class Button:

    def __init__(self,window,text,rect):
        self.rect = rect

    def hoover():

    def clicked():

class Niveau:

    def __init__(self, fenetre, numNiveau):
        self.mur = pygame.image.load("Sprites/mur" + str(numNiveau) + ".png").convert()
        self. sol = pygame.image.load("Sprites/sol" + str(numNiveau) + ".png").convert()
        with open("Levels/" + str(numNiveau) + ".txt", "r") as niveau:
            self.largeur = int(niveau.readline().replace("\n", "").replace("\r", ""))
            self.hauteur = int(niveau.readline().replace("\n", "").replace("\r", ""))
            self.structure = []
            for i in range(self.hauteur):
                self.structure.append(niveau.readline().replace("\n", "").replace("\r", ""))
            self.nbMax = int(niveau.readline().replace("\n", "").replace("\r", ""))
            self.respawn = []
            for i in range(self.nbMax):
                coord = niveau.readline().replace("\n", "").replace("\r", "").split(" ")
                self.respawn.append((int(coord[0]), int(coord[1])))
        for y in range(self.hauteur):
            for x in range(self.largeur):
                if self.structure[y][x] == "M":
                    fenetre.blit(self.mur, (30*x, 30*y))
                if self.structure[y][x] == " ":
                    fenetre.blit(self.sol, (30*x, 30*y))
        pygame.image.save(fenetre, "niveau" + str(numNiveau) + ".png")
        self.image = pygame.image.load("niveau" + str(numNiveau) + ".png").convert()

    def afficher(self, fenetre):
        fenetre.blit(self.image, (0,0))

class Personnage:

    def __init__(self, num, nom, niveau):
        self.num = num                  #Numéro du personnage créé
        self.nom = nom                  #Son nom
        self.bombes = [10]              #Les bombes qu'il possède [normal]
        self.bonus = [0, 0, 1, 1]       #Les bonus qu'il possède [vie supplémentaire, vitesse supplémentaire, nombre de bombes à poser, puissance des bombes]
        self.sprites = []
        for i in range(4):
            sprites = []
            for j in range(3):
                sprites.append(pygame.image.load("Sprites/" + str(i) + str(j) + ".png").convert_alpha())
            self.sprites.append(sprites)
        self.direction = 0
        self.position = niveau.respawn[num - 1]
        self.image = self.sprites[self.direction][0]
        
    def afficher(self, fenetre):
        self.image = self.sprites[self.direction][0]
        fenetre.blit(self.image, (30*self.position[0]+7, 30*self.position[1]+2))

    def deplacer(key1, key2):
        pass        
            
