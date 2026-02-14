import pygame
import sys

import constants				# The constants for the game
from arrow import draw_arrow	# The arrow draw function

clock = pygame.time.Clock()
fps = 60

pygame.init()
running = True

screen_res = (constants.width, constants.height)

screen = pygame.display.set_mode(screen_res)

for x in range(1, 10):
	for y in range(1, 10):
		center = pygame.Vector2((x*50), (y*50))
		draw_arrow(screen, center, 0, constants.red, 10)


while running:
	clock.tick(fps)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	#screen.fill(constants.black)

	pygame.display.flip()

pygame.quit()
sys.exit()
