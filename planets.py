# loads all of the planets and lists starting positions
import pygame
from bodies import Static_body, Moving_body

def load_planet(path):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (100, 100))

planet1_img = load_planet("sprites/planet1.png")
planet2_img = load_planet("sprites/planet2.png")
planet3_img = load_planet("sprites/planet3.png")
planet4_img = load_planet("sprites/planet4.png")
planet5_img = load_planet("sprites/planet5.png")
planet6_img = load_planet("sprites/planet6.png")
planet7_img = load_planet("sprites/planet7.png")
planet8_img = load_planet("sprites/planet8.png")
goal_img    = load_planet("sprites/goalAura.png")

rocket_img = pygame.image.load("sprites/rocket.png").convert_alpha()
rocket_img = pygame.transform.scale(rocket_img, (20, 20))

astro_img = pygame.image.load("sprites/asteroid.png").convert_alpha()
astro_img = pygame.transform.scale(astro_img, (45, 45))

game_bodies = [
    Static_body(600, 600, 5e28, 25, (255,255,0), planet1_img),
    Static_body(200, 300, 2e30, 25, (255,0,0), planet2_img),
    Static_body(300, 300, 1e30, 25, (0,0,0), planet3_img),
    Static_body(400, 400, 8e21, 25, (0,0,0), planet4_img),
    Static_body(500, 500, 2e31, 25, (0,0,0), planet5_img),
    Static_body(200, 200, 8e28, 25, (0,0,0), goal_img, is_goal=True),
    Static_body(700, 500, 1e30, 25, (0,0,0), planet6_img),
    Static_body(800, 500, 1e30, 25, (0,0,0), planet7_img),
    Static_body(300, 500, 1e30, 25, (0,0,0), planet8_img),
    Moving_body(100, 100, 0, 0, 8.681e25, 4, (100, 200, 255), rocket_img)
]

astrioid_bodies = []
