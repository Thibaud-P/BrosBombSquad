################### classes.py ###################
##                                              ##
## This file contain classes wich will be used  ##
## to create UI objects such as windows,        ##
## buttons, and game objects such as maps or    ##
## characters                                   ##
##                                              ##
## Ce fichier contient les classes utilisées    ##
## pour créer les objets d'interface comme les  ##
## fenêtres, les buttons, et les objets du jeu  ##
## comme les maps ou les personnages            ##
##                                              ##
##################################################

import pygame, sys, os, time
from pygame.locals import *
from config import *
from random import randrange

class Globals():

    def __init__(self):
        
        self.window = pygame.display.set_mode((WINDOW_X_RES, WINDOW_Y_RES), WINDOW_FLAGS)
        self.clock = pygame.time.Clock()

class Bonus(pygame.sprite.DirtySprite):

    bonusSprites = [[None for i in range(2)] for i in range(3)]
    bonusTypes = ["BombBonus", "PowerBonus", "SpeedBonus"]

    def __init__(self, posX, posY, bonusType):

        if Bonus.bonusSprites[0][0] == None:

            for i, j in enumerate(Bonus.bonusTypes):

                for k in range(2):

                    Bonus.bonusSprites[i][k] = pygame.image.load(os.path.join("Images", "Bonus", j + str(k) + ".png")).convert()

        pygame.sprite.DirtySprite.__init__(self)

        self.rect = Bonus.bonusSprites[0][0].get_rect()
        self.rect.topleft =(SPRITE_SIZE*posX, SPRITE_SIZE*posY)
        self.bonusType = bonusType
        self.animPos = 0
        self.image = self.bonusSprites[self.bonusType][self.animPos]

    def take(self):
        pass

        
        

class Bomb(pygame.sprite.DirtySprite):

    bombSprites = [None for i in range(3)]

    explosionSprites = [[None for i in range(5)]for i in range(3)]

    explosionType = ["Center", "Tube", "End"]
    
    def __init__(self, posX, posY, power):

        if Bomb.bombSprites[0] == None:

            for i in range(3):

                Bomb.bombSprites[i] = pygame.image.load(os.path.join("Images", "Bombs", "Bomb" + str(i) + ".png")).convert()

        if Bomb.explosionSprites[0] == None:

            for i in range(7):

                Bomb.explosionSprites[i] = pygame.image.load(os.path.join("Images", "Explosions", Bomb.explosionType[i] + str(i) + ".png")).convert()

        pygame.sprite.DirtySprite.__init__(self)

        self.rect = Bomb.bombSprites[0].get_rect()
        self.rect.topleft =(SPRITE_SIZE*posX, SPRITE_SIZE*posY)
        self.image = self.bombSprites[0]
        self.timeOut = time.time() + BOMB_TIMEOUT
        self.posX = posX
        self.posY = posY
        self.power = power
        self.explode = 0

    def update(self):

        if time.time() > self.timeOut:

            self.explode = 1

        elif time.time() + 0.5 > self.timeOut:

            self.image = self.bombSprites[2]

        elif time.time() + 1. > self.timeOut:

            self.image = self.bombSprites[1]

        elif time.time() + 1.5 > self.timeOut:

            self.image = self.bombSprites[0]

        elif time.time() + 2. > self.timeOut:

            self.image = self.bombSprites[1]

    def getAttr(self):

        return(self.posX, self.posY, self.power, self.explode)

class Breakable(pygame.sprite.DirtySprite):

    animations = [None for i in range(7)]

    def __init__(self, posX, posY, spriteSetPath):

        pygame.sprite.DirtySprite.__init__(self)

        if Breakable.animations[0] == None:

            for i in range(7):

                Breakable.animations[i] = pygame.image.load(os.path.join(spriteSetPath, "Breakable" + str(i) + ".png")).convert()

        self.rect = Breakable.animations[0].get_rect()
        self.rect.topleft =(SPRITE_SIZE*posX, SPRITE_SIZE*posY)
        self.animPos = 0
        self.image = self.animations[self.animPos]
        self.explode = 0

    def update(self):

        if self.explode:

            self.animPos -= 1
            self.image = self.animations[self.animPos]

            if self.animPos > 7:

                self.visible = 0
                self.explode = 0
                self.dirty = 1


    def explode(self):

        self.explode = 1
        self.dirty = 2
        
        
