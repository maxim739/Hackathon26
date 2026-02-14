# loads all of the planets and lists starting positions
import pygame
import bodies
import constants

planet1_img = pygame.image.load("sprites/planet1.png").convert_alpha()
planet1_img = pygame.transform.scale(planet1_img, (100, 100))

planet2_img = pygame.image.load("sprites/planet2.png").convert_alpha()
planet2_img = pygame.transform.scale(planet2_img, (100, 100))

planet3_img = pygame.image.load("sprites/planet3.png").convert_alpha()
planet3_img = pygame.transform.scale(planet3_img, (100, 100))

planet4_img = pygame.image.load("sprites/planet4.png").convert_alpha()
planet4_img = pygame.transform.scale(planet4_img, (100, 100))

planet5_img = pygame.image.load("sprites/planet5.png").convert_alpha()
planet5_img = pygame.transform.scale(planet5_img, (100, 100))

planet6_img = pygame.image.load("sprites/planet6.png").convert_alpha()
planet6_img = pygame.transform.scale(planet6_img, (100, 100))

planet7_img = pygame.image.load("sprites/planet7.png").convert_alpha()
planet7_img = pygame.transform.scale(planet7_img, (100, 100))

planet8_img = pygame.image.load("sprites/planet8.png").convert_alpha()
planet8_img = pygame.transform.scale(planet8_img, (100, 100))

goal_img = pygame.image.load("sprites/goalAura.png").convert_alpha()
goal_img = pygame.transform.scale(goal_img, (100, 100))

bodies = [
    bodies.Static_body(0, 0, 5e28, 20, (255, 255, 0), planet1_img),
    bodies.Static_body(4e12, 2e12, 2e30, 20, (255,0,0), planet2_img),
    bodies.Static_body(6e12, 0, 1e30, 20, (0,0,0), planet3_img),
    bodies.Static_body(8e12, 0, 8e21, 20, (0,0,0), planet4_img),
    bodies.Static_body(-5e12, 0, 2e31, 20, (0,0,0), planet5_img),
    bodies.Static_body(8e12, -5e12, 8e28, 20, (0,0,0), goal_img),
    bodies.Static_body(-2e12, -5e12, 1e30, 20, (0,0,0), planet6_img),
    bodies.Static_body(6e12, -4e12, 1e30, 20, (0,0,0), planet7_img),
    bodies.Static_body(0, 4e12, 1e30, 20, (0,0,0), planet8_img),
]