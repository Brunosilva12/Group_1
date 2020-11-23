import pygame
from pygame.locals import *

pygame.init()
fenetre = pygame.display.set_mode((1000,600))
continuer = 1

while continuer :
    for event in pygame.event.get():
        if event.type == QUIT :
            continuer = 0
            pygame.quit()
            exit()