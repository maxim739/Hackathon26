import pygame
import constants
from assets import IMAGES

pygame.init()
pygame.font.init()

buttonFont = pygame.font.Font('PixelPurl.ttf', 30)
titleFont = pygame.font.Font('PixelPurl.ttf', 120)
tutFont = pygame.font.Font('PixelPurl.ttf', 40)

start_button = pygame.Rect(constants.width/2-100, constants.height*4/5, 200, 50)
okay_button = pygame.Rect(constants.width/2-100, constants.height*4/5, 200, 50)
launch_button = pygame.Rect(constants.width*7/8, constants.height*7/8, 200, 50)

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
    text1_surf = buttonFont.render("Made by Maxim DeJong, William Gray, and Saabir Yousuf", True, (255, 255, 255))
    text2_surf = buttonFont.render("McGill Physics Hackathon 2026", True, (255, 255, 255))

    screen.blit(text_surf, (constants.width/2-250, constants.height/5))
    screen.blit(text1_surf, (constants.width/2-275, constants.height*4/5+110))
    screen.blit(text2_surf, (constants.width/2-150, constants.height*4/5+135))

    draw_button(screen, " Start ! ", start_button, constants.startButton)

def drawIntroWindow(screen):
    text1_surf = tutFont.render("Please save us! We don't know how to get home!", True, (255, 255, 255))
    text2_surf = tutFont.render("You can place asteriods in the Universe to alter our path with gravity.", True, (255, 255, 255))
    text3_surf = tutFont.render("     Press r to restart!", True, (255, 255, 255))
    text4_surf = tutFont.render("Make sure we don't crash!", True, (255, 255, 255))

    screen.blit(IMAGES["planet1"], (300, -25))
    screen.blit(IMAGES["planet2"], (900, 250))
    screen.blit(IMAGES["planet3"], (100, 200))
    screen.blit(IMAGES["planet5"], (1300, 100))
    screen.blit(IMAGES["planet6"], (400, 300))
    screen.blit(IMAGES["planet7"], (1000, 0))
    screen.blit(IMAGES["planet8"], (700, 400))
    screen.blit(IMAGES["goalAura"], (1000, 600))
    screen.blit(IMAGES["rotatedRocket"], (200, 600))

    screen.blit(text1_surf, (constants.width/2-250-100, constants.height/5))
    screen.blit(text2_surf, (constants.width/2-250-250, constants.height/5+25))
    screen.blit(text3_surf, (constants.width/2-200, constants.height/5+50))
    screen.blit(text4_surf, (constants.width/2-175, constants.height/5+75)
                )
    draw_button(screen, " Ready! ", okay_button, constants.introButton)

def drawGameWindow(screen):
    # Launch Button
    draw_button(screen, " Launch! ", launch_button, constants.startButton)

def drawWinWindow(screen):
    overlay = pygame.Surface((constants.width, constants.height))
    overlay.set_alpha(200)
    overlay.fill((0, 50, 0))  # Dark green tint
    screen.blit(overlay, (0, 0))
        
        # Display WIN text
    win_font = titleFont
    win_text = win_font.render("YOU WIN!", True, (0, 255, 0))
    win_rect = win_text.get_rect(center=(constants.width // 2, constants.height // 2 - 50))
    screen.blit(win_text, win_rect)
        
        # Display restart instruction
    restart_font = tutFont
    restart_text = restart_font.render("Press R to Restart", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(constants.width // 2, constants.height // 2 + 50))
    screen.blit(restart_text, restart_rect)

