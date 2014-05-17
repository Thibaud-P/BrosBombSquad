################### classes.py ###################
##                                              ##
## This file contain classes wich will be used  ##
##  to create game objects such as maps or      ##
##  characters                                  ##
##                                              ##
## Ce fichier contient les classes utilisées    ##
##  pour créer les objets du jeu comme les maps ##
##  ou les personnages                          ##
##                                              ##
##################################################

import pygame, sys, os, time, random
from pygame.locals import *
from config import *

# All objects classes are pygame.sprite.DirtySprite sprites, unless Bombers and Level which are pygame.sprite.LayeredDirty sprites groups
# Toutes les classes d'objets sont des sprites pygame.sprites.DirtySprite, sauf Bombers et Level qui sont des groupes de sprites pygame.sprite.LayeredDirty


# An empty object, just to know if a place is empty
# Un objet vide, just pour savoir si une case est vide
class Ground():

    item = NOTHING
        

# Same thing as Ground(), but for something indestructible
# Même chose que pour Ground(), mais pour quelque chose d'indestructible
class Wall():

    item = WALL


# A bomb with his sprites, sound, and a timeout
# Une bombe avec ses sprites, sons et un compte à rebours
class Bomb(pygame.sprite.DirtySprite):

    sprites = [None for i in range(3)]

    # The constructor of the class which allow us to create an instance of bomb 
    # Le constructeur de la classe qui permet de créer une instance de bombe
    def __init__(self, player):

        # If it's the first time we create a bomb, then load the sound and the sprites
        #   We must do that to load them once in the class and not in each instance, which save memory and time
        #   We can't load them before, like when we init Bomb.sprites[], because pygame wasn't initialized
        # Si c'est la première fois que l'on crée une bombe alors charger le son et les images
        #   On doit faire ça pour les charger une seule fois dans la classe et non pas dans chaque instance, ce qui économise de la mémoire et du temps
        #   On ne peut pas les charger avant, comme lorsqu'on initialise Bomb.sprites[], car pygame n'était pas initialisé
        if Bomb.sprites[0] == None:

            Bomb.sound = pygame.mixer.Sound(os.path.join("Sounds", "Bomb.wav"))

            for animPos in range(3):

                Bomb.sprites[animPos] = pygame.image.load(os.path.join("Pictures", "Bombs", "Bomb" + str(animPos) + ".png")).convert_alpha()

        # We call the DirtySprites constructor to get the specifics methods and attributes    
        # On appelle le constucteur des DirtySprites pour bénéficier des méthodes et des attibuts spécifiques
        pygame.sprite.DirtySprite.__init__(self)

        # This will allow us to know what kind of item it is
        # Cela va nous permettre de savoir quel type d'objet sera cet objet
        self.item = BOMB

        self.posX = player.posX
        self.posY = player.posY
        self.player = player.num
        self.power = player.power
        # The rect is the rectangle, the coordinate of the surface of the image we must draw on the screen
        #   It will be returned if the DirtySprites' draw method is called and if the sprite is dirty, i.e need to be redrawn
        # Le rect est le rectangle, les coordonnées de la surface de l'image que l'on doit afficher sur l'écran
        #   Il sera retouré par la méthode draw des DirtySprites si celle-ci est appellée et que le sprite est dirty, càd a besoin d'être réaffiché
        self.rect = self.sprites[0].get_rect()
        self.rect.bottomleft =(SPRITE_SIZE*self.posX, SPRITE_SIZE*(self.posY+1))
        # This is the image we need to draw. It will be used by the DirtySprites draw method
        # Cette image est celle que nous devons afficher. Elle sera utilisée par la méthode draw des DirtySprites
        self.image = self.sprites[0]
        # The timeout of the bomb is the moment when it have to explode, so the current time plus the general BOMB_TIMEOUT
        # Le compte à rebours est lorsque la bombe doit exploser, et il est fini après le tempsa actuel plus le BOMB_TIMEOUT general
        self.timeOut = time.time() + BOMB_TIMEOUT
        self.animPos = 0
        self.animDir = 1
        # This will be used to know when the object was last updated
        # Cela sera utiliser pour savoir quand l'objet a été dernièrement mis à jour
        self.lastTime = time.time()

    # This method update the sprite if he has to be. It is called by the Group update method
    # Cette méthode met à jour le sprite si besoin est. Elle est appelée par la méthode update du groupe
    def update(self, level, currentTime):

        # If the time is out
        # Si le compte à rebours est fini
        if currentTime > self.timeOut:

            self.destroy(level)

        # If the sprite was updated more than 0.15s before
        # Si le sprite a été mis àjour il y a plus de 0,15s
        elif currentTime - self.lastTime > 0.15:

            # If the current sprite is the third, then invert the direction of the animation
            # SI the sprite actuel est le troisième, alors inverser la direction de l'animation
            if self.animPos == 2:
                
                self.animDir = -1

            # Same thing if it is the first
            # Même chose si c'est le premier
            elif self.animPos == 0:
                
                self.animDir = 1

            # Change the sprite's number
            # Changer le numéro du sprite
            self.animPos += self.animDir
            # Update the image
            # Mettre à jour l'image
            self.image = self.sprites[self.animPos]
            # The sprite need to be redrawn
            # Le sprite doit être réaffiché
            self.dirty = 1
            # The sprite was just updated
            # Le sprite viens d'être mis à jour
            self.lastTime = currentTime

    # This method is called when the bomb explode
    # ette méthode est appelée lorsque la bombe explose
    def destroy(self, level, fromDir = None):

        self.kill()
        self.sound.play()
        level.players[self.player].bombs -= 1
        # In place of the bomb, put a CENTER explosion and add it to the group
        # A la place de la bombe, mettre une explosion de type CENTER et l'ajouter au groupe
        explosion = Explosion(self.posX, self.posY, CENTER)
        level.itemTable[self.posX][self.posY] = explosion
        level.add(explosion, layer = level.height - self.posY)
        
        for direction in DIRECTIONS:

            # If this direction is no the direction where a bomb exploded and made this bomb explode
            # Si cette direction n'est pas la direction où une bombe a explosée et nous a fait exploser
            if direction != fromDir:

                # For each distance from the bomb in the bomb explosion range
                # Pour chaque distance à la bombe dans le rayon d'explosion de la bombe
                for distance in range(1, self.power):

                    # The coordinate of the case are these, and we get the item type that's in this case
                    # Les coordonnées de la case sont celles-ci, et on prend le type d'objet que l'on a dans cette case
                    newX = self.posX + direction[0]*distance
                    newY = self.posY + direction[1]*distance
                    item = level.itemTable[newX][newY].item

                    # If there is nothing, then we will put an explosion in place, but which one?
                    # S'il n'y a rien, alors on va mettre à la place une explosion, mais lequelle?
                    
                    if item == NOTHING:

                        # We look what there is on the next case
                        # On regarde ce qu'il y a sur la case suivante                        
                        nextItem = level.itemTable[newX + direction[0]][newY + direction[1]].item

                        # If there is nothing or a bomb, we will put a tube explosion
                        # S'il n'y a rien ou une bombe, on va mettre une explosion en tube
                        if (nextItem == NOTHING or nextItem == BOMB) and distance < self.power - 1:
                            
                            if direction == UP or direction == DOWN:
                                
                                explosionType = TUBEVERT
                                
                            else:
                                
                                explosionType = TUBEHOR

                        # Else, if there is something, we will put a end of explosion
                        # Sinon s'il y a quelque chose, on va mettre une fin d'explosion
                        else:
                            
                            if direction == UP:
                                
                                explosionType = ENDUP
                                
                            elif direction == DOWN:
                                
                                explosionType = ENDDOWN
                                
                            elif direction == LEFT:
                                
                                explosionType = ENDLEFT

                            else:
                                
                                explosionType = ENDRIGHT

                        # We put the right type of explosion and continue checking in this direction
                        # On met le bon type d'explosion et on continue de vérifier dans la même direction                            
                        explosion = Explosion(newX, newY, explosionType)
                        level.itemTable[newX][newY] = explosion
                        level.add(explosion, layer = level.height - self.posY)

                    # If there is a breakable wall or a bonus, it explode. Break and try another direction
                    # Si il y a un mur cassable ou un bonus, il explose. Finir et essayer une autre direction                    
                    elif item == BREAKABLE or item == BONUS:

                        level.itemTable[newX][newY].destroy(level)
                        break

                    # If there is a bomb, it explode too, and we pass the direction where the explosion is coming from. Break and try another direction
                    # S'il y a une bombe, elle explose aussi, et on passe la direction d'où vient l'explosion. Finir et essayer une autre direction                  
                    elif item == BOMB:
                        
                        newFromDir = (-direction[0], -direction[1])
                        level.itemTable[newX][newY].destroy(level, newFromDir)
                        break

                    # Else, if it is an unbreakable wall, try another direction
                    # Sinon, si c'est un mur incassable, essayer une autre direction                    
                    else:
                        
                        break
                    
        # Erase the bomb from the group
        # Effacer la bombe du groupe
        self.kill()

