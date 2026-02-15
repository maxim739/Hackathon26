'''
main is the entry point for the game that serves as the
    starting point for all of our other functions
'''

import pygame
import sys
import math
import bodies
from bodies import *
from vectorField import render
import constants
from button import Button
import windows

pygame.init()
clock = pygame.time.Clock()

running = True
gameStopped = False
astromouse = False
astroMass = 5.972e30
mass_1 = 5.972e30
mass_2 = 6.972e30
mass_3 = 7.972e30
mass_4 = 8.972e30
mass_5 = 9.972e30

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
asteroid_button_rect = pygame.Rect(1050, 700, 200, 50)
mass_button_rects = [pygame.Rect(x, 700, 50, 50) for x in (775, 825, 875, 925, 975)]
start_button_rect = pygame.Rect(550, 700, 200, 50)


def click_is_on_ui(click_pos):
    if asteroid_button_rect.collidepoint(click_pos):
        return True
    for rect in mass_button_rects:
        if rect.collidepoint(click_pos):
            return True
    if not bodies.game_start and start_button_rect.collidepoint(click_pos):
        return True
    return False

def start_game():
    bodies.game_start = True


def restart_game():
    """Reset the game to its initial state"""
    global gameStopped, astromouse, asteroids_placed
    
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
        rocket.won = False
    
    # Clear any explosions
    explosion_group.empty()
    
    # Reset game state flags
    gameStopped = False
    astromouse = False
    asteroids_placed = 0
    bodies.game_start = False
    
    print("Game restarted!")



while running:
    print(asteroids_placed)
    clock.tick(constants.fps)
    mouse = pygame.mouse.get_pos()

    astro_scale = pygame.transform.scale(planets.astro_img, (45*(astroMass/mass_1), 45*(astroMass/mass_1)))

    asteroid = Static_body(
        mouse[0], 
        mouse[1], 
        astroMass, 
        12*(astroMass/mass_1), 
        (200, 150, 255), 
        astro_scale)

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

            if can_place and click_is_on_ui((mouse[0], mouse[1])):
                can_place = False

            
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

    button_text = f"Asteroids: ({asteroids_placed} / {constants.MAX_ASTEROIDS})"
    new_but = Button(button_text, 1050, 700, 200, 50, (50, 50, 50), (150, 150, 150))
    new_but.draw(screen)

    mass_text1 = f"1"
    mass_but1 = Button(mass_text1, 775, 700, 50, 50, (50, 50, 50), (150, 150, 150))
    mass_but1.draw(screen, selected=(astroMass == mass_1))

    mass_text2 = f"2"
    mass_but2 = Button(mass_text2, 825, 700, 50, 50, (50, 50, 50), (150, 150, 150))
    mass_but2.draw(screen, selected=(astroMass == mass_2))

    mass_text3 = f"3"
    mass_but3 = Button(mass_text3, 875, 700, 50, 50, (50, 50, 50), (150, 150, 150))
    mass_but3.draw(screen, selected=(astroMass == mass_3))

    mass_text4 = f"4"
    mass_but4 = Button(mass_text4, 925, 700, 50, 50, (50, 50, 50), (150, 150, 150))
    mass_but4.draw(screen, selected=(astroMass == mass_4))

    mass_text5 = f"5"
    mass_but5 = Button(mass_text5, 975, 700, 50, 50, (50, 50, 50), (150, 150, 150))
    mass_but5.draw(screen, selected=(astroMass == mass_5))

    if not bodies.game_start:
        start_but = Button("BLAST OFF", 550, 700, 200, 50, constants.startButton, (129, 0, 209))
        start_but.draw(screen)

    if event.type == pygame.MOUSEBUTTONDOWN and start_but.x < mouse[0] < start_but.x + start_but.width and start_but.y < mouse[1] < start_but.y + start_but.height:
        start_game()

    if event.type == pygame.MOUSEBUTTONDOWN and new_but.x < mouse[0] < new_but.x + new_but.width and new_but.y < mouse[1] < new_but.y + new_but.height:
        astromouse = True

    if event.type == pygame.MOUSEBUTTONDOWN and mass_but1.x < mouse[0] < mass_but1.x + mass_but1.width and mass_but1.y < mouse[1] < mass_but1.y + mass_but1.height:
        astroMass = mass_1

    if event.type == pygame.MOUSEBUTTONDOWN and mass_but2.x < mouse[0] < mass_but2.x + mass_but2.width and mass_but2.y < mouse[1] < mass_but2.y + mass_but2.height:
        astroMass = mass_2

    if event.type == pygame.MOUSEBUTTONDOWN and mass_but3.x < mouse[0] < mass_but3.x + mass_but3.width and mass_but3.y < mouse[1] < mass_but3.y + mass_but3.height:
        astroMass = mass_3

    if event.type == pygame.MOUSEBUTTONDOWN and mass_but4.x < mouse[0] < mass_but4.x + mass_but4.width and mass_but4.y < mouse[1] < mass_but4.y + mass_but4.height:
        astroMass = mass_4

    if event.type == pygame.MOUSEBUTTONDOWN and mass_but5.x < mouse[0] < mass_but5.x + mass_but5.width and mass_but5.y < mouse[1] < mass_but5.y + mass_but5.height:
        astroMass = mass_5

    if astromouse:
        asteroid.draw(screen, constants.width, constants.height)
    #print(astromouse)

    rocket = None

    #Draw all bodies and update position of moving body
    for body in planets.game_bodies:
        if isinstance(body, Moving_body):
            rocket = body
            if gameStopped == False and not body.dead and not body.won:
                body.update_position(planets.game_bodies)
        body.draw(screen, constants.width, constants.height)
    
    explosion_group.update()
    explosion_group.draw(screen)

    if rocket and rocket.won:
        windows.drawWinWindow(screen)


    pygame.display.flip()   # Updates the screen

pygame.quit()
sys.exit()

