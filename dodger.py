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
FPS = 60  # Nombre d'image par secondes

# Paramètres des entités
SPEED = 2
scroll = 0
scroll2 = 0
score_level = 100
score_level2 = 100


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
        self.rand_size = random.randint(self.min_size, self.max_size)
        self.surface = pygame.transform.scale(self.image, (self.rand_size, self.rand_size))


class Virus(object):
    def __init__(self):
        self.size = 35
        self.add_virus_rate = 40
        self.image = pygame.image.load('virus.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.surface = pygame.transform.scale(self.image, (self.size, self.size))


class Vaccine(object):
    def __init__(self):
        self.size = 35
        self.add_vaccine_rate = 50
        self.image = pygame.image.load('vaccin.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.surface = pygame.transform.scale(self.image, (self.size, self.size))


class GameState:
    def __init__(self):
        self.state = "main game"

    def intro(self):
        Menu()

    def main_game(self):
        pygame.mouse.set_visible(False)

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

        # Move the player around.
        if moveLeft and bat.rect.left > 0:
            bat.rect.move_ip(-1 * bat.player_move_rate, 0)
        if moveRight and bat.rect.right < WINDOWWIDTH:
            bat.rect.move_ip(bat.player_move_rate, 0)
        if moveUp and bat.rect.top > 0:
            bat.rect.move_ip(0, -1 * bat.player_move_rate)
        if moveDown and bat.rect.bottom < WINDOWHEIGHT:
            bat.rect.move_ip(0, bat.player_move_rate)

        mainClock.tick(FPS)


    def state_manager(self):
        if self.state == "intro":
            self.intro()
        if self.state == "main_game":
            self.main_game()


class Button(GameState):
    def __init__(self, color_button, x_button, y_button, width, height, text=''):
        super().__init__()
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
            text = font_button.render(self.text, 1, WHITE)
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


# Draw the button on the menu
start_button = Button(BLACK, 348, 428, (WINDOWHEIGHT / 2)+10, 70, "Start")
restart_button = Button(BLACK, 348, 428, (WINDOWHEIGHT / 2)+10, 70, "Restart")
menu_button = Button(BLACK, 25, 25, 125, 50, "Menu")
option_button = Button(BLACK, 360, 515, (WINDOWHEIGHT / 2)-15, 45, "How to play")
back_button = Button(BLACK, 25, 25, 125, 50, "Back")
lvl_button = Button(BLACK, 348, 428, (WINDOWHEIGHT / 2), 70, "Next level")
nxt_button = Button(BLACK, 348, 428, (WINDOWHEIGHT / 2), 70, "Next level")


# Menu
def Menu():
    menuSound.play()
    pygame.mouse.set_visible(True)
    menu = pygame.image.load("menu 1.jpg").convert()
    img = pygame.transform.scale(menu, (1000, 600))
    windowSurface.blit(img, (0, 0))
    start_button.draw(windowSurface, WHITE)
    option_button.draw(windowSurface, WHITE)

    pygame.display.update()


# Option
def Option():
    help = pygame.image.load("Option.png").convert()
    img = pygame.transform.scale(help, (1000, 600))
    windowSurface.blit(img, (0, 0))
    back_button.draw(windowSurface, WHITE)
    pygame.display.update()


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
                    buttonSound.play()
                    return
            if event_Key.type == pygame.MOUSEBUTTONDOWN:
                if option_button.isOver(pos):
                    buttonSound.play()
                    Option()
            if event_Key.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    buttonSound.play()
                    Menu()
            if event_Key.type == pygame.MOUSEBUTTONDOWN:
                if nxt_button.isOver(pos):
                    buttonSound.play()
                    Menu()


def playerHitVirus(playerRect, viruss):  # Définir la fonction : collision entre le player et le virus
    for v in viruss:
        if playerRect.colliderect(v['rect']):  # Détecter la collision
            viruss.remove(v)  # Supprimer le virus à chaque fois que le player le toucher
            return True
    return False


def playerHasHitHospitals(playerRect, hospitals):  # Définir la fonction : collision entre le player et l'hôpital
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


def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()


def b_special(msg, x, y, w, h, ic, ac):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(windowSurface, ac, (x, y, w, h))
        if click[0] == 1:
            if msg == "Level 2":
                level2()
            elif msg == "Menu":
                Menu()
                waitForPlayerToPressKey()
    else:
        pygame.draw.rect(windowSurface, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    windowSurface.blit(textSurf, textRect)

def win_mode():
    pygame.mixer.music.stop()
    levelSound.play()
    pygame.mouse.set_visible(False)

    drawText('LEVEL COMPLETE', windowSurface, (WINDOWHEIGHT / 2)+50, (-250 + scroll), RED, 48)
    windowSurface.blit(level1Image, ((WINDOWHEIGHT / 2)+125, -550 + scroll))
    drawText('INFECT DONALD TRUMP !', windowSurface, (WINDOWHEIGHT / 2)-10, (-700 + scroll), RED, 48)
    b_special("Level 2", (WINDOWHEIGHT / 2)+125, -450 + scroll, 150, 50, BLACK, GREY)

def show_GameOver_screen():
    pygame.mixer.music.stop()
    gameOverSound.play()
    pygame.mouse.set_visible(True)

    drawText('GAME OVER', windowSurface, 290, (WINDOWHEIGHT / 2), BLACK, 100)
    restart_button.draw(windowSurface, WHITE)
    option_button.draw(windowSurface, WHITE)
    menu_button.draw(windowSurface, WHITE)
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

# Set up sounds.
menuSound = pygame.mixer.Sound('Open.wav')
gameOverSound = pygame.mixer.Sound('Gover.wav')
finalSound = pygame.mixer.music.load('Final.wav')
levelSound = pygame.mixer.Sound('Win.wav')
pickupSound = pygame.mixer.Sound('pickup.wav')
buttonSound = pygame.mixer.Sound('Button.wav')
failSound = pygame.mixer.Sound('Fail.wav')
breakSound = pygame.mixer.Sound('Break.wav')

# Set up the volume.
menuSound.set_volume(0.2)
gameOverSound.set_volume(0.5)
pygame.mixer.music.set_volume(0.1)
levelSound.set_volume(0.1)
pickupSound.set_volume(0.2)
buttonSound.set_volume(0.1)
failSound.set_volume(100)
breakSound.set_volume(0.2)

# Show the "Start" screen.
windowSurface.fill((0, 0, 0))
game_state = GameState()
game_state.intro()
level1Image = pygame.image.load('Doni.png')
level1Image = pygame.transform.scale(level1Image, (133, 100))
world = pygame.image.load('world.png')
world = pygame.transform.scale(world, (350, 170))


def level2():
    levelSound.stop()

    while True:
        # Set up the start of the game.
        timer2 = 0
        scroll2 = 0
        Score2 = 0
        bat.max_health = 3
        x = 0
        hospitals = []
        viruss = []
        vaccines = []
        moveLeft = moveRight = moveUp = moveDown = False
        virusAddCounter = 0
        vaccinAddCounter = 0
        hospAddCounter = 0

        # game_state = GameState()
        level2Sound = pygame.mixer.music.load('Level2.wav')
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.rewind()  # relancer directement la musique
        pygame.mixer.music.set_volume(0.05)
        while True:  # The game loop runs while the game part is playing.
            game_state.main_game()

            # Background image settings
            if timer2 < 750:
                x += 1
            rel_x = x % BACKGROUND.get_rect().height
            windowSurface.blit(BACKGROUND, (0, rel_x - BACKGROUND.get_rect().height))
            if rel_x < WINDOWHEIGHT:
                windowSurface.blit(BACKGROUND, (0, rel_x))

            # Enter in win mode
            if Score2 >= score_level2:
                timer2 += 1
                if timer2 < 750:
                    scroll2 += 1
                #Win mode 2
                pygame.mixer.music.stop()

                pygame.mouse.set_visible(False)

                drawText('LEVEL COMPLETE', windowSurface, (WINDOWHEIGHT / 2) + 50, (-250 + scroll2), RED, 48)
                windowSurface.blit(world, ((WINDOWHEIGHT / 2) + 30, -600 + scroll2))
                drawText('YOU DID IT !', windowSurface, (WINDOWHEIGHT / 2) + 100, (-700 + scroll2), RED, 48)
                b_special("Menu", (WINDOWHEIGHT / 2) + 125, -450 + scroll2, 150, 50, BLACK, GREY)

            # Add new baddies at the top of the screen, if needed.
            else:
                virusAddCounter += 1
                vaccinAddCounter += 5
                hospAddCounter += 2

            if virusAddCounter == virus.add_virus_rate:
                virusAddCounter = 0
                newVirus = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - virus.size), 0 - virus.size, virus.size,
                                                virus.size),
                            'speed': 5,
                            'surface': virus.surface,
                            }

                viruss.append(newVirus)

            if vaccinAddCounter == vaccine.add_vaccine_rate:
                vaccinAddCounter = 0
                newVaccin = {
                    'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - vaccine.size), 0 - vaccine.size, vaccine.size,
                                        vaccine.size),
                    'speed': 4,
                    'surface': vaccine.surface,
                }

                vaccines.append(newVaccin)

            if hospAddCounter == hospital.add_hosp_rate:
                hospAddCounter = 0
                newHosp = {
                    'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - hospital.rand_size), 0 - hospital.rand_size,
                                        hospital.rand_size, hospital.rand_size),
                    'speed': SPEED,
                    'surface': hospital.surface,
                }
                hospitals.append(newHosp)

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
            if Score2 < score_level2:
                drawText('Score: %s/4000' % (Score2), windowSurface, 10, 40, WHITE, 36)

            # Draw the lives
            if Score2 < score_level2:
                draw_lives(windowSurface, WINDOWWIDTH - 200, 5, bat.max_health, vies)

            # Check if any of the hospital have hit the player.
            if playerHasHitHospitals(bat.rect, hospitals):
                if Score2 < score_level2:
                    breakSound.play()
                    if bat.max_health == 0:
                        bat.max_health += 3
                    elif bat.max_health == 1:
                        bat.max_health += 2
                    elif bat.max_health == 2:
                        bat.max_health += 1
                    Score2 = 0
                    break

            # Check if any of the virus have hit the player.
            if playerHitVirus(bat.rect, viruss):
                if Score2 < score_level2:
                    Score2 += 100  # add 100 to the topScore
                    pickupSound.play()

            # Check if any of the vaccines have hit the player.
            if playerHitVaccine(bat.rect, vaccines):
                if Score2 < score_level2:
                    bat.max_health -= 1
                    failSound.play()
                    if Score2 >0:
                        Score2 -= 500  # subtract 500 to the topScore
                if bat.max_health == 0:
                    bat.max_health += 3
                    Score2 = 0
                    break

            pygame.display.update()

        # Stop the game and show the "Game Over" screen.
        show_GameOver_screen()


