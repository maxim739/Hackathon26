'''
main is the entry point for the game that serves as the
    starting point for all of our other functions
'''


import pygame
import sys

import constants

pygame.init()
running = True
clock = pygame.time.Clock()

screen_res = (constants.width, constants.height)
pygame.display.set_caption("Rocket Man!")
screen = pygame.display.set_mode(screen_res)

while running:
    clock.tick(constants.fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    pygame.display.flip()   # Updates the screen

pygame.quit()
sys.exit()

