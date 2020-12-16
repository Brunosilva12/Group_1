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
scroll = 0
score_level = 300
score_level2 = 300


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
        self.rand_size = random.randint(self.min_size, self.max_size)
        self.surface = pygame.transform.scale(self.image, (self.rand_size, self.rand_size))
        self.image_2 = pygame.image.load('hosp_lvl2.png').convert_alpha()


class Virus(object):
    def __init__(self):
        self.size = 35
        self.add_virus_rate = 40
        self.image = pygame.image.load('virus.png').convert_alpha()
        self.surface = pygame.transform.scale(self.image, (self.size, self.size))
        self.image_2 = pygame.image.load('virus_2.png').convert_alpha()
        self.surface_2 = pygame.transform.scale(self.image_2, (self.size, self.size))


class Vaccine(object):
    def __init__(self):
        self.size = 35
        self.add_vaccine_rate = 50
        self.image = pygame.image.load('vaccin.png').convert_alpha()
        self.surface = pygame.transform.scale(self.image, (self.size, self.size))
        self.image_2 = pygame.image.load('vaccin_2.png').convert_alpha()
        self.surface_2 = pygame.transform.scale(self.image_2, (self.size, self.size))


class GameState:
    def __init__(self):
        self.state = "main game"

    def intro(self):
        menu()

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
            pygame.draw.rect(window, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4))

        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

        if self.text != '':
            font_button = pygame.font.SysFont('comicsans', 60)
            text = font_button.render(self.text, 1, WHITE)
            window.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isover(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
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
def menu():
    menuSound.play()
    pygame.mouse.set_visible(True)
    menu_img = pygame.image.load("menu 1.jpg").convert()
    pic = pygame.transform.scale(menu_img, (WINDOWWIDTH, WINDOWHEIGHT))
    windowSurface.blit(pic, (0, 0))
    start_button.draw(windowSurface, WHITE)
    option_button.draw(windowSurface, WHITE)

    pygame.display.update()


# Option
def option():
    opt = pygame.image.load("Option.png").convert()
    opt_img = pygame.transform.scale(opt, (WINDOWWIDTH, WINDOWHEIGHT))
    windowSurface.blit(opt_img, (0, 0))
    back_button.draw(windowSurface, WHITE)
    pygame.display.update()


def waitforplayertopresskey():  # Lancer le jeu ou le fermer
    while True:
        for event_Key in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event_Key.type == QUIT:
                terminate()
            if event_Key.type == KEYDOWN:
                if event_Key.key == K_ESCAPE:  # Pressing ESC quits.
                    terminate()
            if event_Key.type == pygame.MOUSEBUTTONDOWN:
                if start_button.isover(pos):
                    buttonSound.play()
                    return
            if event_Key.type == pygame.MOUSEBUTTONDOWN:
                if option_button.isover(pos):
                    buttonSound.play()
                    option()
            if event_Key.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isover(pos):
                    buttonSound.play()
                    menu()
            if event_Key.type == pygame.MOUSEBUTTONDOWN:
                if nxt_button.isover(pos):
                    buttonSound.play()
                    menu()


def playerhitvirus(player_v, vir):  # Définir la fonction : collision entre le player et le virus
    for v_hit in vir:
        if player_v.colliderect(v_hit['rect']):  # Détecter la collision
            vir.remove(v_hit)  # Supprimer le virus à chaque fois que le player le toucher
            return True
    return False


def playerhashithospitals(player_h, hospital_hit):  # Définir la fonction : collision entre le player et l'hôpital
    for h_hit in hospital_hit:
        if player_h.colliderect(h_hit['rect']):  # Détecter la collision
            return True
    return False


def playerhitvaccine(player_va, vacc):  # Définir la fonction : collision entre le player et le vaccin
    for va_hit in vacc:
        if player_va.colliderect(va_hit['rect']):  # Détecter la collision
            vacc.remove(va_hit)  # Supprimer le vaccin à chaque fois que le player le toucher
            return True
    return False


def drawtext(text, surface, x_t, y_t, colour, size):
    font = pygame.font.SysFont(None, size)
    textobj = font.render(text, 1, colour)
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
    textsurface = font.render(text, True, WHITE)
    return textsurface, textsurface.get_rect()


def b_special(msg, pos_x, pos_y, largeur, hauteur, ic, ac):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if pos_x + largeur > mouse[0] > pos_x and pos_y + hauteur > mouse[1] > pos_y:
        pygame.draw.rect(windowSurface, ac, (pos_x, pos_y, largeur, hauteur))
        if click[0] == 1:
            if msg == "Level 2":
                level2()
            if msg == "Terminate":
                terminate()
    else:
        pygame.draw.rect(windowSurface, ic, (pos_x, pos_y, largeur, hauteur))

    smalltext = pygame.font.Font("freesansbold.ttf", 20)
    textsurf, textrect = text_objects(msg, smalltext)
    textrect.center = ((pos_x + (largeur / 2)), (pos_y + (hauteur / 2)))
    windowSurface.blit(textsurf, textrect)


def win_mode():
    pygame.mixer.music.stop()
    winSound.play()
    pygame.mouse.set_visible(False)

    drawtext('LEVEL COMPLETE', windowSurface, (WINDOWHEIGHT / 2)+50, (-150 + scroll), RED, 48)
    windowSurface.blit(level1Image, ((WINDOWHEIGHT / 2)+125, -450 + scroll))
    drawtext('INFECT DONALD TRUMP !', windowSurface, (WINDOWHEIGHT / 2)-10, (-600 + scroll), RED, 48)
    b_special("Level 2", (WINDOWHEIGHT / 2)+125, -350 + scroll, 150, 50, BLACK, GREY)


def show_gameover_screen():
    pygame.mixer.music.stop()
    gameOverSound.play()
    pygame.mouse.set_visible(True)

    drawtext('GAME OVER', windowSurface, 290, (WINDOWHEIGHT / 2), BLACK, 100)
    restart_button.draw(windowSurface, WHITE)
    option_button.draw(windowSurface, WHITE)
    menu_button.draw(windowSurface, WHITE)
    pygame.display.update()
    waitforplayertopresskey()

    gameOverSound.stop()


# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Loco-vid')

# Background image
BACKGROUND = pygame.image.load('fond.png').convert()  # fond
BACKGROUND_2 = pygame.image.load('fond_2.png').convert()  # fond
timer_x = 0

# Set up sounds.
menuSound = pygame.mixer.Sound('Open.wav')
gameOverSound = pygame.mixer.Sound('Gover.wav')
finalSound = pygame.mixer.music.load('Final.wav')
winSound = pygame.mixer.Sound('Win.wav')
win2Sound = pygame.mixer.Sound('Win2.wav')
pickupSound = pygame.mixer.Sound('pickup.wav')
buttonSound = pygame.mixer.Sound('Button.wav')
failSound = pygame.mixer.Sound('Fail.wav')
breakSound = pygame.mixer.Sound('Break.wav')

# Set up the volume.
menuSound.set_volume(0.2)
gameOverSound.set_volume(0.5)
pygame.mixer.music.set_volume(0.1)
winSound.set_volume(0.1)
win2Sound.set_volume(0.07)
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
world = pygame.image.load('covid_world.png')
world = pygame.transform.scale(world, (800, 400))
logo = pygame.image.load('logo_game.jpg')
logo = pygame.transform.scale(logo, (150, 150))


def level2():
    winSound.stop()

    while True:
        # Set up the start of the game.
        timer2 = 0
        scroll2 = 0
        score2 = 0
        bat.max_health = 3
        timer_x2 = 0
        hospitals_2 = []
        viruss_2 = []
        vaccines_2 = []
        virusaddcounter_2 = 0
        vaccinaddcounter_2 = 0
        hospaddcounter_2 = 0

        pygame.mixer.music.load('Level2.wav')
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.rewind()  # relancer directement la musique
        pygame.mixer.music.set_volume(0.05)

        while True:  # The game loop runs while the game part is playing.
            game_state.main_game()

            # Background image settings
            if timer2 < 1600:
                timer_x2 += 1
            rel_x2 = timer_x2 % BACKGROUND_2.get_rect().height
            windowSurface.blit(BACKGROUND_2, (0, rel_x2 - BACKGROUND_2.get_rect().height))
            if rel_x2 < WINDOWHEIGHT:
                windowSurface.blit(BACKGROUND_2, (0, rel_x2))

            # Enter in win mode
            if score2 >= score_level2:
                timer2 += 1
                if timer2 < 1600:
                    scroll2 += 1
                # Win mode 2
                pygame.mixer.music.stop()
                if scroll2 == 500:
                    win2Sound.play()
                if scroll2 > 1010:
                    menuSound.play()
                if scroll2 > 1595:
                    b_special("Terminate", (WINDOWHEIGHT / 2) + 500, 500, 150, 50, BLACK, GREY)

                pygame.mouse.set_visible(False)
                drawtext('LEVEL COMPLETE', windowSurface, (WINDOWHEIGHT / 2) + 50, (-150 + scroll2), RED, 48)
                windowSurface.blit(world, ((WINDOWHEIGHT / 2) - 200, - 550 + scroll2))
                drawtext('YOU DID IT !', windowSurface, (WINDOWHEIGHT / 2) + 100, (-600 + scroll2), RED, 48)

                drawtext('Crédits', windowSurface, (WINDOWHEIGHT / 2) + 150, (-1550 + scroll2), WHITE, 42)
                drawtext('Loco-vid ALPHA 1.0', windowSurface, (WINDOWHEIGHT / 2) + 125, (-1500 + scroll2), WHITE, 26)
                windowSurface.blit(logo, ((WINDOWHEIGHT / 2) + 125, - 1430 + scroll2))
                drawtext('Copyright : GROUPE ONE', windowSurface, (WINDOWHEIGHT / 2) + 100, (-1230+scroll2), WHITE, 26)
                drawtext('Staff', windowSurface, (WINDOWHEIGHT / 2) + 180, (-1180 + scroll2), WHITE, 32)
                drawtext('Tiffany Garcia', windowSurface, (WINDOWHEIGHT / 2) + 105, (-1140 + scroll2), WHITE, 20)
                drawtext('INGENIEURE SON', windowSurface, (WINDOWHEIGHT / 2) + 215, (-1140 + scroll2), WHITE, 20)
                drawtext('Daniel Do Vale Anes', windowSurface, (WINDOWHEIGHT / 2) + 65, (-1110 + scroll2), WHITE, 20)
                drawtext('INGENIEUR DESIGN', windowSurface, (WINDOWHEIGHT / 2) + 215, (-1110 + scroll2), WHITE, 20)
                drawtext('Erika da Silva', windowSurface, (WINDOWHEIGHT / 2) + 105, (-1080 + scroll2), WHITE, 20)
                drawtext('CREATIVE MIND', windowSurface, (WINDOWHEIGHT / 2) + 215, (-1080 + scroll2), WHITE, 20)
                drawtext('Bruno Samuel Da Silva Ferreira', windowSurface,
                         (WINDOWHEIGHT/2)-5, (-1050+scroll2), WHITE, 20)
                drawtext('DEBUGER', windowSurface, (WINDOWHEIGHT / 2) + 215, (-1050 + scroll2), WHITE, 20)

            # Add new baddies at the top of the screen, if needed.
            else:
                virusaddcounter_2 += 1
                vaccinaddcounter_2 += 5
                hospaddcounter_2 += 1

            if virusaddcounter_2 == virus.add_virus_rate:
                virusaddcounter_2 = 0
                newvirus_2 = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - virus.size), 0 - virus.size,
                                                  virus.size, virus.size),
                              'speed x': random.randrange(-3, 3, 1),
                              'speed': 6,
                              'surface': virus.surface_2,
                              }
                viruss_2.append(newvirus_2)

            if vaccinaddcounter_2 == vaccine.add_vaccine_rate:
                vaccinaddcounter_2 = 0
                newvaccin_2 = {
                    'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - vaccine.size), 0 - vaccine.size, vaccine.size,
                                        vaccine.size),
                    'speed': 4,
                    'surface': vaccine.surface_2,
                }
                vaccines_2.append(newvaccin_2)

            if hospaddcounter_2 == hospital.add_hosp_rate:
                hospaddcounter_2 = 0
                hosp_rand_size = random.randint(hospital.min_size, hospital.max_size)
                newhosp_2 = {
                    'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - hosp_rand_size), 0 - hosp_rand_size,
                                        hosp_rand_size, hosp_rand_size),
                    'speed': 2,
                    'surface': pygame.transform.scale(hospital.image_2, (hosp_rand_size, hosp_rand_size)),
                }
                hospitals_2.append(newhosp_2)

            # Draw and move the virus. And delete the virus that have fallen past the bottom.
            for v_2 in viruss_2[:]:
                v_2['rect'].move_ip(v_2['speed x'], v_2['speed'])
                windowSurface.blit(v_2['surface'], v_2['rect'])
                if v_2['rect'].top > WINDOWHEIGHT:
                    viruss_2.remove(v_2)

            # Draw and move the vaccines. And delete vaccines that have fallen past the bottom.
            for va_2 in vaccines_2[:]:
                va_2['rect'].move_ip(0, va_2['speed'])
                windowSurface.blit(va_2['surface'], va_2['rect'])
                if va_2['rect'].top > WINDOWHEIGHT:
                    vaccines_2.remove(va_2)

            # Draw and move the hospitals. And delete hospitals that have fallen past the bottom.
            for h_2 in hospitals_2[:]:
                h_2['rect'].move_ip(0, h_2['speed'])
                windowSurface.blit(h_2['surface'], h_2['rect'])
                if h_2['rect'].top > WINDOWHEIGHT:
                    hospitals_2.remove(h_2)

            # Draw the player's rectangle.
            windowSurface.blit(bat.image, bat.rect)

            # Level 1
            if score2 < score_level2:
                drawtext('Score: %s/4000' % score2, windowSurface, 10, 40, WHITE, 36)

            # Draw the lives
            if score2 < score_level2:
                draw_lives(windowSurface, WINDOWWIDTH - 200, 5, bat.max_health, vies)

            # Check if any of the hospital have hit the player.
            if playerhashithospitals(bat.rect, hospitals_2):
                if score2 < score_level2:
                    breakSound.play()
                    if bat.max_health == 0:
                        bat.max_health += 3
                    elif bat.max_health == 1:
                        bat.max_health += 2
                    elif bat.max_health == 2:
                        bat.max_health += 1
                    break

            # Check if any of the virus have hit the player.
            if playerhitvirus(bat.rect, viruss_2):
                if score2 < score_level2:
                    score2 += 100  # add 100 to the topScore
                    pickupSound.play()

            # Check if any of the vaccines have hit the player.
            if playerhitvaccine(bat.rect, vaccines_2):
                if score2 < score_level2:
                    bat.max_health -= 1
                    failSound.play()
                    if score2 > 500:
                        score2 -= 500  # subtract 500 to the topScore
                    if score2 <= 500:
                        score2 -= score2
                if bat.max_health == 0:
                    bat.max_health += 3
                    break

            pygame.display.update()

        # Stop the game and show the "Game Over" screen.
        show_gameover_screen()


