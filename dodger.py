import pygame
import random
import sys
from pygame.locals import *

# Définir les variables pour les couleurs
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (127, 127, 127)

# Définir les variables pour la taille de l'écran
WINDOWWIDTH = 1000
WINDOWHEIGHT = 600

FPS = 60  # Nombre d'images par secondes

# Définition des scores à atteindre dans le jeu
score_level = 4000
score_level2 = 4000


# Définition des class pour les entités du jeu (Player, Hospital, Virus, Vaccine)
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


# Définition de la class pour le jeu (Menu, How to play et Game)
class GameState:
    def __init__(self):
        self.state = "main game"

    def intro(self):  # Définir la page menu
        menu()
        waitforplayertopresskey()

    def main_game(self):  # Définir la page de jeu
        pygame.mouse.set_visible(False)  # Rend le curseur de la souris invisible

        for event in pygame.event.get():  # Boucle for pour les actions du joueur
            if event.type == QUIT:
                # Si le joueur presse sur la croix rouge ,  quitter le jeu.
                terminate()

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    # Si le joueur presse le touche "Escape", il quitte le jeu.
                    terminate()

            if event.type == MOUSEMOTION:
                # Si la souris bouge, l'entité player bouge à l'endroit où se trouve le curseur.
                bat.rect.centerx = event.pos[0]
                bat.rect.centery = event.pos[1]

        # Bouge l'entité player pour qu'elle reste visible en entier si le curseur sort de la fenêtre de jeu
        if moveLeft and bat.rect.left > 0:
            bat.rect.move_ip(-1 * bat.player_move_rate, 0)
        if moveRight and bat.rect.right < WINDOWWIDTH:
            bat.rect.move_ip(bat.player_move_rate, 0)
        if moveUp and bat.rect.top > 0:
            bat.rect.move_ip(0, -1 * bat.player_move_rate)
        if moveDown and bat.rect.bottom < WINDOWHEIGHT:
            bat.rect.move_ip(0, bat.player_move_rate)

        # Fonction pour limiter le nombre de tick à 60 FPS ici (FPS = 60)
        mainClock.tick(FPS)

    def state_manager(self):  # Définition pour savoir quelle page lancer
        if self.state == "intro":
            self.intro()
        if self.state == "main_game":
            self.main_game()