# Draw the button on the menu
pygame.display.update()
waitForPlayerToPressKey()

############# START ####################
Score = 0
Score2 = 0
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
    # game_state = GameState()

    menuSound.stop()
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.rewind()  # relancer directement la musique

    while True:  # The game loop runs while the game part is playing.
        game_state.main_game()

        # Background image settings
        if timer < 750:
            x += 1
        rel_x = x % BACKGROUND.get_rect().height
        windowSurface.blit(BACKGROUND, (0, rel_x - BACKGROUND.get_rect().height))
        if rel_x < WINDOWHEIGHT:
            windowSurface.blit(BACKGROUND, (0, rel_x))

        # Enter in win mode
        if Score >= score_level:
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
            newVirus = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - virus.size), 0 - virus.size, virus.size,
                                            virus.size),
                        'speed': SPEED,
                        'surface': virus.surface,
                        }

            viruss.append(newVirus)

        if vaccinAddCounter == vaccine.add_vaccine_rate:
            vaccinAddCounter = 0
            newVaccin = {
                'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - vaccine.size), 0 - vaccine.size, vaccine.size,
                                    vaccine.size),
                'speed': SPEED,
                'surface': vaccine.surface,
            }

            vaccines.append(newVaccin)

        if hospAddCounter == hospital.add_hosp_rate:
            hospAddCounter = 0
            newHosp = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - hospital.rand_size), 0 - hospital.rand_size,
                                           hospital.rand_size, hospital.rand_size),
                       'speed': SPEED,
                       'surface': hospital.surface,
                       }
            hospitals.append(newHosp)

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
        if Score < score_level:
            drawText('Score: %s/4000' % (Score), windowSurface, 10, 40, WHITE, 36)

        # Draw the lives
        if Score < score_level:
            draw_lives(windowSurface, WINDOWWIDTH - 200, 5, bat.max_health, vies)

        # Check if any of the hospital have hit the player.
        if playerHasHitHospitals(bat.rect, hospitals):
            if Score < score_level:
                breakSound.play()
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
            if Score < score_level:
                Score += 100  # add 100 to the topScore
                pickupSound.play()

        # Check if any of the vaccines have hit the player.
        if playerHitVaccine(bat.rect, vaccines):
            if Score < score_level:
                bat.max_health -= 1
                failSound.play()
                if Score > 0:
                    Score -= 500  # subtract 500 to the topScore
            if bat.max_health == 0:
                bat.max_health += 3
                Score = 0
                break

        pygame.display.update()

    # Stop the game and show the "Game Over" screen.
    show_GameOver_screen()
