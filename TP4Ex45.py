import statistics as s
student_and_grade = {"Martina": 5.35, "Bastien": 5.07, "Claire": 3.53, "Anna":
                    4.09, "Maria": 4.55, "Kim": 3.98,"Robin": 3.87, "Adriana": 5.20, "Kristina":
                    5.33, "Michael": 4.52, "Sophie": 4.54, "Sara": 4.94,"Olof": 4.61, "Tina": 5.74,
                    "Hanna": 4.42, "Mirsa": 5.55, "Sanna": 4.99, "Sally": 4.34,"Urban": 4.11,
                    "Kelly": 5.14, "Helmer": 4.53, "Joanna": 4.69, "Josephine": 4.00, "Vilma": 5.19,
                    "Martin": 5.35, "Bastiena": 5.07, "Klaire": 3.53, "Anne": 4.09, "Marie": 4.55,
                    "Kimi": 4.98,"Robina": 3.87, "Adrian": 5.20, "Kristian": 3.3, "Michaelle": 3.52,
                    "Sophia": 4.54, "Sarah": 4.94,"Olaf": 4.61, "Tino": 5.74, "Hanne": 4.42, "Mirso":
                    3.55, "Sannah": 4.99, "Sallie": 4.34,"Urbi": 4.11, "Kellian": 5.14, "Helmut": 4.53,
                    "Joan": 4.69, "Joseph": 4.00, "Vilmer": 5.19 }

grade_average = s.mean(student_and_grade.values())
students_above_avg = []
for name, grade in student_and_grade.items():
    if grade > grade_average:
        students_above_avg.append(grade)

print(grade_average)
print(len(students_above_avg))

print("test2.0")

#Show the "Menu" screen
def draw_text(text,font,color,surface,x,y):
    textobj = font.render(text,1,color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)

click = False
def main_menu():
    while True :
        windowSurface.fill((0,0,0))
        draw_text("Main menu",font,(255,255,255),windowSurface, 20,20)

        mx,my =pygame.mouse.get_pos()
        button1 = pygame.Rect(50,100,200,50)
        button2 = pygame.Rect(50, 200, 200, 50)
        if button1.collidepoint((mx,my)):
            if click:
                game()
        if button2.collidepoint((mx,my)):
            if click :
                options()
        pygame.draw.rect(windowSurface, (255,0,0), button1)
        pygame.draw.rect(windowSurface, (255,0,0),button2)

        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE :
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN :
                if event.button1 == 1:
                    click = True

            pygame.display.update()
            mainClock.tick(60)
main_menu()

def game():
    running = True
    while running :
        windowSurface.fill((0,0,0))
        draw_text("Game", font, (255, 255, 255), windowSurface, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE :
                    running = False

        pygame.display.update()
        mainClock.tick(60)

def options():
    running = True
    while running :
        windowSurface.fill((0, 0, 0))
        draw_text("Options", font, (255, 255, 255), windowSurface, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE :
                    running = False

        pygame.display.update()
        mainClock.tick(60)
