import pygame

from arrow import draw_arrow

pygame.init()

CLOCK = pygame.time.Clock()
FPS = 60

WIDTH = 1280
HEIGHT = 720
RESOLUTION = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(RESOLUTION)

while True:
    CLOCK.tick(FPS)

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    SCREEN.fill(pygame.Color("black"))

    center = pygame.Vector2(500, 500)
    draw_arrow(SCREEN, center, 0, pygame.Color("dodgerblue"), 10)

    pygame.display.flip()