# Définition de la class pour les buttons
class Button(GameState):
    def __init__(self, color_button, x_button, y_button, width, height, text=''):  # Paramètres du button
        super().__init__()
        self.color = color_button
        self.x = x_button
        self.y = y_button
        self.width = width
        self.height = height
        self.text = text

    def draw(self, window, outline):  # Définition de la fonction pour dessiner le bouton
        pygame.draw.rect(window, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

        #   Dessiner le texte dans le bouton
        font_button = pygame.font.SysFont('comicsans', 60)
        text = font_button.render(self.text, 1, WHITE)
        window.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isover(self, pos):  # Définition de la fonction pour retourner True quand le joueur presse sur le bouton
        # Pos est la position du curseur
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False


def terminate():  # Définition de la fonction pour fermer la fenêtre du jeu
    pygame.quit()
    sys.exit()


# Dessiner les boutons utilisés hors de la boucle du jeu
start_button = Button(BLACK, 348, 428, (WINDOWHEIGHT / 2) + 10, 70, "Start")
restart_button = Button(BLACK, 348, 428, (WINDOWHEIGHT / 2) + 10, 70, "Restart")
menu_button = Button(BLACK, 25, 25, 125, 50, "Menu")
option_button = Button(BLACK, 360, 515, (WINDOWHEIGHT / 2) - 15, 45, "How to play")
back_button = Button(BLACK, 25, 25, 125, 50, "Back")


# Définition de la fonction menu
def menu():
    menuSound.play()
    pygame.mouse.set_visible(True)
    menu_img = pygame.image.load("menu 1.jpg").convert()
    pic = pygame.transform.scale(menu_img, (WINDOWWIDTH, WINDOWHEIGHT))
    windowSurface.blit(pic, (0, 0))
    start_button.draw(windowSurface, WHITE)
    option_button.draw(windowSurface, WHITE)
    pygame.display.update()


# Définition de la fonction option ("How To Play")
def option():
    opt = pygame.image.load("Option.png").convert()
    opt_img = pygame.transform.scale(opt, (WINDOWWIDTH, WINDOWHEIGHT))
    windowSurface.blit(opt_img, (0, 0))
    back_button.draw(windowSurface, WHITE)
    pygame.display.update()


# Définition de la fonction pour toutes les actions qui nécessite qu'un bouton soit pressé
def waitforplayertopresskey():
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


# Définition de la fonction d'une collision entre le joueur et le virus
def playerhitvirus(player_v, vir):
    for v_hit in vir:
        if player_v.colliderect(v_hit['rect']):  # Détecter la collision
            vir.remove(v_hit)  # Supprimer le virus à chaque fois que le joueur le touche
            return True
    return False


# Définition de la fonction d'une collision entre le joueur et les hôpitaux
def playerhashithospitals(player_h, hospital_hit):
    for h_hit in hospital_hit:
        if player_h.colliderect(h_hit['rect']):  # Détecter la collision
            return True
    return False


# Définition de la fonction d'une collision entre le joueur et le vaccin
def playerhitvaccine(player_va, vacc):
    for va_hit in vacc:
        if player_va.colliderect(va_hit['rect']):  # Détecter la collision
            vacc.remove(va_hit)  # Supprimer le vaccin à chaque fois que le joueur le touche
            return True
    return False


# Définition de la fonction pour dessiner les zones de textes
def drawtext(text, surface, x_t, y_t, colour, size):
    font = pygame.font.SysFont(None, size)
    textobj = font.render(text, 1, colour)
    textrect = textobj.get_rect()
    textrect.topleft = (x_t, y_t)
    surface.blit(textobj, textrect)


# Variables pour définir les vies
img = pygame.image.load("vie.png")
vies = pygame.transform.scale(img, (130, 86))
vies.set_colorkey(BLACK)


# Définition pour dessiner les vies
def draw_lives(surf, x_l, y_l, max_health_l, img_l):
    for i in range(max_health_l):
        img_rect = img_l.get_rect()
        img_rect.x = x_l + 45 * i
        img_rect.y = y_l
        surf.blit(img_l, img_rect)


# Définition de la fonction texte pour le bouton spécial
def text_objects(text, font):
    textsurface = font.render(text, True, WHITE)
    return textsurface, textsurface.get_rect()


# Définition de la fonction du bouton spécial
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


# Définition de la fonction quand le joueur atteind le score final du niveau 1
def win_mode():
    pygame.mixer.music.stop()
    winSound.play()
    drawtext('LEVEL COMPLETE', windowSurface, (WINDOWHEIGHT / 2) + 50, (-150 + scroll), RED, 48)
    windowSurface.blit(level1Image, ((WINDOWHEIGHT / 2) + 125, -450 + scroll))
    drawtext('INFECT DONALD TRUMP !', windowSurface, (WINDOWHEIGHT / 2) - 10, (-600 + scroll), RED, 48)
    b_special("Level 2", (WINDOWHEIGHT / 2) + 125, -350 + scroll, 150, 50, BLACK, GREY)


# Définitioin de la fonction quand le joueur perd
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


# Configuration de pygame et de la fenêtre de jeu.
pygame.init()
mainClock = pygame.time.Clock()  # Variable pour avoir un suivi du temps quand on lance pygame.init()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Loco-vid')

# Définir les images de fond des 2 niveaux
BACKGROUND = pygame.image.load('fond.png').convert()  # fond du niveau 1
BACKGROUND_2 = pygame.image.load('fond_2.png').convert()  # fond du niveau 2

# Images utilisées entre les niveaux et à la fin du jeu
level1Image = pygame.image.load('Doni.png')
level1Image = pygame.transform.scale(level1Image, (133, 100))
world = pygame.image.load('covid_world.png')
world = pygame.transform.scale(world, (800, 400))
logo = pygame.image.load('logo_game.jpg')
logo = pygame.transform.scale(logo, (150, 150))

# Installer les sons du jeu
menuSound = pygame.mixer.Sound('Open.wav')
gameOverSound = pygame.mixer.Sound('Gover.wav')
finalSound = pygame.mixer.music.load('Final.wav')
winSound = pygame.mixer.Sound('Win.wav')
win2Sound = pygame.mixer.Sound('Win2.wav')
pickupSound = pygame.mixer.Sound('pickup.wav')
buttonSound = pygame.mixer.Sound('Button.wav')
failSound = pygame.mixer.Sound('Fail.wav')
breakSound = pygame.mixer.Sound('Break.wav')

# Configurer le volume pour chaque son
menuSound.set_volume(0.2)
gameOverSound.set_volume(0.5)
pygame.mixer.music.set_volume(0.1)
winSound.set_volume(0.1)
win2Sound.set_volume(0.07)
pickupSound.set_volume(0.2)
buttonSound.set_volume(0.1)
failSound.set_volume(100)
breakSound.set_volume(0.2)

# Lance le menu
game_state = GameState()
game_state.intro()


# Définition de la fonction pour le niveau 2
def level2():
    winSound.stop()

    while True:
        # Configurer les paramètres du niveau 2
        timer2 = 0
        timer_x2 = 0
        scroll2 = 0
        score2 = 0
        bat.max_health = 3
        hospitals_2 = []
        viruss_2 = []
        vaccines_2 = []
        virusaddcounter_2 = 0
        vaccinaddcounter_2 = 0
        hospaddcounter_2 = 0

        # Configurer la musique du niveau 2
        menuSound.stop()
        pygame.mixer.music.load('Level2.wav')
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.rewind()  # relancer directement la musique
        pygame.mixer.music.set_volume(0.05)

        while True:  # La boucle du jeu s'execute tant que le jeu n'est pas fini.
            game_state.main_game()

            # Configurer les paramètres du fond d'écran
            if timer2 < 1600:
                timer_x2 += 1
            rel_x2 = timer_x2 % BACKGROUND_2.get_rect().height
            windowSurface.blit(BACKGROUND_2, (0, rel_x2 - BACKGROUND_2.get_rect().height))
            if rel_x2 < WINDOWHEIGHT:
                windowSurface.blit(BACKGROUND_2, (0, rel_x2))

            # Entrer dans le win_mode
            if score2 >= score_level2:
                timer2 += 1
                if timer2 < 1600:
                    scroll2 += 1
                pygame.mixer.music.stop()
                if scroll2 == 500:
                    win2Sound.play()
                if scroll2 > 1010:
                    menuSound.play()
                if scroll2 > 1595:
                    b_special("Terminate", (WINDOWHEIGHT / 2) + 500, 500, 150, 50, BLACK, GREY)

                drawtext('LEVEL COMPLETE', windowSurface, (WINDOWHEIGHT / 2) + 50, (-150 + scroll2), RED, 48)
                windowSurface.blit(world, ((WINDOWHEIGHT / 2) - 200, - 550 + scroll2))
                drawtext('YOU DID IT !', windowSurface, (WINDOWHEIGHT / 2) + 100, (-600 + scroll2), RED, 48)

                # Dessiner les crédits à la fin du win_mode
                drawtext('Crédits', windowSurface, (WINDOWHEIGHT / 2) + 150, (-1550 + scroll2), WHITE, 42)
                drawtext('Loco-vid ALPHA 1.0', windowSurface, (WINDOWHEIGHT / 2) + 125, (-1500 + scroll2), WHITE, 26)
                windowSurface.blit(logo, ((WINDOWHEIGHT / 2) + 125, - 1430 + scroll2))
                drawtext('Copyright : GROUPE ONE', windowSurface, (WINDOWHEIGHT / 2) + 100, (-1230 + scroll2), WHITE,
                         26)
                drawtext('Staff', windowSurface, (WINDOWHEIGHT / 2) + 180, (-1180 + scroll2), WHITE, 32)
                drawtext('Tiffany Garcia', windowSurface, (WINDOWHEIGHT / 2) + 105, (-1140 + scroll2), WHITE, 20)
                drawtext('INGENIEURE SON', windowSurface, (WINDOWHEIGHT / 2) + 215, (-1140 + scroll2), WHITE, 20)
                drawtext('Daniel Do Vale Anes', windowSurface, (WINDOWHEIGHT / 2) + 65, (-1110 + scroll2), WHITE, 20)
                drawtext('INGENIEUR DESIGN', windowSurface, (WINDOWHEIGHT / 2) + 215, (-1110 + scroll2), WHITE, 20)
                drawtext('Erika da Silva', windowSurface, (WINDOWHEIGHT / 2) + 105, (-1080 + scroll2), WHITE, 20)
                drawtext('CREATIVE MIND', windowSurface, (WINDOWHEIGHT / 2) + 215, (-1080 + scroll2), WHITE, 20)
                drawtext('Bruno Samuel Da Silva Ferreira', windowSurface,
                         (WINDOWHEIGHT / 2) - 5, (-1050 + scroll2), WHITE, 20)
                drawtext('DEBUGER', windowSurface, (WINDOWHEIGHT / 2) + 215, (-1050 + scroll2), WHITE, 20)

            # Définir la quantité de nouveaux éléments qui apparaissent
            else:
                virusaddcounter_2 += 1
                vaccinaddcounter_2 += 5
                hospaddcounter_2 += 1

            # Si la quantité de nouveaux virus est égale au taux d'ajout de virus, on définit un nouveau virus
            if virusaddcounter_2 == virus.add_virus_rate:
                virusaddcounter_2 = 0
                newvirus_2 = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - virus.size), 0 - virus.size,
                                                  virus.size, virus.size),
                              'speed x': random.randrange(-3, 3, 1),
                              'speed': 6,
                              'surface': virus.surface_2,
                              }
                viruss_2.append(newvirus_2)

            # Si la quantité de nouveaux vaccins est égale au taux d'ajout de vaccins, on définit un nouveau vaccins
            if vaccinaddcounter_2 == vaccine.add_vaccine_rate:
                vaccinaddcounter_2 = 0
                newvaccin_2 = {
                    'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - vaccine.size), 0 - vaccine.size, vaccine.size,
                                        vaccine.size),
                    'speed': 4,
                    'surface': vaccine.surface_2,
                }
                vaccines_2.append(newvaccin_2)

            # Si la quantité de nouveaux hôpitaux est égale au taux d'ajout des hôpitaux, on définit un nouvel hôpital
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

            # Dessiner et bouger les virus
            for v_2 in viruss_2[:]:
                v_2['rect'].move_ip(v_2['speed x'], v_2['speed'])
                windowSurface.blit(v_2['surface'], v_2['rect'])
                if v_2['rect'].top > WINDOWHEIGHT:  # supprimer les virus qui sortent de la fenêtre
                    viruss_2.remove(v_2)

            # Dessiner et bouger les vaccins
            for va_2 in vaccines_2[:]:
                windowSurface.blit(va_2['surface'], va_2['rect'])

                # Les vaccins bougent en fonction de la position du joueur
                if bat.rect < va_2['rect']:     # Tous les virus qui sont à droite du joueur
                    va_2['rect'].move_ip(- 1, va_2['speed'])
                if bat.rect > va_2['rect']:     # Tous les vaccins qui sont à gauche du joueur
                    va_2['rect'].move_ip(1, va_2['speed'])

                if va_2['rect'].top > WINDOWHEIGHT:  # supprimer les vaccins qui sortent de la fenêtre
                    vaccines_2.remove(va_2)

            # Dessiner et bouger les hôpitaux
            for h_2 in hospitals_2[:]:
                h_2['rect'].move_ip(0, h_2['speed'])
                windowSurface.blit(h_2['surface'], h_2['rect'])
                if h_2['rect'].top > WINDOWHEIGHT:  # supprimer les hôpitaux qui sortent de la fenêtre
                    hospitals_2.remove(h_2)

            # Dessiner le joueur
            windowSurface.blit(bat.image, bat.rect)

            # Dessiner le score et les vies
            if score2 < score_level2:
                drawtext('Score: %s/4000' % score2, windowSurface, 10, 40, WHITE, 36)
                draw_lives(windowSurface, WINDOWWIDTH - 200, 5, bat.max_health, vies)

            # Contrôler si le joueur a touché un hôpital
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

            # Contrôler si le joueur a touché un virus
            if playerhitvirus(bat.rect, viruss_2):
                if score2 < score_level2:
                    score2 += 100  # ajouter 100 points au score
                    pickupSound.play()

            # Contrôler si le joueur a touché un vaccin
            if playerhitvaccine(bat.rect, vaccines_2):
                if score2 < score_level2:
                    bat.max_health -= 1
                    failSound.play()
                    if score2 > 500:
                        score2 -= 500  # enlever 500 points au score
                    if score2 <= 500:
                        score2 -= score2
                if bat.max_health == 0:
                    bat.max_health += 3
                    break

            pygame.display.update()  # mettre à jour la fenêtre

        # Terminer le jeu et montrer la fenêtre du "Game Over"
        show_gameover_screen()


