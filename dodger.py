import pygame
import random
import sys
from pygame.locals import *

WINDOWWIDTH = 800  # Taille de l'écran
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)  # Couleur du text
FPS = 60  # Nombre d'image par secondes

# Paramètres des entités
HOSPMINSIZE = 40
HOSPMAXSIZE = 100
ADDNEWHOSPRATE = 100

BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
MINSPEED = 1
MAXSPEED = 3
ADDNEWBADDIERATE = 20

VACCINMINSIZE = 10
VACCINMAXSIZE = 40
ADDNEWVACCINRATE = 50

PLAYERMOVERATE = 5


def terminate():  # Fermer la fenêtre du jeu
    pygame.quit()
    sys.exit()


def waitForPlayerToPressKey():  # Lancer le jeu ou le fermer
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # Pressing ESC quits.
                    terminate()
                return


def playerHasHitBaddie(playerRect, baddies, hops):
    for c in hops:
        if playerRect.colliderect(c['rect']):
            return True
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    for v in vaccin:
        if playerRect.colliderect(v['rect']):
            return True
    return False


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Loco-vid')
pygame.mouse.set_visible(False)

BACKGROUND = pygame.image.load('fond.png').convert()  # fond
x = 0

# Set up the fonts.
font = pygame.font.SysFont(None, 48)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('Gover.wav')
pygame.mixer.music.load('Final.wav')

# Set up images.
playerImage = pygame.image.load('baddie.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('virus.png')
hospImage = pygame.image.load('hosp.png')
vaccinImage = pygame.image.load('vaccin.png')

# Show the "Start" screen.
windowSurface.fill((0, 0, 0))
drawText('Loco-vid', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

############# START ####################
topScore = 0
while True:
    # Set up the start of the game.
    baddies = []
    vaccin = []
    hosp = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    baddieAddCounter = 0
    vaccinAddCounter = 0
    hospAddCounter = 0

    baddieAddCounter += 1
    vaccinAddCounter += 1
    hospAddCounter += 1

    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.rewind()  # relancer directement la musique

    while True:  # The game loop runs while the game part is playing.
        score += 1  # Increase score.

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where to the cursor.
                playerRect.centerx = event.pos[0]
                playerRect.centery = event.pos[1]
        # Add new baddies at the top of the screen, if needed.

        if hospAddCounter == ADDNEWHOSPRATE:
            hospAddCounter = 0
            hospSize = random.randint(HOSPMINSIZE, HOSPMAXSIZE)
            newHosp = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - hospSize), 0 - hospSize, hospSize, hospSize),
                       'speed': random.randint(MINSPEED, MAXSPEED),
                       'surface': pygame.transform.scale(hospImage, (hospSize, hospSize)),
                       }
            hosp.append(newHosp)
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - baddieSize), 0 - baddieSize, baddieSize,
                                             baddieSize),
                         'speed': random.randint(MINSPEED, MAXSPEED),
                         'surface': pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                         }

            baddies.append(newBaddie)

        if vaccinAddCounter == ADDNEWVACCINRATE:
            vaccinAddCounter = 0
            vaccinSize = random.randint(VACCINMINSIZE, VACCINMAXSIZE)
            newVaccin = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - vaccinSize), 0 - vaccinSize, vaccinSize,
                                             vaccinSize),
                         'speed': random.randint(MINSPEED, MAXSPEED),
                         'surface': pygame.transform.scale(vaccinImage, (vaccinSize, vaccinSize)),
                         }

            vaccin.append(newVaccin)

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Move the hospitals down.
        for c in hosp:
            c['rect'].move_ip(0, c['speed'])

        # Move the baddies down.
        for b in baddies:
            b['rect'].move_ip(0, b['speed'])

        # Move the vaccins down
        for v in vaccin:
            v['rect'].move_ip(0, v['speed'])

        # Delete hosp that have fallen past the bottom.
        for c in hosp[:]:
            if c['rect'].top > WINDOWHEIGHT:
                hosp.remove(c)

        # Delete baddies that have fallen past the bottom.
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Delete vaccins that have fallen past the bottom.
        for v in vaccin[:]:
            if v['rect'].top > WINDOWHEIGHT:
                vaccin.remove(v)

        # Draw the game world on the window.
        windowSurface.fill((0, 0, 0))

        # Background image
        rel_x = x % BACKGROUND.get_rect().height
        windowSurface.blit(BACKGROUND, (0, rel_x - BACKGROUND.get_rect().height))
        if rel_x < WINDOWHEIGHT:
            windowSurface.blit(BACKGROUND, (0, rel_x))
        x += 1

        # Draw the score and top score.
        drawText('Score: %s' % score, font, windowSurface, 10, 0)
        drawText('Top Score: %s' % topScore, font, windowSurface, 10, 40)

        # Draw the player's rectangle.
        windowSurface.blit(playerImage, playerRect)

        # Draw each hosp.
        for c in hosp:
            windowSurface.blit(c['surface'], c['rect'])

        # Draw each baddie.
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        # Draw each vaccin.
        for v in vaccin:
            windowSurface.blit(v['surface'], v['rect'])

        pygame.display.update()

        # Check if any of the baddies have hit the player.
        if playerHasHitBaddie(playerRect, baddies, hosp):
            if score > topScore:
                topScore = score  # set new top score
            break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