# Explosion of a specific type, with an animation
# Une explosion d'un type spécifique, avec une animation
class Explosion(pygame.sprite.DirtySprite):

    sprites = [[None for i in range(5)]for j in range(7)]

    # Names of the images to load
    # Noms des images à charger
    names = ["Center", "Tube", "End"]

    
    # The constructor of the class which allow us to create an instance of explosion
    # Le constructeur de la classe qui permet de créer une instance de explosion
    def __init__(self, posX, posY, explosionType):

        # See Bomb()
        # Cf. Bomb()        
        if Explosion.sprites[0][0] == None:
           
            for animPos in range(5):

                for name in Explosion.names:

                    sprite = pygame.image.load(os.path.join("Pictures", "Explosions", name + str(animPos) + ".png")).convert_alpha()

                    if name == "Center":

                        Explosion.sprites[0][animPos] = sprite

                    elif name == "Tube":

                        Explosion.sprites[1][animPos] = sprite
                        # Rotate the sprite to get an horizontal tube
                        # Faire pivoter pour obtenir un tube horizontal
                        Explosion.sprites[2][animPos] = pygame.transform.rotate(sprite, 90)

                    elif name == "End":

                        Explosion.sprites[3][animPos] = sprite
                        # Rotate the sprite to get the others directions' ends
                        # Faire pivoter pour obtenir les fin des autre direction
                        Explosion.sprites[4][animPos] = pygame.transform.rotate(sprite, 90)
                        Explosion.sprites[5][animPos] = pygame.transform.rotate(sprite, 180)
                        Explosion.sprites[6][animPos] = pygame.transform.rotate(sprite, 270)
                        
        # See Bomb()
        # Cf. Bomb()    
        pygame.sprite.DirtySprite.__init__(self)

        self.item = EXPLOSION

        self.posX = posX
        self.posY = posY
        self.rect = self.sprites[0][0].get_rect()
        self.rect.bottomleft =(SPRITE_SIZE*self.posX, SPRITE_SIZE*(self.posY+1))
        self.type = explosionType
        self.animPos = 0
        self.animDir = 1
        self.image = self.sprites[self.type][self.animPos]
        self.lastTime = time.time()
        
    # See Bomb()
    # Cf. Bomb() 
    def update(self, level, currentTime):

        if currentTime - self.lastTime > 0.05:

            # If we already go to last sprite number (animDir == -1) and we are at the first sprite number (animPos == 0), put Ground in place and erase from group
            # Si on est déjà allé au dernier numéro de sprite (animDir == -1) et qu'on est au premier (animPos == 0), mettre un Ground à la place et effacer du groupe
            
            if self.animPos == 0 and self.animDir == -1:
                
                level.itemTable[self.posX][self.posY] = Ground()
                self.kill()
                
            else:

                # If we are at the last sprite number, change animation direction
                # Si on est au dernier numéro de sprite, changer la direction de l'animation
                if self.animPos == 4:
                    
                    self.animDir = -1
                    
                # See Bomb()
                # Cf. Bomb()
                self.animPos += self.animDir
                self.image = self.sprites[self.type][self.animPos]                
                self.lastTime = currentTime
                self.dirty = 1
                