# Configurer les paramètres du jeu avant de le lancer
scroll = 0
Score = 0
bat = Player(WINDOWWIDTH // 2, WINDOWHEIGHT - 50)
virus = Virus()
vaccine = Vaccine()
hospital = Hospital()

while True:
    # Configurer les paramètres du niveau 1
    timer = 0
    timer_x = 0
    hospitals = []
    viruss = []
    vaccines = []
    virusaddcounter = 0
    vaccinaddcounter = 0
    hospaddcounter = 0
    moveLeft = moveRight = moveUp = moveDown = True

    # Configurer la musique du niveau 1
    menuSound.stop()
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.rewind()  # relancer directement la musique

    while True:  # La boucle du jeu s'execute tant que le jeu n'est pas fini.
        game_state.main_game()

        # Background image settings
        if timer < 650:
            timer_x += 1
        rel_x = timer_x % BACKGROUND.get_rect().height
        windowSurface.blit(BACKGROUND, (0, rel_x - BACKGROUND.get_rect().height))
        if rel_x < WINDOWHEIGHT:
            windowSurface.blit(BACKGROUND, (0, rel_x))

        # Configurer les paramètres du fond d'écran
        if Score >= score_level:
            timer += 1
            if timer < 650:
                scroll += 1
            win_mode()
        # Définir la quantité de nouveaux éléments qui apparaissent
        else:
            virusaddcounter += 1
            vaccinaddcounter += 2
            hospaddcounter += 1

        # Si la quantité de nouveaux virus est égale au taux d'ajout de virus, on définit un nouveau virus
        if virusaddcounter == virus.add_virus_rate:
            virusaddcounter = 0
            newvirus = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - virus.size), 0 - virus.size, virus.size,
                                            virus.size),
                        'speed': 3,
                        'surface': virus.surface,
                        }
            viruss.append(newvirus)

        # Si la quantité de nouveaux vaccins est égale au taux d'ajout de vaccins, on définit un nouveau vaccins
        if vaccinaddcounter == vaccine.add_vaccine_rate:
            vaccinaddcounter = 0
            newvaccin = {
                'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - vaccine.size), 0 - vaccine.size, vaccine.size,
                                    vaccine.size),
                'speed': 3,
                'surface': vaccine.surface,
            }
            vaccines.append(newvaccin)

        # Si la quantité de nouveaux hôpitaux est égale au taux d'ajout de hôpitaux, on définit un nouveau hôpital
        if hospaddcounter == hospital.add_hosp_rate:
            hospaddcounter = 0
            newhosp = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - hospital.rand_size), 0 - hospital.rand_size,
                                           hospital.rand_size, hospital.rand_size),
                       'speed': 2,
                       'surface': hospital.surface,
                       }
            hospitals.append(newhosp)

        # Dessiner et bouger les virus
        for v in viruss:
            v['rect'].move_ip(0, v['speed'])
            windowSurface.blit(v['surface'], v['rect'])
            if v['rect'].top > WINDOWHEIGHT:    # supprimer les viruss qui sortent de la fenêtre
                viruss.remove(v)

        # Dessiner et bouger les vaccins
        for va in vaccines[:]:
            va['rect'].move_ip(0, va['speed'])
            windowSurface.blit(va['surface'], va['rect'])
            if va['rect'].top > WINDOWHEIGHT:   # supprimer les vaccins qui sortent de la fenêtre
                vaccines.remove(va)

        # Dessiner et bouger les hôpitaux
        for h in hospitals[:]:
            h['rect'].move_ip(0, h['speed'])
            windowSurface.blit(h['surface'], h['rect'])
            if h['rect'].top > WINDOWHEIGHT:    # supprimer les hôpitaux qui sortent de la fenêtre
                hospitals.remove(h)

        # Dessiner le joueur
        windowSurface.blit(bat.image, bat.rect)

        # Dessiner le score et les vies
        if Score < score_level:
            drawtext('Score: %s/4000' % Score, windowSurface, 10, 40, WHITE, 36)    # Dessine le score
            draw_lives(windowSurface, WINDOWWIDTH - 200, 5, bat.max_health, vies)   # Dessine les vies

        # Contrôler si le joueur a touché un hôpital
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

        # Contrôler si le joueur a touché un virus
        if playerhitvirus(bat.rect, viruss):
            if Score < score_level:
                Score += 100  # ajouter 100 points au score
                pickupSound.play()

        # Contrôler si le joueur a touché un vaccin
        if playerhitvaccine(bat.rect, vaccines):
            if Score < score_level:
                bat.max_health -= 1
                failSound.play()
                if Score > 500:
                    Score -= 500  # enlever 500 points au score
                if Score <= 500:
                    Score -= Score
            if bat.max_health == 0:
                bat.max_health += 3
                Score = 0
                break

        pygame.display.update()   # mettre à jour la fenêtre

    # Terminer le jeu et montrer la fenêtre du "Game Over"
    show_gameover_screen()