# Draw the button on the menu
pygame.display.update()
waitforplayertopresskey()
# START
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
    virusaddcounter = 0
    vaccinaddcounter = 0
    hospaddcounter = 0

    menuSound.stop()
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.rewind()  # relancer directement la musique

    while True:  # The game loop runs while the game part is playing.
        game_state.main_game()

        # Background image settings
        if timer < 650:
            timer_x += 1
        rel_x = timer_x % BACKGROUND.get_rect().height
        windowSurface.blit(BACKGROUND, (0, rel_x - BACKGROUND.get_rect().height))
        if rel_x < WINDOWHEIGHT:
            windowSurface.blit(BACKGROUND, (0, rel_x))

        # Enter in win mode
        if Score >= score_level:
            timer += 1
            if timer < 650:
                scroll += 1
            win_mode()
        # Add new baddies at the top of the screen, if needed.
        else:
            virusaddcounter += 1
            vaccinaddcounter += 2
            hospaddcounter += 1

        if virusaddcounter == virus.add_virus_rate:
            virusaddcounter = 0
            newvirus = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - virus.size), 0 - virus.size, virus.size,
                                            virus.size),
                        'speed': 3,
                        'surface': virus.surface,
                        }
            viruss.append(newvirus)

        if vaccinaddcounter == vaccine.add_vaccine_rate:
            vaccinaddcounter = 0
            newvaccin = {
                'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - vaccine.size), 0 - vaccine.size, vaccine.size,
                                    vaccine.size),
                'speed': 3,
                'surface': vaccine.surface,
            }
            vaccines.append(newvaccin)

        if hospaddcounter == hospital.add_hosp_rate:
            hospaddcounter = 0
            newhosp = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - hospital.rand_size), 0 - hospital.rand_size,
                                           hospital.rand_size, hospital.rand_size),
                       'speed': 2,
                       'surface': hospital.surface,
                       }
            hospitals.append(newhosp)

        # Draw and move the virus. And delete the virus that have fallen past the bottom.
        for v in viruss:
            v['rect'].move_ip(0, v['speed'])
            windowSurface.blit(v['surface'], v['rect'])
            if v['rect'].top > WINDOWHEIGHT:
                viruss.remove(v)

        # Draw and move the vaccines. And delete vaccines that have fallen past the bottom.
        for va in vaccines[:]:
            va['rect'].move_ip(0, va['speed'])
            windowSurface.blit(va['surface'], va['rect'])
            if va['rect'].top > WINDOWHEIGHT:
                vaccines.remove(va)

        # Draw and move the hospitals. And delete the hospitals that have fallen past the bottom.
        for h in hospitals[:]:
            h['rect'].move_ip(0, h['speed'])
            windowSurface.blit(h['surface'], h['rect'])
            if h['rect'].top > WINDOWHEIGHT:
                hospitals.remove(h)

        # Draw the player's rectangle.
        windowSurface.blit(bat.image, bat.rect)

        # Level 1
        if Score < score_level:
            drawtext('Score: %s/4000' % Score, windowSurface, 10, 40, WHITE, 36)

        # Draw the lives
        if Score < score_level:
            draw_lives(windowSurface, WINDOWWIDTH - 200, 5, bat.max_health, vies)

        # Check if any of the hospital have hit the player.
        if playerhashithospitals(bat.rect, hospitals):
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
        if playerhitvirus(bat.rect, viruss):
            if Score < score_level:
                Score += 100  # add 100 to the topScore
                pickupSound.play()

        # Check if any of the vaccines have hit the player.
        if playerhitvaccine(bat.rect, vaccines):
            if Score < score_level:
                bat.max_health -= 1
                failSound.play()
                if Score > 500:
                    Score -= 500  # subtract 500 to the topScore
                if Score <= 500:
                    Score -= Score
            if bat.max_health == 0:
                bat.max_health += 3
                Score = 0
                break

        pygame.display.update()

    # Stop the game and show the "Game Over" screen.
    show_gameover_screen()
