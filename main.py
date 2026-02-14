'''
main is the entry point for the game that serves as the
    starting point for all of our other functions
'''

import pygame
import sys

from bodies import *
from vectorField import render
from windows import *
import constants

pygame.init()
clock = pygame.time.Clock()

current_state = constants.STATE_LANDING
running = True
gameStopped = False

screen_res = (constants.width, constants.height)
pygame.display.set_caption("Rocket Man!")
screen = pygame.display.set_mode(screen_res)

bodies = [
    Static_body(600, 600, 2e30, 16, (255,255,0)),
    Static_body(100, 100, 2e30, 16, (255,0,0)),
]

render(screen, bodies)



while running:
    clock.tick(constants.fps)

    events = pygame.event.get()
    mouse_pos = pygame.mouse.get_pos()
    
    for event in events:
        # Check events list for any state specific logic
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == constants.STATE_LANDING and start_button.collidepoint(event.pos):
                current_state = constants.STATE_TUT
            elif current_state == constants.STATE_TUT and okay_button.collidepoint(event.pos):
                current_state = constants.STATE_GAME
    
    # You could do an async physics sim or whatever here
    screen.fill((0, 0, 0))  # Clear screen

    if current_state == constants.STATE_LANDING:
        drawStartWindow(screen) # Includes the "Start" button
    elif current_state == constants.STATE_TUT:
        drawIntroWindow(screen)
    elif current_state == constants.STATE_GAME:
        render(screen, bodies)

    pygame.display.flip()   # Updates the screen

pygame.quit()
sys.exit()

