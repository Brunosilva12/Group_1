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
SPEED = 2
count = 0


class Player(object):
    def __init__(self, x_pl, y_pl):
        self.max_health = 3
        self.player_move_rate = 5
        self.image = pygame.image.load('baddie.png')
        self.rect = self.image.get_rect()
        self.rect.x = x_pl
        self.rect.y = y_pl


class Hospital(object):
    def __init__(self):
        self.min_size = 100
        self.max_size = 200
        self.add_hosp_rate = 100
        self.image = pygame.image.load('hos.jpg')
        self.rect = self.image.get_rect()


class Virus(object):
    def __init__(self):
        self.size = 35
        self.add_virus_rate = 40
        self.image = pygame.image.load('virus.png').convert_alpha()
        self.rect = self.image.get_rect()


class Vaccine(object):
    def __init__(self):
        self.size = 35
        self.add_vaccine_rate = 50
        self.image = pygame.image.load('vaccin.png').convert_alpha()
        self.rect = self.image.get_rect()


def terminate():  # Fermer la fenêtre du jeu
    pygame.quit()
    sys.exit()


def waitForPlayerToPressKey():  # Lancer le jeu ou le fermer
    while True:
        for event_Key in pygame.event.get():
            if event_Key.type == QUIT:
                terminate()
            if event_Key.type == KEYDOWN:
                if event_Key.key == K_ESCAPE:  # Pressing ESC quits.
                    terminate()
                return


def playerHitVirus(playerRect, virus_):  # Définir la fonction : collision entre le player et le virus
    for v_ in virus_:
        if playerRect.colliderect(v_['rect']):  # Détecter la collision
            viruss.remove(v_)  # Supprimer le virus à chaque fois que le player le toucher
            return True
    return False


def playerHasHitHospitals(playerRect, hospitals_):  # Définir la fonction : collision entre le player et l'hôpital
    for h_ in hospitals_:
        if playerRect.colliderect(h_['rect']):  # Détecter la collision
            return True
    return False


def playerHitVaccine(playerRect, vaccines_):  # Définir la fonction : collision entre le player et le vaccin
    for va_ in vaccines_:
        if playerRect.colliderect(va_['rect']):  # Détecter la collision
            vaccines.remove(va_)  # Supprimer le vaccin à chaque fois que le player le toucher
            return True
    return False


def drawText(text, font_t, surface, x_t, y_t):
    textobj = font_t.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x_t, y_t)
    surface.blit(textobj, textrect)


# draw lives
img = pygame.image.load("vie.png")
vies = pygame.transform.scale(img, (130, 86))
vies.set_colorkey(BLACK)


def draw_lives(surf, x_l, y_l, max_health_l, img_l):
    for i in range(max_health_l):
        img_rect = img_l.get_rect()
        img_rect.x = x_l + 45 * i
        img_rect.y = y_l
        surf.blit(img_l, img_rect)


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

# Show the "Start" screen.
windowSurface.fill((0, 0, 0))
#drawText('Loco-vid', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
#drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
#pygame.display.update()

#Ouvrir une fenêtre de la même taille que le jeu
fenetre = pygame.display.set_mode((1000,600))
running = 1

#Chargement image
menu = pygame.image.load("menu 1.jpg").convert()
img = pygame.transform.scale(menu, (1000, 600))
fenetre.blit(img, (0,0))
pygame.display.flip()

#Attendre que le joueur presse une touche
pygame.display.update()
waitForPlayerToPressKey()

############# START ####################

topScore = 0
bat = Player(WINDOWWIDTH // 2, WINDOWHEIGHT - 50)
virus = Virus()
vaccine = Vaccine()
hospital = Hospital()

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

        if virusAddCounter == virus.add_virus_rate:
            virusAddCounter = 0
            virusSize = virus.size
            newVirus = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - virusSize), 0 - virusSize, virusSize,
                                            virusSize),
                        'speed': SPEED,
                        'surface': pygame.transform.scale(virus.image, (virusSize, virusSize)),
                        }

            viruss.append(newVirus)

        if vaccinAddCounter == vaccine.add_vaccine_rate:
            vaccinAddCounter = 0
            vaccinSize = vaccine.size
            newVaccin = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - vaccinSize), 0 - vaccinSize, vaccinSize,
                                             vaccinSize),
                         'speed': SPEED,
                         'surface': pygame.transform.scale(vaccine.image, (vaccinSize, vaccinSize)),
                         }

            vaccines.append(newVaccin)

        if hospAddCounter == hospital.add_hosp_rate:
            hospAddCounter = 0
            hospSize = random.randint(hospital.min_size, hospital.max_size)
            newHosp = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - hospSize), 0 - hospSize, hospSize, hospSize),
                       'speed': SPEED,
                       'surface': pygame.transform.scale(hospital.image, (hospSize, hospSize)),
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

        # Move the hospitals down.
        for h in hospitals:
            h['rect'].move_ip(0, h['speed'])

        # Delete the hospitals that have fallen past the bottom.
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
        drawText('Score: %s' % score, font, windowSurface, 10, 0)
        drawText('Top Score: %s' % topScore, font, windowSurface, 10, 40)

        draw_lives(windowSurface, WINDOWWIDTH - 200, 5, bat.max_health, vies)
        pygame.display.update()

        # Check if any of the hospital have hit the player.
        if playerHasHitHospitals(bat.rect, hospitals):
            if score > topScore:
                topScore = score  # set new top score
            if bat.max_health == 0:
                bat.max_health += 3
            elif bat.max_health == 1:
                bat.max_health += 2
            elif bat.max_health == 2:
                bat.max_health += 1
            break

        # Check if any of the virus have hit the player.
        if playerHitVirus(bat.rect, viruss):
            if score > topScore:
                topScore += 100  # add 100 to the topScore

        # Check if any of the vaccines have hit the player.
        if playerHitVaccine(bat.rect, vaccines):
            if score > topScore:
                topScore -= 100  # subtract 100 to the topScore
            bat.max_health -= 1
            count += 1
            if bat.max_health == 0:
                bat.max_health += 3
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
