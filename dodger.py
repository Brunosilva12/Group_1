import pygame
import random
import sys
from pygame.locals import *

# from menu import Menu

WINDOWWIDTH = 1000  # Taille de l'écran
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)  # Couleur du text
FPS = 60  # Nombre d'image par secondes

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paramètres des entités
HOSPMINSIZE = 100
HOSPMAXSIZE = 150
ADDNEWHOSPRATE = 100

VIRUSSIZE = 35
ADDNEWVIRUSRATE = 40

VACCINSIZE = 35
ADDNEWVACCINRATE = 50

SPEED = 2

# PLAYERMOVERATE = 5
MAXHEALTH = 3
count = 0


class Player(object):
    def __init__(self, x, y):
        self.currentHealth = 3
        self.max_health = 3
        self.player_move_rate = 5
        self.image = pygame.image.load('baddie.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


bat = Player(WINDOWWIDTH // 2, WINDOWHEIGHT - 50)


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


def playerHitVirus(playerRect, viruss):  # Définir la fonction : collision entre le player et le virus
    for v in viruss:
        if playerRect.colliderect(v['rect']):  # Détecter la collision
            viruss.remove(v)  # Supprimer le virus à chaque fois que le player le toucher
            return True
    return False


def playerHasHitBaddie(playerRect, hospitals):  # Définir la fonction : collision entre le player et l'hôpital
    for h in hospitals:
        if playerRect.colliderect(h['rect']):  # Détecter la collision
            return True
    return False


def playerHitVaccine(playerRect, vaccines):  # Définir la fonction : collision entre le player et le vaccin
    for va in vaccines:
        if playerRect.colliderect(va['rect']):  # Détecter la collision
            vaccines.remove(va)  # Supprimer le vaccin à chaque fois que le player le toucher
            return True
    return False


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# draw lives
img = pygame.image.load("vie.png")
vies = pygame.transform.scale(img, (100, 76))
vies.set_colorkey(BLACK)


def draw_lives(surf, x, y, MAXHEALTH, img):
    for i in range(MAXHEALTH):
        img_rect = img.get_rect()
        img_rect.x = x + 45 * i
        img_rect.y = y
        surf.blit(img, img_rect)


# on garde les rectangles au cas où on veut remettre ça
# def drawHealthMeter(currentHealth):
# for i in range(MAXHEALTH):
# pygame.draw.rect(windowSurface, RED, (870 + (10 * currentHealth) - i * 30, 35, 29, 10))
# for i in range(currentHealth):
# pygame.draw.rect(windowSurface, WHITE, (870 + (10 * currentHealth) - i * 30, 35, 29, 10), 1)


# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Loco-vid')
pygame.mouse.set_visible(False)

# Background image
BACKGROUND = pygame.image.load('fond.png').convert()  # fond
x = 0

# Set up the same fonts for everything
font = pygame.font.SysFont(None, 48)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('Gover.wav')
pygame.mixer.music.load('Final.wav')

# Set up images.
# playerImage = pygame.image.load('baddie.png')
# playerRect = playerImage.get_rect()
virusImage = pygame.image.load('virus.png')
hospImage = pygame.image.load('hos.jpg')
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
    hospitals = []
    viruss = []
    vaccines = []
    score = 0
    moveLeft = moveRight = moveUp = moveDown = False
    virusAddCounter = 0
    vaccinAddCounter = 0
    hospAddCounter = 0

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
                bat.rect.centerx = event.pos[0]
                bat.rect.centery = event.pos[1]

        # Add new baddies at the top of the screen, if needed.
        virusAddCounter += 1
        vaccinAddCounter += 1
        hospAddCounter += 1

        if virusAddCounter == ADDNEWVIRUSRATE:
            virusAddCounter = 0
            virusSize = VIRUSSIZE
            newVirus = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - virusSize), 0 - virusSize, virusSize,
                                            virusSize),
                        'speed': SPEED,
                        'surface': pygame.transform.scale(virusImage, (virusSize, virusSize)),
                        }

            viruss.append(newVirus)

        if vaccinAddCounter == ADDNEWVACCINRATE:
            vaccinAddCounter = 0
            vaccinSize = VACCINSIZE
            newVaccin = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - vaccinSize), 0 - vaccinSize, vaccinSize,
                                             vaccinSize),
                         'speed': SPEED,
                         'surface': pygame.transform.scale(vaccinImage, (vaccinSize, vaccinSize)),
                         }

            vaccines.append(newVaccin)

        if hospAddCounter == ADDNEWHOSPRATE:
            hospAddCounter = 0
            hospSize = random.randint(HOSPMINSIZE, HOSPMAXSIZE)
            newHosp = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - hospSize), 0 - hospSize, hospSize, hospSize),
                       'speed': SPEED,
                       'surface': pygame.transform.scale(hospImage, (hospSize, hospSize)),
                       }
            hospitals.append(newHosp)

        # Move the player around.
        if moveLeft and bat.rect.left > 0:
            bat.rect.move_ip(-1 * bat.player_move_rate, 0)
        if moveRight and bat.rect.right < WINDOWWIDTH:
            bat.rect.move_ip(bat.player_move_rate, 0)
        if moveUp and bat.rect.top > 0:
            bat.rect.move_ip(0, -1 * bat.player_move_rate)
        if moveDown and bat.rect.bottom < WINDOWHEIGHT:
            bat.rect.move_ip(0, bat.player_move_rate)

        # Move the baddies down.
        for h in hospitals:
            h['rect'].move_ip(0, h['speed'])

        # Delete baddies that have fallen past the bottom.
        for h in hospitals[:]:
            if h['rect'].top > WINDOWHEIGHT:
                hospitals.remove(h)

        # Move the virus down.
        for v in viruss:
            v['rect'].move_ip(0, v['speed'])

        # Delete virus that have fallen past the bottom.
        for v in viruss[:]:
            if v['rect'].top > WINDOWHEIGHT:
                viruss.remove(v)

        # Move the vaccine down.
        for va in vaccines:
            va['rect'].move_ip(0, va['speed'])

        # Delete vaccines that have fallen past the bottom.
        for va in vaccines[:]:
            if va['rect'].top > WINDOWHEIGHT:
                vaccines.remove(va)

        # Draw the game world on the window.
        windowSurface.fill((0, 0, 0))

        # Background image settings
        rel_x = x % BACKGROUND.get_rect().height
        windowSurface.blit(BACKGROUND, (0, rel_x - BACKGROUND.get_rect().height))
        if rel_x < WINDOWHEIGHT:
            windowSurface.blit(BACKGROUND, (0, rel_x))
        x += 1

        # Draw the player's rectangle.
        windowSurface.blit(bat.image, bat.rect)

        # Draw each object.
        for h in hospitals:
            windowSurface.blit(h['surface'], h['rect'])

        for v in viruss:
            windowSurface.blit(v['surface'], v['rect'])

        for va in vaccines:
            windowSurface.blit(va['surface'], va['rect'])

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        draw_lives(windowSurface, WINDOWWIDTH - 200, 5, MAXHEALTH, vies)
        pygame.display.update()

        # Check if any of the hospital have hit the player.
        if playerHasHitBaddie(bat.rect, hospitals):
            if score > topScore:
                topScore = score  # set new top score
            if MAXHEALTH == 0:
                MAXHEALTH += 3
            elif MAXHEALTH == 1:
                MAXHEALTH += 2
            elif MAXHEALTH == 2:
                MAXHEALTH += 1
            break

        # Check if any of the virus have hit the player.
        if playerHitVirus(bat.rect, viruss):
            if score > topScore:
                topScore += 100  # add 100 to the topScore

        # Check if any of the vaccines have hit the player.
        if playerHitVaccine(bat.rect, vaccines):
            if score > topScore:
                topScore -= 100  # subtract 100 to the topScore
            MAXHEALTH -= 1
            count += 1
            if MAXHEALTH == 0:
                MAXHEALTH += 3
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
