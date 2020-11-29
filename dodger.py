import pygame
import random
import sys
from pygame.locals import *

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (127, 127, 127)

WINDOWWIDTH = 1000  # Taille de l'écran
WINDOWHEIGHT = 600
TEXTCOLOR = WHITE  # Couleur du text
FPS = 60  # Nombre d'image par secondes

# Paramètres des entités
SPEED = 2
scroll = 0
score_level1 = 400


class Object():
    def __init__(self, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

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
        self.image = pygame.image.load('hos.jpg').convert_alpha()
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


class GameState(object):
    def __init__(self):
        self.state = "main game"

    def main_game(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()

            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where to the cursor.
                bat.rect.centerx = event.pos[0]
                bat.rect.centery = event.pos[1]

    def state_manager(self):
        if self.state == "main_game":
            self.main_game()


class Button(object):
    def __init__(self, color_button, x_button, y_button, width, height, text=''):
        self.color = color_button
        self.x = x_button
        self.y = y_button
        self.width = width
        self.height = height
        self.text = text

    def draw(self, window, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(window, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font_button = pygame.font.SysFont('comicsans', 60)
            text = font_button.render(self.text, 1, (255, 255, 255))
            window.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


def terminate():  # Fermer la fenêtre du jeu
    pygame.quit()
    sys.exit()


# Menu
def Menu():

    menu = pygame.image.load("menu 1.jpg").convert()
    img = pygame.transform.scale(menu, (1000, 600))
    windowSurface.blit(img, (0, 0))


# Option
def Option():
    help = pygame.image.load("Help.png").convert()
    img = pygame.transform.scale(help, (1000, 600))
    windowSurface.blit(img, (0, 0))

    pygame.display.update()
    waitForPlayerToGetBack()

def waitForPlayerToGetBack():
    while True:
        for event_Key in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event_Key.type == QUIT:
                terminate()
            if event_Key.type == KEYDOWN:
                if event_Key.key == K_ESCAPE:  # Pressing ESC quits.
                    terminate()
            if event_Key.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    Menu()

def waitForPlayerToPressKey():  # Lancer le jeu ou le fermer
    while True:
        for event_Key in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event_Key.type == QUIT:
                terminate()
            if event_Key.type == KEYDOWN:
                if event_Key.key == K_ESCAPE:  # Pressing ESC quits.
                    terminate()
            if event_Key.type == pygame.MOUSEBUTTONDOWN:
                if start_button.isOver(pos):
                    return
            if event_Key.type == pygame.MOUSEBUTTONDOWN:
                if option_button.isOver(pos):
                    Option()



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


def drawText(text, surface, x_t, y_t, color, size):
    font = pygame.font.SysFont(None, size)
    textobj = font.render(text, 1, color)
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

def level2():
    niveau2 = pygame.image.load("level2.png")
    niveau2_img = pygame.transform.scale(niveau2, (1000, 600))

    windowSurface.blit(niveau2_img, (0, 0))

def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()

def b_special(msg, x, y, w, h, ic, ac):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(windowSurface, ac, (x, y, w, h))
        if click[0] == 1:
                level2()
    else:
        pygame.draw.rect(windowSurface, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    windowSurface.blit(textSurf, textRect)


def win_mode():
    drawText('LEVEL COMPLETE', windowSurface, 350, (-250 + scroll), RED, 48)
    windowSurface.blit(level1Image, (450, -500 + scroll))
    drawText('INFECT DONALD TRUMP !', windowSurface, 300, (-700 + scroll), RED, 48)
    b_special("Level 2", 800, 400, 150, 50, BLACK, GREY)

    pygame.mixer.music.stop()
    levelSound.play()

def show_GameOver_screen():
    pygame.mixer.music.stop()
    gameOverSound.play()
    pygame.mouse.set_visible(True)

    drawText('GAME OVER', windowSurface, 300, (WINDOWHEIGHT / 2), (0, 0, 0), 100)
    start_button = Button((0, 0, 0), 348, 428, (WINDOWHEIGHT / 2), 70, "Restart")
    start_button.draw(windowSurface, (255, 255, 255))
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Loco-vid')

# Background image
BACKGROUND = pygame.image.load('fond.png').convert()  # fond
BACKGROUND_rect = BACKGROUND.get_rect()
x = 0

# Set up the same fonts for everything
font = pygame.font.SysFont(None, 48)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('Gover.wav')
pygame.mixer.music.load('Final.wav')
levelSound = pygame.mixer.Sound('Win.wav')

# Show the "Start" screen.
windowSurface.fill((0, 0, 0))
Menu()
level1Image = pygame.image.load('Doni.png')
level1Image = pygame.transform.scale(level1Image, (133, 100))

# Draw the button on the menu
start_button = Button((0, 0, 0), 348, 428, 305, 70, "Start")
start_button.draw(windowSurface, (255, 255, 255))
option_button = Button((0, 0, 0), 360, 515, 268, 45, "How to play")
option_button.draw(windowSurface, (255, 255, 255))
back_button = Button((0, 0, 0), 25, 25, 125, 50, "Back")
back_button.draw(windowSurface, (255, 255, 255))
pygame.display.update()
waitForPlayerToPressKey()

############# START ####################
Score = 0
bat = Player(WINDOWWIDTH // 2, WINDOWHEIGHT - 50)
virus = Virus()
vaccine = Vaccine()
hospital = Hospital()

while True:
    # Set up the start of the game.
    hospitals = []
    viruss = []
    vaccines = []
    timer = 0
    moveLeft = moveRight = moveUp = moveDown = False
    virusAddCounter = 0
    vaccinAddCounter = 0
    hospAddCounter = 0
    game_state = GameState()

    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.rewind()  # relancer directement la musique

    while True:  # The game loop runs while the game part is playing.
        game_state.main_game()
        pygame.mouse.set_visible(False)
        # Draw the game world on the window.
        windowSurface.fill((0, 0, 0))

        # Background image settings
        if timer < 750:
            x += 1
        rel_x = x % BACKGROUND.get_rect().height
        windowSurface.blit(BACKGROUND, (0, rel_x - BACKGROUND.get_rect().height))
        if rel_x < WINDOWHEIGHT:
            windowSurface.blit(BACKGROUND, (0, rel_x))

        # Enter in win mode
        if Score >= score_level1:
            timer += 1
            if timer < 750:
                scroll += 1
            win_mode()
        # Add new baddies at the top of the screen, if needed.
        else:
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

        # Draw the player's rectangle.
        windowSurface.blit(bat.image, bat.rect)

        # Draw each object.
        for h in hospitals:
            windowSurface.blit(h['surface'], h['rect'])

        for v in viruss:
            windowSurface.blit(v['surface'], v['rect'])

        for va in vaccines:
            windowSurface.blit(va['surface'], va['rect'])

        # Level 1
        if Score < score_level1:
            drawText('Score: %s/4000' % (Score), windowSurface, 10, 40, TEXTCOLOR, 36)

        # Draw the lives
        if Score < score_level1:
            draw_lives(windowSurface, WINDOWWIDTH - 200, 5, bat.max_health, vies)
        pygame.display.update()

        # Check if any of the hospital have hit the player.
        if playerHasHitHospitals(bat.rect, hospitals):
            if bat.max_health == 0:
                bat.max_health += 3
            elif bat.max_health == 1:
                bat.max_health += 2
            elif bat.max_health == 2:
                bat.max_health += 1
            Score = 0
            break

        # Check if any of the virus have hit the player.
        if playerHitVirus(bat.rect, viruss):
            if Score < score_level1:
                Score += 100  # add 100 to the topScore

        # Check if any of the vaccines have hit the player.
        if playerHitVaccine(bat.rect, vaccines):
            if Score < score_level1 and Score > 0:
                Score -= 100  # subtract 100 to the topScore
            bat.max_health -= 1
            if bat.max_health == 0:
                bat.max_health += 3
                Score = 0
                break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    show_GameOver_screen()
