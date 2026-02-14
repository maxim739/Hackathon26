import pygame
import sys

import constants	# The constants for the game

pygame.init()
running = True

screen_res = (constants.width, constants.height)

screen = pygame.display.set_mode(screen_res)

for x in range(0, 10):
	for y in range(0, 10):
		pygame.draw.circle(screen, constants.red, center=[(x*50), (y*50)], radius=10)


while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	#screen.fill(constants.black)

	pygame.display.flip()

pygame.quit()
sys.exit()
