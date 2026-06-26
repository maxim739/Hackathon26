'''
main is the entry point for the game that serves as the
    starting point for all of our other functions
'''

import pygame
import sys
import math
import os

def _asset(path):
    """Resolve asset path — works both in dev and inside a PyInstaller bundle."""
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, path)

from logic import bodies
from logic import constants
from logic.bodies import Static_body, Moving_body, explosion_group
from logic.map_loader import list_maps, load_map
from display import vector_field
from display import windows
from display import button
from display import assets
from display.button import Button
from display.assets import load_assets, IMAGES
from display.windows import drawStartWindow, drawIntroWindow, drawWinWindow
from display.windows import start_button, okay_button

pygame.init()
clock = pygame.time.Clock()

current_state = constants.STATE_LANDING

running = True
gameStopped = False
astromouse = True
can_place = False
speed_doubled = False
just_reset = False

astroMass = 5.972e30
mass_1 = 5.972e30
mass_2 = 6.972e30
mass_3 = 7.972e30
mass_4 = 8.972e30
mass_5 = 9.972e30

screen_res = (constants.width, constants.height)
pygame.display.set_caption("Rocket Man!")
screen = pygame.display.set_mode(screen_res)

load_assets()

available_maps = list_maps()
selected_map_index = 0
selected_map_data = load_map(available_maps[selected_map_index]) if available_maps else None

def _load_planet(path):
    img = pygame.image.load(_asset(path)).convert_alpha()
    return pygame.transform.scale(img, (140, 140))

planet1_img = _load_planet("assets/sprites/planets/planet1.png")
planet2_img = _load_planet("assets/sprites/planets/planet2.png")
planet3_img = _load_planet("assets/sprites/planets/planet3.png")
planet4_img = _load_planet("assets/sprites/planets/planet4.png")
planet5_img = _load_planet("assets/sprites/planets/planet5.png")
planet6_img = _load_planet("assets/sprites/planets/planet6.png")
planet7_img = _load_planet("assets/sprites/planets/planet7.png")
planet8_img = _load_planet("assets/sprites/planets/planet8.png")
goal_img    = _load_planet("assets/sprites/goalAura.png")

rocket_img = pygame.image.load(_asset("assets/sprites/rocket.png")).convert_alpha()
rocket_img = pygame.transform.scale(rocket_img, (20, 20))

astro_img = pygame.image.load(_asset("assets/sprites/asteroid.png")).convert_alpha()
astro_img = pygame.transform.scale(astro_img, (45, 45))

def build_bodies_from_map(map_data):
    result = []
    for b in map_data['bodies']:
        sprite_key = b['sprite']
        if sprite_key in ('goalAura', 'goal'):
            img = _load_planet('assets/sprites/goalAura.png')
        else:
            img = _load_planet(f'assets/sprites/planets/{sprite_key}.png')
        radius_px = constants.SPRITE_RADII.get(sprite_key, 65)
        result.append(Static_body(
            b['x'], b['y'], b['mass'], radius_px,
            (0, 0, 0), img,
            is_goal=b.get('is_goal', False),
        ))
    r = map_data['rocket']
    rocket_img_local = pygame.image.load(_asset('assets/sprites/rocket.png')).convert_alpha()
    rocket_img_local = pygame.transform.scale(rocket_img_local, (20, 20))
    result.append(Moving_body(r['x'], r['y'], r['vx'], r['vy'], r['mass'], constants.SPRITE_RADII['rocket'], (100, 200, 255), rocket_img_local))
    return result

game_bodies = build_bodies_from_map(selected_map_data) if selected_map_data else []

initial_rocket_index = None
initial_rocket_state = None
asteroids_placed = 0

for i, body in enumerate(game_bodies):
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

initial_bodies_count = len(game_bodies)
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
    global gameStopped, astromouse, asteroids_placed, game_bodies, speed_doubled
    global initial_rocket_index, initial_rocket_state, initial_bodies_count

    # Rebuild bodies from the current map
    game_bodies = build_bodies_from_map(selected_map_data) if selected_map_data else game_bodies[:initial_bodies_count]

    initial_rocket_index = None
    initial_rocket_state = None
    for i, body in enumerate(game_bodies):
        if isinstance(body, Moving_body):
            initial_rocket_index = i
            initial_rocket_state = {'x': body.x, 'y': body.y, 'screen_x': body.screen_x, 'screen_y': body.screen_y, 'vx': body.vx, 'vy': body.vy, 'dead': False}
            break
    initial_bodies_count = len(game_bodies)

    # Reset the rocket to its initial state
    if initial_rocket_index is not None and initial_rocket_state is not None:
        rocket = game_bodies[initial_rocket_index]
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
    speed_doubled = False

    vector_field.renderSurface(field_cache, game_bodies)

    print("Game restarted!")

