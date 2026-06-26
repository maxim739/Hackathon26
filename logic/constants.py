'''
This script holds all of the constants that are needed
    throughout the project to ensure that necessary
    variables are consistent throughout the project
'''


import pygame

# Game constants
fps = 60
STATE_LANDING = "landing"
STATE_TUT = "tutorial"
STATE_GAME = "game"

# Physics constants
G = 6.67430e-11
scale = 6e-11
dt = 864000 #TEN days in seconds
rocketMass = 8e25

MAX_FORCE = 1e31
MIN_FORCE = 1e20

MAX_ASTEROIDS = 10

# Visual radii in pixels after scaling to display size (computed from non-transparent pixels)
# Planets scale to 140x140, asteroid to 45x45, rocket to 20x20
SPRITE_RADII = {
    'planet1':  43,
    'planet2':  32,
    'planet3':  57,
    'planet4':  56,
    'planet5':  44,
    'planet6':  43,
    'planet7':  64,
    'planet8':  47,
    'goalAura': 55,
    'asteroid': 11,
    'rocket':   11,
}

# Screen values
width = 1300
height = 800

# Colors
opacityVal = 1
thresh = 10

red = pygame.Color(255, 0, 0)
black = (0, 0, 0)
blue = pygame.Color("dodgerblue")
arrow = pygame.Color(50, 50, 50)

startButton = pygame.Color(250, 0, 250)
introButton = pygame.Color(250, 0, 250)
