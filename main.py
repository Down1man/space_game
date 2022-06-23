import pygame
import os
pygame.font.init()

#okno gry
WIDTH, HEIGHT = 750, 500
OKNO = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Taka gra")

#zmienne
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 60
SHIP_WIDTH, SHIP_HEIGHT = 60, 60
SHIP_MS = 5
LINIA = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
KULE_MS = 10
MAX_KUL = 3
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
FONT = pygame.font.SysFont("comicsans", 30)
ZWYCIEZCA_FONT = pygame.font.SysFont("comicsans", 80)

#statki
YELLOW_SHIP_IMAGE = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
RED_SHIP_IMAGE = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
YELLOW_SHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 90)
RED_SHIP = pygame.transform.rotate(pygame.transform.scale(RED_SHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 270)

#tlo
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))


def wypelnianie(yellow, red, kule_yellow, kule_red, yellow_zycia, red_zycia):
    OKNO.blit(BG, (0, 0))
    pygame.draw.rect(OKNO, WHITE, LINIA)
    RED_ZYCIA_TEXT = FONT.render("Zycia: " + str(red_zycia), True, WHITE)
    YELLOW_ZYCIA_TEXT = FONT.render("Zycia: " + str(yellow_zycia), True, WHITE)
    OKNO.blit(RED_ZYCIA_TEXT, (10, 10))
    OKNO.blit(YELLOW_ZYCIA_TEXT, (WIDTH-RED_ZYCIA_TEXT.get_width() - 10, 10))
    OKNO.blit(YELLOW_SHIP, (yellow.x, yellow.y))
    OKNO.blit(RED_SHIP, (red.x, red.y))

    for kule in kule_red:
        pygame.draw.rect(OKNO, RED, kule)

    for kule in kule_yellow:
        pygame.draw.rect(OKNO, GREEN, kule)

    pygame.display.update()

def zwyciezca(text):
    taki = ZWYCIEZCA_FONT.render(text, True, GREEN)
    OKNO.blit(taki, (WIDTH//2 - taki.get_width()/2, HEIGHT//2 - taki.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def movement_red(key_pressed, red):
    if key_pressed[pygame.K_a] and red.x - SHIP_MS > 0:
        red.x -= SHIP_MS
    if key_pressed[pygame.K_d] and red.x + SHIP_MS + SHIP_WIDTH - 10 < LINIA.x:
        red.x += SHIP_MS
    if key_pressed[pygame.K_w] and red.y - SHIP_MS > 0:
        red.y -= SHIP_MS
    if key_pressed[pygame.K_s] and red.y + SHIP_MS + SHIP_HEIGHT < HEIGHT:
        red.y += SHIP_MS


def movement_yellow(key_pressed, yellow):
    if key_pressed[pygame.K_LEFT] and yellow.x - SHIP_MS > LINIA.x:
        yellow.x -= SHIP_MS
    if key_pressed[pygame.K_RIGHT] and yellow.x + SHIP_MS + SHIP_WIDTH < WIDTH:
        yellow.x += SHIP_MS
    if key_pressed[pygame.K_UP] and yellow.y - SHIP_MS > 0:
        yellow.y -= SHIP_MS
    if key_pressed[pygame.K_DOWN] and yellow.y + SHIP_MS + SHIP_HEIGHT < HEIGHT:
        yellow.y += SHIP_MS

def fizyka(kule_yellow, kule_red, yellow, red):
    for kula in kule_red:
        kula.x += KULE_MS
        if yellow.colliderect(kula):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            kule_red.remove(kula)
        if kula.x > WIDTH:
            kule_red.remove(kula)

    for kula in kule_yellow:
        kula.x -= KULE_MS
        if red.colliderect(kula):
            pygame.event.post(pygame.event.Event(RED_HIT))
            kule_yellow.remove(kula)
        if kula.x < 0:
            kule_yellow.remove(kula)


def main():
    yellow = pygame.Rect(600, 100, SHIP_WIDTH, SHIP_HEIGHT)
    red = pygame.Rect(200, 100, SHIP_WIDTH, SHIP_HEIGHT)

    kule_red = []
    kule_yellow = []

    yellow_zycia = 5
    red_zycia = 5

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(kule_red) < MAX_KUL:
                    kula = pygame.Rect(red.x + red.width, red.y + red.height//2 - 2, 10, 5)
                    kule_red.append(kula)
                if event.key == pygame.K_RCTRL and len(kule_yellow) < MAX_KUL:
                    kula = pygame.Rect(yellow.x, yellow.y + yellow.height//2 + 2, 10, 5)
                    kule_yellow.append(kula)
            if event.type == RED_HIT:
                red_zycia -= 1
            if event.type == YELLOW_HIT:
                yellow_zycia -= 1

        winner = ""
        if red_zycia <= 0:
            winner = "Zielony wygrywa"
        if yellow_zycia <= 0:
            winner = "Czerwony wygrywa"
        if winner != "":
            zwyciezca(winner)
            break

        key_pressed = pygame.key.get_pressed()

        movement_red(key_pressed, red)
        movement_yellow(key_pressed, yellow)
        fizyka(kule_yellow, kule_red, yellow, red)
        wypelnianie(yellow, red, kule_yellow, kule_red, yellow_zycia, red_zycia)

    pygame.quit()


main()
