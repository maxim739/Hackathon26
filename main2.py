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
from button import Button

pygame.init()
clock = pygame.time.Clock()

running = True
gameStopped = False
astromouse = False

screen_res = (constants.width, constants.height)
pygame.display.set_caption("Rocket Man!")
screen = pygame.display.set_mode(screen_res)

import planets

while running:
    clock.tick(constants.fps)
    mouse = pygame.mouse.get_pos()

    asteroid = Static_body(
        mouse[0], 
        mouse[1], 
        5.972e30, 
        12, 
        (200, 150, 255), 
        planets.planet1_img)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Place an asteroid where the mouse is
        if event.type == pygame.MOUSEBUTTONDOWN and astromouse == True:
            can_place = True
            
            #Cannot place an asteroid on top of another body
            for body in planets.game_bodies:
                body_screen_x = int(body.x * constants.scale + constants.width // 2)
                body_screen_y = int(body.y * constants.scale + constants.height // 2)
                if math.hypot(mouse[0] - body_screen_x, mouse[1] - body_screen_y) <= body.radius:
                    can_place = False
                    break

            if can_place:
                planets.astrioid_bodies.append(asteroid)
                astromouse = False

    
    # Render the screen
    screen.fill(constants.black)

    new_but = Button("New", 400, 400, 100, 100, (50, 50, 50), (150, 150, 150))
    new_but.draw(screen)
    
    if event.type == pygame.MOUSEBUTTONDOWN and new_but.x < mouse[0] < new_but.x + new_but.width and new_but.y < mouse[1] < new_but.y + new_but.height:
        astromouse = True

    if astromouse:
        asteroid.draw(screen, constants.width, constants.height)
    print(astromouse)


    #Draw all bodies and update position of moving body
    for body in planets.game_bodies:
        if isinstance(body, Moving_body) and gameStopped == False:
            body.update_position(planets.game_bodies)
        body.draw(screen, constants.width, constants.height)

    for asto in planets.astrioid_bodies:
        asto.draw(screen, constants.width, constants.height)

    print(planets.astrioid_bodies)
    pygame.display.flip()   # Updates the screen

pygame.quit()
sys.exit()

