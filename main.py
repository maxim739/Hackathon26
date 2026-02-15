'''
main is the entry point for the game that serves as the
    starting point for all of our other functions
'''

import pygame
import sys

import bodies
from bodies import *
from vectorField import renderSurface
import windows
from windows import *
import constants
from button import Button
from assets import load_assets, IMAGES

pygame.init()
clock = pygame.time.Clock()

current_state = constants.STATE_LANDING

running = True
gameStopped = False
astromouse = True
can_place = False

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
    can_place = True

    renderSurface(field_cache, planets.game_bodies)
    
    print("Game restarted!")

field_cache = pygame.Surface((constants.width, constants.height), pygame.SRCALPHA)
field_needs_update = True

renderSurface(field_cache, planets.game_bodies)

while running:
    clock.tick(constants.fps)

    events = pygame.event.get()
    mouse_pos = pygame.mouse.get_pos()

    astro_scale = pygame.transform.scale(planets.astro_img, (45*(astroMass/mass_1), 45*(astroMass/mass_1)))

    asteriod = Static_body(mouse_pos[0], mouse_pos[1], astroMass, 12*(astroMass/mass_1), (200, 150, 255), astro_scale)
    
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
                #screen.blit(field_cache, (0, 0))
                if astromouse:
                    can_place = True

                    if asteroids_placed >= constants.MAX_ASTEROIDS:
                        can_place = False

                    if start_but.x < mouse_pos[0] < start_but.x + start_but.width and start_but.y < mouse_pos[1] < start_but.y + start_but.height:
                        break

                    if new_but.x < mouse_pos[0] < new_but.x + new_but.width and new_but.y < mouse_pos[1] < new_but.y + new_but.height:
                        break

                    if mass_but1.x < mouse_pos[0] < mass_but1.x + mass_but1.width and mass_but1.y < mouse_pos[1] < mass_but1.y + mass_but1.height:
                        break

                    if mass_but2.x < mouse_pos[0] < mass_but2.x + mass_but2.width and mass_but2.y < mouse_pos[1] < mass_but2.y + mass_but2.height:
                        break

                    if mass_but3.x < mouse_pos[0] < mass_but3.x + mass_but3.width and mass_but3.y < mouse_pos[1] < mass_but3.y + mass_but3.height:
                        break

                    if mass_but4.x < mouse_pos[0] < mass_but4.x + mass_but4.width and mass_but4.y < mouse_pos[1] < mass_but4.y + mass_but4.height:
                        break

                    if mass_but5.x < mouse_pos[0] < mass_but5.x + mass_but5.width and mass_but5.y < mouse_pos[1] < mass_but5.y + mass_but5.height:
                        break

                    if can_place:
                        for body in planets.game_bodies:
                            body_screen_x = int(body.x * constants.scale + constants.width // 2)
                            body_screen_y = int(body.y * constants.scale + constants.height // 2)
                            if math.hypot(mouse_pos[0] - body_screen_x, mouse_pos[1] - body_screen_y) <= body.radius:
                                can_place = False
                                break

                    if can_place:
                        planets.game_bodies.append(asteriod)
                        renderSurface(field_cache, planets.game_bodies)
                        asteroids_placed += 1
    
    # You could do an async physics sim or whatever here
    screen.fill((0, 0, 0))  # Clear screen

    mass_text1 = f"1"
    mass_but1 = Button(mass_text1, 775, 700, 50, 50, (50, 50, 50), (150, 150, 150))
    

    mass_text2 = f"2"
    mass_but2 = Button(mass_text2, 825, 700, 50, 50, (50, 50, 50), (150, 150, 150))
    

    mass_text3 = f"3"
    mass_but3 = Button(mass_text3, 875, 700, 50, 50, (50, 50, 50), (150, 150, 150))
    

    mass_text4 = f"4"
    mass_but4 = Button(mass_text4, 925, 700, 50, 50, (50, 50, 50), (150, 150, 150))
    

    mass_text5 = f"5"
    mass_but5 = Button(mass_text5, 975, 700, 50, 50, (50, 50, 50), (150, 150, 150))
    


    if current_state == constants.STATE_LANDING:
        drawStartWindow(screen) # Includes the "Start" button
    elif current_state == constants.STATE_TUT:
        drawIntroWindow(screen)
    elif current_state == constants.STATE_GAME:
        screen.blit(field_cache, (0, 0))
        button_text = f"Asteroids: ({asteroids_placed} / {constants.MAX_ASTEROIDS})"
        new_but = Button(button_text, 1050, 700, 200, 50, (50, 50, 50), (150, 150, 150))
        new_but.draw(screen)

        mass_but1.draw(screen, selected=(astroMass == mass_1))
        mass_but2.draw(screen, selected=(astroMass == mass_2))
        mass_but3.draw(screen, selected=(astroMass == mass_3))
        mass_but4.draw(screen, selected=(astroMass == mass_4))
        mass_but5.draw(screen, selected=(astroMass == mass_5))

        if not bodies.game_start:
            start_but = Button("BLAST OFF", 550, 700, 200, 50, constants.startButton, (129, 0, 209))
            start_but.draw(screen)

        if event.type == pygame.MOUSEBUTTONDOWN and start_but.x < mouse_pos[0] < start_but.x + start_but.width and start_but.y < mouse_pos[1] < start_but.y + start_but.height:
            start_game()

        if event.type == pygame.MOUSEBUTTONDOWN and new_but.x < mouse_pos[0] < new_but.x + new_but.width and new_but.y < mouse_pos[1] < new_but.y + new_but.height:
            astromouse = True

        if event.type == pygame.MOUSEBUTTONDOWN and mass_but1.x < mouse_pos[0] < mass_but1.x + mass_but1.width and mass_but1.y < mouse_pos[1] < mass_but1.y + mass_but1.height:
            astroMass = mass_1

        if event.type == pygame.MOUSEBUTTONDOWN and mass_but2.x < mouse_pos[0] < mass_but2.x + mass_but2.width and mass_but2.y < mouse_pos[1] < mass_but2.y + mass_but2.height:
            astroMass = mass_2

        if event.type == pygame.MOUSEBUTTONDOWN and mass_but3.x < mouse_pos[0] < mass_but3.x + mass_but3.width and mass_but3.y < mouse_pos[1] < mass_but3.y + mass_but3.height:
            astroMass = mass_3

        if event.type == pygame.MOUSEBUTTONDOWN and mass_but4.x < mouse_pos[0] < mass_but4.x + mass_but4.width and mass_but4.y < mouse_pos[1] < mass_but4.y + mass_but4.height:
            astroMass = mass_4

        if event.type == pygame.MOUSEBUTTONDOWN and mass_but5.x < mouse_pos[0] < mass_but5.x + mass_but5.width and mass_but5.y < mouse_pos[1] < mass_but5.y + mass_but5.height:
            astroMass = mass_5

        if astromouse:
            asteriod.draw(screen, constants.width, constants.height)

        rocket = None

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