# Breakable wall with an explosion animation
# Un mur cassable avec une animation d'explosion
class Breakable(pygame.sprite.DirtySprite):

    sprites = [None for i in range(7)]
    
    # The constructor of the class which allow us to create an instance of breakable wall
    # Le constructeur de la classe qui permet de créer une instance de mur cassable
    def __init__(self, posX, posY, spriteSetPath):
        
        # See Bomb()
        # Cf. Bomb()
        if Breakable.sprites[0] == None:

            for i in range(7):

                Breakable.sprites[i] = pygame.image.load(os.path.join(spriteSetPath, "Breakable" + str(i) + ".png")).convert_alpha()
                
        # See Bomb()
        # Cf. Bomb()
        pygame.sprite.DirtySprite.__init__(self)

        self.item = BREAKABLE

        self.posX = posX
        self.posY = posY
        self.rect = Breakable.sprites[0].get_rect()
        self.rect.bottomleft =(SPRITE_SIZE*self.posX, SPRITE_SIZE*(self.posY+1))
        self.animPos = 0
        self.image = self.sprites[self.animPos]
        self.explode = 0
        self.lastTime = time.time()
        
    # See Bomb()
    # Cf. Bomb()
    def update(self, level, currentTime):

        # If the sprite was updated more than 0.05s ago and the wall is exploding
        # Si le sprite a été mis à jour il y a plus de 0,05s and que le mur est en train d'exploser
        if currentTime - self.lastTime > 0.05 and self.explode:

            # See Bomb()
            # Cf. Bomb()
            self.animPos += 1

            #If the animation is over
            # Si l'animation est terminée
            if self.animPos > 6:
                
                self.kill()
                
            else:

                self.lastTime = currentTime
                self.image = self.sprites[self.animPos]
                
            self.dirty = 1

    # This method init the destuction of the wall and drop a bonus randomly
    # Cette méthode initialise la destruction du mur et pose un bonus aléatoirement
    def destroy(self, level):
        
        bonusRandom = random.randrange(15)
        
        if bonusRandom < 3:
            
            bonus = Bonus(self.posX, self.posY, bonusRandom)
            level.itemTable[self.posX][self.posY] = bonus
            level.add(bonus, layer = level.height - self.posY - 1)
            
        else:
            
            level.itemTable[self.posX][self.posY] = Ground()
            
        self.explode = 1
        self.dirty = 1
        
