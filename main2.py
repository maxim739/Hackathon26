'''
main is the entry point for the game that serves as the
    starting point for all of our other functions
'''


import pygame
import sys

from bodies import *
from vectorField import render
import constants

pygame.init()
clock = pygame.time.Clock()

running = True
gameStopped = False

screen_res = (constants.width, constants.height)
pygame.display.set_caption("Rocket Man!")
screen = pygame.display.set_mode(screen_res)

bodies = [
    Static_body(0, 0, 1.989e30, 16, (255, 255, 0)),
    Static_body(2e12, 0, 2e30, 16, (255,0,0)),
    Moving_body(1e12, 0, 0, 30000, 5.972e24, 8, (0, 0, 255)),
]

render(screen, bodies)

while running:
    clock.tick(constants.fps)
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            bodies.append(Static_body((mouse[0]/constants.scale)-constants.width/constants.scale/2, mouse[1]/constants.scale-constants.height/constants.scale/2, 5.972e24, 12, (200, 150, 255)))

    
    # Render the screen
    for body in bodies:
        if isinstance(body, Moving_body) and gameStopped == False:
            body.update_position(bodies)
        body.draw(screen, constants.width, constants.height)

    pygame.display.flip()   # Updates the screen

pygame.quit()
sys.exit()

