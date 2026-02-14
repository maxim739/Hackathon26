'''
main is the entry point for the game that serves as the
    starting point for all of our other functions
'''


import pygame
import sys
import math
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

#list of bodies in the game, can be static or moving. Static bodies are like planets and placeable asteroids and moving body is the player
bodies = [
    #Static_body(0, 0, 1.989e30, 16, (255, 255, 0)),
    Static_body(650, 400, 1e31, 16, (255,0,0)),
    Moving_body(750, 400, 0, 20000, 5.972e24, 8, (0, 0, 255)),
]

while running:
    clock.tick(constants.fps)
    mouse = pygame.mouse.get_pos()

    asteroid = Static_body(mouse[0], mouse[1], 5.972e30, 12, (200, 150, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Place an asteroid where the mouse is
        if event.type == pygame.MOUSEBUTTONDOWN:
            can_place = True
            
            #Cannot place an asteroid on top of another body
            for body in bodies:
                body_screen_x = int(body.x * constants.scale + constants.width // 2)
                body_screen_y = int(body.y * constants.scale + constants.height // 2)
                if math.hypot(mouse[0] - body_screen_x, mouse[1] - body_screen_y) <= body.radius:
                    can_place = False
                    break

            if can_place:
                bodies.append(asteroid)

    
    # Render the screen
    screen.fill(constants.black)
    asteroid.draw(screen, constants.width, constants.height)

    #Draw all bodies and update position of moving body
    for body in bodies:
        if isinstance(body, Moving_body) and gameStopped == False:
            body.update_position(bodies)
        body.draw(screen, constants.width, constants.height)

    pygame.display.flip()   # Updates the screen

pygame.quit()
sys.exit()