field_cache = pygame.Surface((constants.width, constants.height), pygame.SRCALPHA)
field_needs_update = True

vector_field.renderSurface(field_cache, game_bodies)

while running:
    clock.tick(constants.fps)

    just_reset = False
    events = pygame.event.get()
    event = pygame.event.Event(pygame.NOEVENT)
    mouse_pos = pygame.mouse.get_pos()

    astro_scale = pygame.transform.scale(astro_img, (45*(astroMass/mass_1), 45*(astroMass/mass_1)))

    asteriod = Static_body(mouse_pos[0], mouse_pos[1], astroMass, constants.SPRITE_RADII['asteroid'], (200, 150, 255), astro_scale)

    for event in events:
        # Check events list for any state specific logic
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and constants.STATE_GAME:
                restart_game()
            if current_state == constants.STATE_TUT and event.key == pygame.K_LEFT:
                selected_map_index = (selected_map_index - 1) % len(available_maps)
                selected_map_data = load_map(available_maps[selected_map_index])
            if current_state == constants.STATE_TUT and event.key == pygame.K_RIGHT:
                selected_map_index = (selected_map_index + 1) % len(available_maps)
                selected_map_data = load_map(available_maps[selected_map_index])

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
                        for body in game_bodies:
                            body_screen_x = int(body.x * constants.scale + constants.width // 2)
                            body_screen_y = int(body.y * constants.scale + constants.height // 2)
                            if math.hypot(mouse_pos[0] - body_screen_x, mouse_pos[1] - body_screen_y) <= body.radius:
                                can_place = False
                                break

                    if can_place:
                        game_bodies.append(asteriod)
                        vector_field.renderSurface(field_cache, game_bodies)
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
        if available_maps:
            map_font = pygame.font.Font(_asset('assets/fonts/PixelPurl.ttf'), 24)
            map_name = available_maps[selected_map_index]
            map_text = map_font.render(f'< Map: {map_name} >', True, (200, 200, 255))
            screen.blit(map_text, map_text.get_rect(center=(constants.width // 2, constants.height - 80)))
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

        rocket_dead = any(isinstance(b, Moving_body) and b.dead for b in game_bodies)

        if rocket_dead:
            reset_but = Button("RESET", 550, 700, 200, 50, (150, 30, 30), (220, 60, 60))
            reset_but.draw(screen)
            if event.type == pygame.MOUSEBUTTONDOWN and reset_but.x < mouse_pos[0] < reset_but.x + reset_but.width and reset_but.y < mouse_pos[1] < reset_but.y + reset_but.height:
                restart_game()
                just_reset = True
        elif not bodies.game_start:
            start_but = Button("BLAST OFF", 550, 700, 200, 50, constants.startButton, (129, 0, 209))
            start_but.draw(screen)
            if not just_reset and event.type == pygame.MOUSEBUTTONDOWN and start_but.x < mouse_pos[0] < start_but.x + start_but.width and start_but.y < mouse_pos[1] < start_but.y + start_but.height:
                start_game()
        else:
            boost_color = (60, 60, 60) if speed_doubled else (200, 100, 0)
            boost_label = "2x SPEED" if not speed_doubled else "BOOSTED"
            boost_but = Button(boost_label, 550, 700, 200, 50, boost_color, (255, 140, 0))
            boost_but.draw(screen)
            if event.type == pygame.MOUSEBUTTONDOWN and not speed_doubled:
                if boost_but.x < mouse_pos[0] < boost_but.x + boost_but.width and boost_but.y < mouse_pos[1] < boost_but.y + boost_but.height:
                    for body in game_bodies:
                        if isinstance(body, Moving_body) and not body.dead and not body.won:
                            body.vx *= 2
                            body.vy *= 2
                    speed_doubled = True

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

        for body in game_bodies:
            if isinstance(body, Moving_body):
                rocket = body
                if gameStopped == False and not body.dead and not body.won:
                    body.update_position(game_bodies)
            body.draw(screen, constants.width, constants.height)

        explosion_group.update()
        explosion_group.draw(screen)

        if rocket and rocket.won:
            windows.drawWinWindow(screen)

    pygame.display.flip()   # Updates the screen

pygame.quit()
sys.exit()