# Bonus of a specific type, with an animation
# Un bonus d'un type spécifique, avec une animation
class Bonus(pygame.sprite.DirtySprite):

    sprites = [[None for i in range(2)] for i in range(3)]

    # See Explosion()
    # Cf. Explosion()
    names = ["BombBonus", "PowerBonus", "SpeedBonus"]
    
    # The constructor of the class which allow us to create an instance of bonus
    # Le constructeur de la classe qui permet de créer une instance de bonus
    def __init__(self, posX, posY, bonusType):


        if Bonus.sprites[0][0] == None:

            for nameNum, name in enumerate(Bonus.names):

                for animPos in range(2):

                    Bonus.sprites[nameNum][animPos] = pygame.image.load(os.path.join("Pictures", "Bonus", name + str(animPos) + ".png")).convert()

            Bonus.sound = pygame.mixer.Sound(os.path.join("Sounds", "Bonus.wav"))
                    
        # See Bomb()
        # Cf. Bomb()
        pygame.sprite.DirtySprite.__init__(self)

        self.item = BONUS

        self.posX = posX
        self.posY = posY
        self.rect = Bonus.sprites[0][0].get_rect()
        self.rect.bottomleft =(SPRITE_SIZE*self.posX, SPRITE_SIZE*(self.posY+1))
        self.type = bonusType
        self.animPos = 0
        self.image = self.sprites[self.type][self.animPos]
        self.lastTime = time.time()
        
    # See Bomb()
    # Cf. Bomb()
    def update(self, level, currentTime):

        if currentTime - self.lastTime > 0.25:

            # If animPos == 1, then animPos = 1 - 1 = 0. If animPos == 0, then animPos = 1 - 0 = 1
            # Si animPos == 1, alors animPos = 1 - 1 = 0. Si animPos == 0, alors animPos = 1 - 0 = 1            
            self.animPos = 1 - self.animPos
                
            self.lastTime = currentTime
            self.image = self.sprites[self.type][self.animPos]
            self.dirty = 1

    # Put Ground() in place, erase from the group and return the bonus type
    # Met un Ground() à la place, efface du groupe et retourne le type de bonus
    def destroy(self, level):

        # TODO: Destroy animation

        level.itemTable[self.posX][self.posY] = Ground()
        self.kill()
        self.sound.play()

        return(self.type)
    
