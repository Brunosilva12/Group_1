import pygame
from pygame.locals import *

#Lancer pygame
pygame.init()
#Ouvrir une fenêtre de la même taille que le jeu
fenetre = pygame.display.set_mode((1000,600))
running = 1

#Chargement image
menu = pygame.image.load("menu 1.jpg").convert()
fenetre.blit(menu, (0,0))
pygame.display.flip()

#Boucle perpétuelle qui permet de garder la fenêtre ouverte
while running :
    for event in pygame.event.get():
        if event.type == QUIT :
            continuer = 0
            pygame.quit()
            exit()



