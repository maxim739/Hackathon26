import pygame
import constants
from assets import IMAGES

pygame.init()
pygame.font.init()

buttonFont = pygame.font.Font('PixelPurl.ttf', 30)
titleFont = pygame.font.Font('PixelPurl.ttf', 120)

start_button = pygame.Rect(constants.width/2-100, constants.height*4/5, 200, 50)
okay_button = pygame.Rect(300, 400, 200, 50)

def draw_button(screen, text, rect, color):
    pygame.draw.rect(screen, color, rect)
    text_surf = buttonFont.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def drawStartWindow(screen):
    screen.blit(IMAGES["planet1"], (300, -25))
    screen.blit(IMAGES["planet2"], (900, 250))
    screen.blit(IMAGES["planet3"], (100, 200))
    screen.blit(IMAGES["planet5"], (1300, 100))
    screen.blit(IMAGES["planet6"], (400, 300))
    screen.blit(IMAGES["planet7"], (1000, 0))
    screen.blit(IMAGES["planet8"], (700, 400))
    screen.blit(IMAGES["goalAura"], (1000, 600))
    screen.blit(IMAGES["rotatedRocket"], (200, 600))


    text_surf = titleFont.render("ROCKETMAN!", True, (255, 255, 255))
    screen.blit(text_surf, (constants.width/2-250, constants.height/5))
    draw_button(screen, " Start ! ", start_button, constants.startButton)

def drawIntroWindow(screen):
    draw_button(screen, " Ready! ", okay_button, constants.introButton)
