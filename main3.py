'''
main is the entry point for the game that serves as the
    starting point for all of our other functions
'''


import pygame
import sys

from bodies import *
from vectorField import *
import constants

pygame.init()
clock = pygame.time.Clock()

running = True
gameStopped = False

screen_res = (constants.width, constants.height)
pygame.display.set_caption("Rocket Man!")
screen = pygame.display.set_mode(screen_res)

bodies = [
    Static_body(600, 600, 2e30, 16, constants.blue),
    Static_body(100, 100, 2e30, 16, constants.red),
    Static_body(600, 100, 4e30, 16, constants.blue),
    Static_body(100, 600, 4e30, 16, constants.red),
]

render(screen, bodies)

while running:
    clock.tick(constants.fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Render the screen
    for body in bodies:
        if isinstance(body, Moving_body) and gameStopped == False:
            body.update_position(body)
        body.draw(screen, constants.width, constants.height)

    
    pygame.display.flip()   # Updates the screen

pygame.quit()
sys.exit()