class Level(pygame.sprite.LayeredDirty):

    def __init__(self, window, numLevel):
        
        pygame.sprite.LayeredDirty.__init__(self)

        with open(os.path.join("Levels", "Level " + str(numLevel) + ".txt"), "r") as file:

            # We pick up each real information in the text file, and we convert it correctly
            # On prend chaque vraie information dans le fichier texte, et on la convertit correctement
            
            self.name = file.readline().replace("Level name: ", "").replace("\n", "")
            self.spriteSet = file.readline().replace("Sprite Set: ", "").replace("\n", "")
            self.spriteSetPath = os.path.join("Images", "Levels", self.spriteSet)
            self.playerMax = int(file.readline().replace("Player Maximum: ", "").replace("\n", ""))
            
            self.spawns = []
            for i in range(self.playerMax):
                spawn = file.readline().replace("Spawn " + str(i+1) + ": ", "").replace("\n", "").split(", ")
                self.spawns.append((int(spawn[0]), int(spawn[1])))
                
            self.width = int(file.readline().replace("Widht: ", "").replace("\n", ""))
            self.height = int(file.readline().replace("Heigth: ", "").replace("\n", ""))
            
            file.readline()
            self.structure = []
            for i in range(self.height):
                structureLine = []
                charLine = file.readline().replace("\n", "")
                for j in range(self.width):
                    structureLine.append(int(charLine[j]))
                self.structure.append(structureLine)
                
        self.wallSprite = pygame.image.load(os.path.join(self.spriteSetPath, "Wall.png")).convert()
        self.groundSprite = pygame.image.load(os.path.join(self.spriteSetPath, "Ground.png")).convert()

        for y in range(self.height):
            for x in range(self.width):
                if self.structure[y][x] == 5:
                    self.structure[y][x] == WALL
                    window.blit(self.wallSprite, (SPRITE_SIZE*x, SPRITE_SIZE*y))
                else:
                    self.structure[y][x] == NOTHING
                    window.blit(self.groundSprite, (SPRITE_SIZE*x, SPRITE_SIZE*y))
            
        pygame.image.save(window, os.path.join("Levels", "Level " + str(numLevel) + ".png"))
        self.background = pygame.image.load(os.path.join("Levels", "Level " + str(numLevel) + ".png")).convert()
        self.clear(window, self.background)

        self.itemTable = [[None for i in range(self.height)] for i in range(self.width)]
        
        for x in range(self.width):
            for y in range(self.height):
                if self.structure[y][x] == 4:
                    self.itemTable[x][y] = Breakable(x, y, self.spriteSetPath)
                    self.add(self.itemTable[x][y])

        self.bombs = []
                    
    def wallExplosion(x, y):

        self.itemTable[x][y].explode()
        bonusRandom = randrange(15)
        if bonusRandom == 0:
            self.item[x][y] = Bonus(x, y, bonusRandom)
            self.add(self.item[x][y])
            self.structure[y][x] = BONUS
        else:
            self.item[x][y] = None
            self.structure[y][x] = NOTHING

    def bombExplosion(x, y, power):
        pass
    
            
class Bombers(pygame.sprite.LayeredDirty):

    def __init__(self, window, level, numPlayer):

        pygame.sprite.LayeredDirty.__init__(self)

        self.numPlayer = numPlayer
        self.players = []
        for i in range(4):
            self.players.append(Bomber(i, level.spawns[numPlayer - 1], numPlayer%1))
            self.add(self.players[i])
            numPlayer -= 1

        level.add(self, layer = 1)

    def action(self, window):

        for sprite in self:
            sprite.action(window)
        
class Bomber(pygame.sprite.DirtySprite):

    def __init__(self, num, spawn, ia):

        pygame.sprite.DirtySprite.__init__(self)
        
        self.num = num
        self.ia = ia
        self.speed = 1
        self.bombsMax = 1
        self.power = 1
        self.sprites = []
        for i in range(4):
            sprites = []
            for j in range(3):
                sprites.append(pygame.image.load("Sprites/" + str(i) + str(j) + ".png").convert_alpha())
            self.sprites.append(sprites)
        self.direction = DOWN
        self.animPos = 0
        self.moving = False
        self.position = spawn
        self.image = self.sprites[self.direction][0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (SPRITE_SIZE*self.position[0] - 1, SPRITE_SIZE*self.position[1] - 11)
        
    def action(self, level):
        if self.ia:
            
            pass

        else:

            
                
    def update(self):

        if self.moving:

            position = self.rect.topleft

            if self.direction == DOWN:

                if position[1]%16 < 4:

                    self.animPos = 2

                elif position[1]%8 < 4:

                    self.animPos = 1
                    
                else:
                    
                    self.animPos = 0
                    
            elif self.direction == UP:

                if position[1]%16 > 12:

                    self.animPos = 2

                elif position[1]%8 > 4:

                    self.animPos = 1
                    
                else:
                    
                    self.animPos = 0
                    
            elif self.direction == LEFT:

                if position[0]%16 < 4:

                    self.animPos = 2

                elif position[0]%8 < 4:

                    self.animPos = 1
                    
                else:
                    
                    self.animPos = 0
                    
            elif self.direction == RIGHT:

                if position[0]%16 > 12:

                    self.animPos = 2

                elif position[0]%8 > 4:

                    self.animPos = 1
                    
                else:
                    
                    self.animPos = 0

        else:

            self.animPos = 0

        self.image = self.sprites[self.direction][self.animPos]


##    def get_offset:
##
##        if self.direction == DOWN:
##
##            return(0, 4)
##
##        elif self.direction == UP:
##
##            return(0, -4)
##
##        elif self.direction == LEFT:
##
##            return(-4, 0)
##
##        elif self.direction == RIGHT:
##
##            return(4, 0)
