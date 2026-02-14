import pygame
import constants

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

    text_surf = titleFont.render("ROCKETMAN!", True, (255, 255, 255))
    screen.blit(text_surf, (constants.width/2-250, constants.height/5))
    draw_button(screen, " Start ! ", start_button, constants.startButton)

def drawIntroWindow(screen):
    draw_button(screen, " Ready! ", okay_button, constants.introButton)
