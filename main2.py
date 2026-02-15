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

initial_rocket_index = None
initial_rocket_state = None

asteroids_placed = 0

for i, body in enumerate(planets.game_bodies):
    if isinstance(body, Moving_body):
        initial_rocket_index = i
        initial_rocket_state = {
            'x': body.x,
            'y': body.y,
            'screen_x': body.screen_x,
            'screen_y': body.screen_y,
            'vx': body.vx,
            'vy': body.vy,
            'dead': False
        }
        break

initial_bodies_count = len(planets.game_bodies)

def restart_game():
    """Reset the game to its initial state"""
    global gameStopped, astromouse
    
    # Remove all asteroids (any bodies added after the initial count)
    planets.game_bodies = planets.game_bodies[:initial_bodies_count]
    
    # Reset the rocket to its initial state
    if initial_rocket_index is not None and initial_rocket_state is not None:
        rocket = planets.game_bodies[initial_rocket_index]
        rocket.x = initial_rocket_state['x']
        rocket.y = initial_rocket_state['y']
        rocket.screen_x = initial_rocket_state['screen_x']
        rocket.screen_y = initial_rocket_state['screen_y']
        rocket.vx = initial_rocket_state['vx']
        rocket.vy = initial_rocket_state['vy']
        rocket.dead = False
    
    # Clear any explosions
    explosion_group.empty()
    
    # Reset game state flags
    gameStopped = False
    astromouse = False
    asteroids_placed = 0
    
    print("Game restarted!")



while running:
    clock.tick(constants.fps)
    mouse = pygame.mouse.get_pos()

    asteroid = Static_body(
        mouse[0], 
        mouse[1], 
        5.972e30, 
        12, 
        (200, 150, 255), 
        planets.astro_img)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()

        #Place an asteroid where the mouse is
        if event.type == pygame.MOUSEBUTTONDOWN and astromouse == True:
            can_place = True

            if asteroids_placed >= constants.MAX_ASTEROIDS:
                can_place = False
                astromouse = False
                print('max astro')

            
            #Cannot place an asteroid on top of another body
            if can_place:
                for body in planets.game_bodies:
                    body_screen_x = int(body.x * constants.scale + constants.width // 2)
                    body_screen_y = int(body.y * constants.scale + constants.height // 2)
                    if math.hypot(mouse[0] - body_screen_x, mouse[1] - body_screen_y) <= body.radius:
                        can_place = False
                        break

            if can_place:
                planets.game_bodies.append(asteroid)
                asteroids_placed += 1
                astromouse = False

    
    # Render the screen
    screen.fill(constants.black)

    new_but = Button("New", 1150, 700, 100, 50, (50, 50, 50), (150, 150, 150))
    new_but.draw(screen)
    
    if event.type == pygame.MOUSEBUTTONDOWN and new_but.x < mouse[0] < new_but.x + new_but.width and new_but.y < mouse[1] < new_but.y + new_but.height:
        astromouse = True

    if astromouse:
        asteroid.draw(screen, constants.width, constants.height)
    print(astromouse)


    #Draw all bodies and update position of moving body
    for body in planets.game_bodies:
        if isinstance(body, Moving_body) and gameStopped == False and not body.dead:
            body.update_position(planets.game_bodies)
        body.draw(screen, constants.width, constants.height)
    
    explosion_group.update()
    explosion_group.draw(screen)

    pygame.display.flip()   # Updates the screen

pygame.quit()
sys.exit()

