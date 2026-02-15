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
from assets import load_assets, IMAGES

pygame.init()
clock = pygame.time.Clock()

current_state = constants.STATE_LANDING
running = True
gameStopped = False
place_ast = False
launched = False

screen_res = (constants.width, constants.height)
pygame.display.set_caption("Rocket Man!")
screen = pygame.display.set_mode(screen_res)

import planets

load_assets()

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
    
    # Clear any explosions
    explosion_group.empty()
    
    # Reset game state flags
    gameStopped = False
    astromouse = False
    asteroids_placed = 0
    
    print("Game restarted!")


while running:
    clock.tick(constants.fps)

    events = pygame.event.get()
    mouse_pos = pygame.mouse.get_pos()

    asteriod = Static_body(mouse_pos[0], mouse_pos[1], 5.972e30, 12, (200, 150, 255), planets.astro_img)
    
    for event in events:
        # Check events list for any state specific logic
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and constants.STATE_GAME:
                restart_game()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == constants.STATE_LANDING and start_button.collidepoint(event.pos):
                current_state = constants.STATE_TUT
            elif current_state == constants.STATE_TUT and okay_button.collidepoint(event.pos):
                current_state = constants.STATE_GAME
            elif current_state == constants.STATE_GAME:
                if launch_button.collidepoint(event.pos):
                    launched = True
                elif place_ast and asteroids_placed < constants.MAX_ASTEROIDS:
                    # We are allowed by the game to place an asteriod
                    for body in planets.game_bodies:    # We make sure we aren't in a planet
                        body_screen_x = int(body.x * constants.scale + constants.width // 2)
                        body_screen_y = int(body.y * constants.scale + constants.height // 2)
                        if math.hypot(mouse_pos[0] - body_screen_x, mouse_pos[1] - body_screen_y) <= body.radius:
                            can_place = False
                            break
                    
                    # We are able to place the asteroid here
                    planets.game_bodies.append(asteriod)
                    asteroids_placed += 1
                    astromouse = False
    
    # You could do an async physics sim or whatever here
    screen.fill((0, 0, 0))  # Clear screen

    if current_state == constants.STATE_LANDING:
        drawStartWindow(screen) # Includes the "Start" button
    elif current_state == constants.STATE_TUT:
        drawIntroWindow(screen)
    elif current_state == constants.STATE_GAME:
        #render(screen, planets.game_bodies)
        # jk
        place_ast = True

        if launched == False:
            render(screen, planets.game_bodies)

        place_ast = True

        drawGameWindow(screen)

        asteriod_text = f"Asteriods ({asteroids_placed} / {constants.MAX_ASTEROIDS})"
        text_surf = buttonFont.render(asteriod_text, True, (255, 255, 255))
        screen.blit(text_surf, (constants.width/8, constants.height*7/8))

        

        for body in planets.game_bodies:
            if isinstance(body, Moving_body) and gameStopped == False and not body.dead:
                body.update_position(planets.game_bodies)
            body.draw(screen, constants.width, constants.height)
        
        explosion_group.update()
        explosion_group.draw(screen)



    pygame.display.flip()   # Updates the screen

pygame.quit()
sys.exit()

