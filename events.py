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



# permanent_events(event): handle events that we always want to handle, like if the user want to quit or toggle fullscreen
#                          traite les évènements que nous voulons toujours traiter, comme lorsque l'utilisateur veut quitter ou basculer en plein écran

def permanent_events(event):

    # If the user try to close the program hitting ESCAPE, ALT-F4 or by pressing the window's close button, ask for confirmation and close or resume
    # Si l'utilisateur cherche à fermer le programme en appuyant sur ECHAP, ALT-F4 ou sur le boutton de fermeture de la fenêtre, demander confirmation puis fermer ou continuer
    if (event.type == QUIT) or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == KMOD_LALT|K_F4)):
        
        ## TODO: Draw the message box, Save program's state
        while 1:
            
            for event in pygame.event.get():
                
                # If he put his mouse on the yes button, change the button's apparence
                # S'il passe sa souris sur le boutton oui, changer l'apparence du boutton
                if event.type == MOUSEMOTION
                and (event.pos[0] >= yes_button.rect[0] and event.pos[0] <= (yes_button.rect[0] +yes_button.rect[3]))
                and (event.pos[1] >= yes_button.rect[1] and event.pos[1] <= (yes_button.rect[1] +yes_button.rect[4])):

                    yes_button.hoover()
                    
                # If he put his mouse on the no button, change the button's apparence
                # S'il passe sa souris sur le boutton non, changer l'apparence du boutton
                if event.type == MOUSEMOTION
                and (event.pos[0] >= no_button.rect[0] and event.pos[0] <= (no_button.rect[0] + no_button.rect[3]))
                and (event.pos[1] >= no_button.rect[1] and event.pos[1] <= (no_button.rect[1] + no_button.rect[4])):

                    no_button.hoover()
                    
                # If he hit again ALT-F4, or if he confirms (press on yes button), then exit
                # S'il appuie encore une fois sur ALT-F4, ou s'il confirme (appuie sur le boutton oui), alors quitter
                if (event.type == KEYDOWN and event.key == KMOD_LALT|K_F4)
                or (event.type == MOUSEBUTTONDOWN
                    and (event.pos[0] >= yes_button.rect[0] and event.pos[0] <= (yes_button.rect[0] +yes_button.rect[3]))
                    and (event.pos[1] >= yes_button.rect[1] and event.pos[1] <= (yes_button.rect[1] +yes_button.rect[4]))):

                    pygame.quit()
                    sys.exit()
                    
                # If he doesn't confirm, then resume
                # S'il ne confirme pas, alors revenir au programme
                if event.type == MOUSEBUTTONDOWN
                and (event.pos[0] >= no_button.rect[0] and event.pos[0] <= (no_button.rect[0] + no_button.rect[3]))
                and (event.pos[1] >= no_button.rect[1] and event.pos[1] <= (no_button.rect[1] + no_button.rect[4])):

                    ## TODO: Clear the message box, Restaure program's state

            pygame.display.flip()

    # If the user hit F11, switch to fullscreen
    # Si l'utilisateur appuie sur F11, basculer en plein écran
    elif event.type == KEYDOWN and event.key == K_F11:
        pygame.display.toggle_fullscreen()
        print("togle!!!")
