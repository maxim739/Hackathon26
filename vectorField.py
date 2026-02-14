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

for x in range((constants.width // 20)+1):
	for y in range((constants.height // 20)+1):
		center = pygame.Vector2((x*20), (y*20))
		draw_arrow(screen, center, (x-y)*10, constants.blue, 5)


while running:
	clock.tick(fps)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	#screen.fill(constants.black)

	pygame.display.flip()

pygame.quit()
sys.exit()