# This class is used to create players and handle their movements and action
# Cette class est utilisée pour créer des joueurs et gérer leurs mouvements et actions
class Player(pygame.sprite.DirtySprite):

    deathSound = None
    
    # The constructor of the class which allow us to create an player
    # Le constructeur de la classe qui permet de créer un joueur
    def __init__(self, num, spawn, ia):
        
        # See Bomb()
        # Cf. Bomb()
        if Player.deathSound == None:

            Player.deathSound = pygame.mixer.Sound(os.path.join("Sounds", "Death.wav"))

        # See Bomb()
        # Cf. Bomb()
        pygame.sprite.DirtySprite.__init__(self)

        # Differents caracteristics and images of the player
        # Différentes caractéristiques et images du joueur
        self.num = num
        self.ia = ia
        self.speed = SPEED_INIT
        self.bombsMax = BOMBSMAX_INIT
        self.bombs = 0
        self.power = POWER_INIT
        self.sprites = []
        
        for direction in range(4):
            
            spriteLine = []
            
            for animPos in range(3):
                
                spriteLine.append(pygame.image.load(os.path.join("Pictures", "Players", "Player " + str(self.num), str(direction) + str(animPos) + ".png")).convert_alpha())
                
            self.sprites.append(spriteLine)
                               
        self.direction = DOWN
        self.spriteDir = 0
        self.spritePos = 0
        self.moving = False
        # Pos represent the table coordinates and screenPos and lastScreenPos the screen coordinates
        # Pos représente les coordonnées du tableau et screenPos et lastScreenPos les coordonnées sur l'écran
        self.posX = spawn[0]
        self.posY = spawn[1]
        self.screenPosX = float(SPRITE_SIZE*self.posX)
        self.screenPosY = float(SPRITE_SIZE*(self.posY+1))
        self.image = self.sprites[self.spriteDir][self.spritePos]
        self.rect = self.image.get_rect()
        self.rect.bottomleft =(self.screenPosX, self.screenPosY)
        self.alive = True
        self.dirty = 2
        
    # Update the player's sprite, react to keys pressed, check death... once per frame because dirty = 2
    # Mise à jour du sprite du joueur, réaction au touches pressées, vérifier la mort... Une fois par tour de boucle dejeu car dirty = 2
    def update(self, level, time):

        # If the player is alive...
        # Si le joueur est vivant...
        if self.alive:

            self.checkBox(level)

            # If the player is human
            # Si le joueur est humain
            if not self.ia:

                # Check the key pressed and update the player's caracteristics
                # Vérifier les touches pressées et mettre à jour les caractéristiques du joueur
                keyPressed = pygame.key.get_pressed()
                self.checkBombDrop(level, keyPressed)
                self.setDirection(level, keyPressed)

                if self.moving:

                    # Update the screen position depending on the speed and the direction
                    # Mettre à jour la postion sur l'écran en fonction de la vitesse et de la direction
                    self.screenPosX += float(self.direction[0]*self.speed)
                    self.screenPosY += float(self.direction[1]*self.speed)          
                    self.rect.bottomleft = int(self.screenPosX), int(self.screenPosY)
                    # Change the layer, so the more the player is at the bottom, the more he will be on the top after the blitting
                    # Change la profondeur, pour que les joueurs les plus en bas soient les plus en avant lors de l'affichage
                    level.change_layer(self, self.rect.bottom)
                    # Update posX and posY to fit closer to the screen position
                    # Met à jour posX et posY pour correspondre au plus près à la position sur l'écran
                    self.posX = int(self.screenPosX / SPRITE_SIZE + 0.5)
                    self.posY = int(self.screenPosY / SPRITE_SIZE + 0.5) - 1
                    self.setSpritePos()

                    # When we detect that we changed of box, we end the movement to be able to change direction
                    # Quand on détecte que l'on a changé de case, on met fin au mouvement to pouvoir changer la direction
                    endMov = False
                    
                    if (self.direction == DOWN or self.direction == UP) and (self.screenPosY // SPRITE_SIZE) != ((self.screenPosY - self.speed) // SPRITE_SIZE):

                        endMov = True

                    elif (self.direction == RIGHT or self.direction == LEFT) and (self.screenPosX // SPRITE_SIZE) != ((self.screenPosX - self.speed) // SPRITE_SIZE):

                        endMov = True

                    if endMov:

                        self.moving = False
                        self.spritePos = 0
                        # Not needed
                        # Pas indispensable
                        self.posX = int(self.screenPosX // SPRITE_SIZE)
                        self.posY = int(self.screenPosY // SPRITE_SIZE) - 1
                        
                self.setSpriteDir()
                self.image = self.sprites[self.spriteDir][self.spritePos]

            # If it's an IA
            # Si c'est une IA
            else:

                # TODO: IA
                pass
                
        # ...And if he's dead
        # ...Et s'il est mort
        else:

            self.kill()
            # TODO: Play death anim
            pass
            
    # Check events determined by what's in the box
    # Vérifie des évènement déterminés par ce qu'il y a dans la case
    def checkBox(self, level):

        box = level.itemTable[self.posX][self.posY]

        if box.item == BONUS:

            # On destroy, the bonus return is type
            # A la destuction, le bonus retourne son type
            bonus = box.destroy(level)

            if bonus == 0:

                self.bombsMax += 1

            elif bonus == 1:

                self.power += 1

            # It would be bad if the player move too fast
            # Il ne faudrait pas que le joueur aille trop vite
            elif self.speed < 2:

                self.speed += 0.25

        # If there is an explosion, then you're dead!
        # S'il y a une explosion, vous êtes mort!
        elif box.item == EXPLOSION and self.num == 0:

            self.alive = False
            self.deathSound.play()

    # Drop a bomb if possible
    # Pose une bombe s'il le peut
    def checkBombDrop(self, level, keyPressed):

        # If the player pressed the bomb drop key, if the player droped not too many bombs and the box is empty, then drop bomb
        # Si le joueur appuye sur la touche pour poser une bombe, qu'il n'en a pas posé trop et que la case est libre, alors poser une bombe
        if keyPressed[KEYS[self.num][4]]:
            
            bombX = int((self.screenPosX + self.getOffset()[0]) / SPRITE_SIZE)
            bombY = int((self.screenPosY + self.getOffset()[1]) / SPRITE_SIZE)
            bombX = self.posX
            bombY = self.posY
            
            if level.itemTable[bombX][bombY].item == NOTHING and self.bombs < self.bombsMax:
                
                # Update the group sprites, the item table. Don't mind the layer, it will be used one day but is useless now
                # Met à jour le groupe de sprite et le tableau d'objets. Ne faites pas attention au layer, il est inutile pour l'instant
                bomb = Bomb(self)
                level.add(bomb, layer = bombY)
                level.itemTable[bombX][bombY] = bomb
                # Update bombs droped simultanously by the player
                # Mise à jour le nombre de bombes posée simultanément par le joueur
                self.bombs += 1

    # Check whether the player can move in this direction or not
    # Vérifie si le joueur peut bouger dans la direction
    def checkDirection(self, level, direction):

        # If there is something in the next box that the player can't pass trough (item >= 3), the player can't go on it
        # S'il y a quelque chose dans la prochaine case et que le joueur ne peut pas passer à travers (item >=3), alors il ne peut pas y aller
        if level.itemTable[self.posX + direction[0]][self.posY + direction[1]].item >= 3:

            return(False)
        
        else:

            return(True)

    def setDirection(self, level, keyPressed):

        # If the player is moving, so between two boxes, he can only reverse his movement if there is nothing he can't pass through in the box he left
        # Si le joueur est en mouvement, donc entre deux cases, il peut seulement inverser son mouvement s'il n'y a rien en dur dans la case qu'il a quitté
        if self.moving:
            
            if self.direction == RIGHT and keyPressed[KEYS[self.num][2]]:# and self.checkDirection(level, LEFT):
            
                self.direction = LEFT
                
            elif self.direction == LEFT and keyPressed[KEYS[self.num][3]]:# and self.checkDirection(level, RIGHT):
                    
                self.direction = RIGHT
                    
            elif self.direction == UP and keyPressed[KEYS[self.num][1]]:# and self.checkDirection(level, DOWN):
                    
                self.direction = DOWN
                    
            elif self.direction == DOWN and keyPressed[KEYS[self.num][0]]:# and self.checkDirection(level, UP):
                    
                self.direction = UP

        # Else, if the player is right in one box, he can choose any direction he wants if it's possible
        # Sinon, si le joueur et pile dans une case, il peut choisir le direction qu'il veut si c'est possible
        else:

            # If the player don't press left or right, or press both, don't try to move on the X axis
            #   Else, try to move 
            # Si le joueur n'appuye pas sur gauche et droite, ou bien sur les deux à la fois, ne pas essayer de bouger sur l'axe X
            #   Sinon, essayer de bouger selon la touche pressée
            if (keyPressed[KEYS[self.num][3]] and keyPressed[KEYS[self.num][2]]) or ((not keyPressed[KEYS[self.num][3]]) and (not keyPressed[KEYS[self.num][2]])):
                
                dirX = 0
                
            elif keyPressed[KEYS[self.num][3]]:
                
                dirX = 1
                
            else:
                
                dirX = -1
                
            # Same thing on Y axis
            # Même chose sur l'axe Y
            if (keyPressed[KEYS[self.num][0]] and keyPressed[KEYS[self.num][1]]) or ((not keyPressed[KEYS[self.num][0]]) and (not keyPressed[KEYS[self.num][1]])):

                dirY = 0

            elif keyPressed[KEYS[self.num][1]]:

                dirY = 1

            else:

                dirY = -1

            # We try to update the direction, and first try with the direction different from the current
            # On essaye de mettre à jour la direction, et on essaye d'abord avec les directions différentes de l'actuelle
            if self.direction[0] == 0 and dirX != 0:
                
                self.direction = (dirX, 0)
                # The player will move only if he can
                # Le joueur va bouger uniquement s'il le peut
                self.moving = self.checkDirection(level, self.direction)

            elif self.direction[1] == 0 and dirY != 0:
                
                self.direction = (0, dirY)
                self.moving = self.checkDirection(level, self.direction)

            elif dirX != 0:
                
                self.direction = (dirX, 0)                
                self.moving = self.checkDirection(level, self.direction)
                    
            elif dirY != 0:
                
                self.direction = (0, dirY)
                self.moving = self.checkDirection(level, self.direction)

    # Set a new sprite direction depending on the player's direction
    # Met une nouvelle direction selon la direction du joueur
    def setSpriteDir(self):

        if self.direction == DOWN:
            
            self.spriteDir = 0
            
        if self.direction == UP:
            
            self.spriteDir = 2
            
        if self.direction == RIGHT:
            
            self.spriteDir = 1
            
        if self.direction == LEFT:
            
            self.spriteDir = 3
            
    # Update the animation position depending on player's direction and position on the screen
    # Met à jour la position dans l'animation selon la direction du joueur et sa position sur l'écran
    def setSpritePos(self):

        if self.moving:

            # If the player move up or down, we take into account the bottom of the sprite, else we take the left side
            # Si le joueur bouge vers le haut ou le bas, on prend en compte le bas du sprite, sinon on prend le côté gauche
            if self.direction == DOWN or self.direction == UP:

                position = self.rect.bottom

            else:

                position = self.rect.left

            # It is difficult to explain, a drawing would be better, but at the beginning, the end, and right in the middle, we set to animation 0
            #   Else, if we are not at one of these position, whether it's at the left or right we put animation 1 or 2
            # C'est difficile à expliquer, un dessin serait plus parlant, mais au début, pile au milieu et la fin du déplacement, on met l'animation 0
            #   Sinon, si l'on est pas à l'une de ces position, selon  si c'est à gauche ou à droite ou met l'animation 1 ou 2
            if position%16 < 7 and position%16 > 0:
                    
                self.spritePos = 2
                    
            elif position%8 < 7 and position%16 > 0:
                    
                self.spritePos = 1
                    
            else:
                    
                self.spritePos = 0

        # If we don't move, we put back the animation 0
        # Si l'on ne bouge pas on remet l'animation 0      
        else:
            
            self.spritePos = 0

    # Return a little offset used to drop bombs ahead of the player
    # Retourne un petit décalage utilisé pour poser des bombes juste devant le joueur
    def getOffset(self):

        if self.direction == DOWN:

            return(0, 4)

        elif self.direction == UP:

            return(0, -4)

        elif self.direction == LEFT:

            return(-4, 0)

        elif self.direction == RIGHT:

            return(4, 0)

        
# The most important, the group which contain items and players, and load the level
# Le plus important, le groupe qui contient les objets et les joueurs, et qui charge le niveau
class Level(pygame.sprite.LayeredDirty):

    # The constructor of the class which allow us to create an instance of the level number numLevel
    # Le constructeur de la classe qui permet de créer une instance du niveau numéro numLevel
    def __init__(self, window, numLevel, numPlayers):

        # We call LayeredDirty's constructor to get the specifics methods and attibutes
        # On appelle le constructeur de LayeredDirty pour bénéficier des méthodes et attributs spécifiques
        pygame.sprite.LayeredDirty.__init__(self)

        # We open the level's file and we extract useful infos
        # On ouvre le fichier du niveau et on extrait les infos utiles
        with open(os.path.join("Levels", "Level " + str(numLevel) + ".txt"), "r") as file:

            # Each time, we get all the ligne, then strip the human readable infos and the end of ligne character
            # A chaque fois, on prend toute la ligne, on enlève les infos pour les utilisateurs et le caractère de fin de ligne            
            self.name = file.readline().replace("Level name: ", "").replace("\n", "")
            self.spriteSet = file.readline().replace("Sprite Set: ", "").replace("\n", "")
            self.spriteSetPath = os.path.join("Pictures", "Levels", self.spriteSet)
            self.playerMax = int(file.readline().replace("Player Maximum: ", "").replace("\n", ""))
            
            self.spawns = []
            for i in range(self.playerMax):
                
                spawn = file.readline().replace("Spawn " + str(i+1) + ": ", "").replace("\n", "").split(", ")
                self.spawns.append((int(spawn[0]), int(spawn[1])))
                
            self.width = int(file.readline().replace("Widht: ", "").replace("\n", ""))
            self.height = int(file.readline().replace("Heigth: ", "").replace("\n", ""))

            # There are only human readable infos on this ligne, pass it
            # Il n'y a que des infos pour l'utilisateur sur cette ligne, la passer
            file.readline()
            # We now load a table of all the items and initialize it with the file
            self.itemTable = [[None for i in range(self.height)] for j in range(self.width)]
            for i in range(self.height):
                
                levelLine = file.readline().replace("\n", "")
                itemLine = []
                
                for j in range(self.width):
                    
                    itemType = int(levelLine[j])
                    
                    if itemType == 0:

                        newItem = Ground()

                    elif itemType == 5:

                        newItem = Wall()

                    elif itemType == 4:

                        newItem = Breakable(j, i, self.spriteSetPath)
                        self.add(newItem, layer = self.height - i)
                                                
                    self.itemTable[j][i] = newItem

        # We load the backgrounds sprites and generate it
        # On charge les sprites de fond et on génère celui-ci
        self.wallSprite = pygame.image.load(os.path.join(self.spriteSetPath, "Wall.png")).convert()
        self.groundSprite = pygame.image.load(os.path.join(self.spriteSetPath, "Ground.png")).convert()
        for y in range(self.height):
            
            for x in range(self.width):
                
                if self.itemTable[x][y].item == WALL:
                    
                    window.blit(self.wallSprite, (SPRITE_SIZE*x, SPRITE_SIZE*y))
                    
                else:
                    
                    window.blit(self.groundSprite, (SPRITE_SIZE*x, SPRITE_SIZE*y))
                                        
        # Once done, we save it in an image, and set it as background of the sprite's group
        # Une fois cela fait, on le sauvegarde dans une mage et on le définit comme fond du group de sprite
        pygame.image.save(window, os.path.join("Levels", "Level " + str(numLevel) + ".png"))
        self.background = pygame.image.load(os.path.join("Levels", "Level " + str(numLevel) + ".png")).convert()
        self.clear(window, self.background)

        # Let's create the players! They will be stored in this list
        # Créons maintenant les joueurs! Il seront stockés dans cette liste
        self.numPlayers = numPlayers
        self.players = []
        for i in range(self.playerMax):

            # At each loop, we decrement numPlayers, wich represent the number of human players
            # A chaque tour de la boucle, on décrémente numPlayers, qui represente le nombre de joueurs humains           
            if numPlayers > 0:
                
                ia = 0
                
            else:
                
                ia = 1

            # We create the player and add it to the group
            player = Player(i, self.spawns[numPlayers - 1], ia)
            self.players.append(player)
            self.add(player, layer = player.rect.bottom)
            numPlayers -= 1
