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
