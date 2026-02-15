import pygame
import constants				# The constants for the game
import math
from bodies import *

def draw_arrow(
    surface: pygame.Surface,
    center: pygame.Vector2,
    angle: float,  # Degrees
    color: pygame.Color,
    size: int = 20,
):
    # Width of the shaft relative to the head size
    sw = size // 3  
    
    # Define the 7 points of the arrow relative to (0,0)
    # Default orientation: pointing UP
    vertices = [
        pygame.Vector2(0, -size),          # 1. Tip
        pygame.Vector2(size, 0),           # 2. Right Head Corner
        pygame.Vector2(sw, 0),             # 3. Right Shoulder
        pygame.Vector2(sw, size*2),          # 4. Bottom Right Tail
        pygame.Vector2(-sw, size*2),         # 5. Bottom Left Tail
        pygame.Vector2(-sw, 0),            # 6. Left Shoulder
        pygame.Vector2(-size, 0),          # 7. Left Head Corner
    ]

    # Rotate each vertex and shift to center
    # .rotate(angle) handles the math; center + v positions it
    rotated_points = [center + v.rotate(angle) for v in vertices]

    # Draw the full arrow as a single polygon
    pygame.draw.polygon(surface, color, rotated_points)


def render(screen, bodies):
	'''Renders a vector field based on passed bodies'''
	# Need to find max and min force values to normalize to the arrows
	cols = (constants.width // 20) + 1
	rows = (constants.height // 20) + 1

	force_grid = [[pygame.Vector2(0, 0) for _ in range(rows)] for _ in range(cols)]

	max_total_force = 0.0
	min_total_force = 1e30

	# Calc forces and find max/min
	for x in range(cols):
		for y in range(rows):
			forces = force_grid[x][y]

			for body in bodies:
				if isinstance(body, Static_body):
					dx = (body.screen_x - (x * 20)) / constants.scale
					dy = (body.screen_y - (y * 20)) / constants.scale
					dist_sq = dx**2 + dy**2 + 0.1
					dist = math.sqrt(dist_sq)

					force_mag = (constants.G * body.mass * constants.rocketMass) / dist_sq
					forces.x += force_mag * (dx/dist)
					forces.y += force_mag * (dy/dist)

					mag = forces.length()
					if mag > max_total_force: max_total_force = mag
					if mag < min_total_force: min_total_force = mag

	max_total_force = max_total_force * 1e0

	log_max = math.log10(max_total_force) if max_total_force > 0 else 0
	log_min = math.log10(min_total_force) if min_total_force > 0 else 0
	log_range = log_max - log_min

	#print(f"Min: {log_max} Max: {log_min}")

	for x in range(cols):
		for y in range(rows):
			forces = force_grid[x][y]
			mag = forces.length()

			if mag > 0 and log_range > 0:
				log_mag = math.log10(mag)
				normalized_val = (log_mag - log_min) / log_range
				sharper = normalized_val ** 20
				color_int = int(sharper * 255)
			else:
				color_int = 0

			color_int = max(0, min(255, color_int))
			angle = math.degrees(math.atan2(forces.y, forces.x)) + 90
			center = pygame.Vector2(x * 20, y * 20)
			color_int = int(min(255, color_int*constants.opacityVal))
			if color_int < constants.thresh: color_int = 0
			color = pygame.Color(color_int, color_int, color_int)
			draw_arrow(screen, center, angle, color, 5)

def renderSurface(target_surface, bodies_list):
	target_surface.fill((0, 0, 0, 0))
	
	cols = (constants.width // 20) + 1
	rows = (constants.height // 20) + 1

	force_grid = [[pygame.Vector2(0, 0) for _ in range(rows)] for _ in range(cols)]

	max_total_force = 0.0
	min_total_force = 1e30

	# Calc forces and find max/min
	for x in range(cols):
		for y in range(rows):
			forces = force_grid[x][y]

			for body in bodies_list:
				if isinstance(body, Static_body):
					dx = (body.screen_x - (x * 20)) / constants.scale
					dy = (body.screen_y - (y * 20)) / constants.scale
					dist_sq = dx**2 + dy**2 + 0.1
					dist = math.sqrt(dist_sq)

					force_mag = (constants.G * body.mass * constants.rocketMass) / dist_sq
					forces.x += force_mag * (dx/dist)
					forces.y += force_mag * (dy/dist)

					mag = forces.length()
					if mag > max_total_force: max_total_force = mag
					if mag < min_total_force: min_total_force = mag

	max_total_force = max_total_force * 1e0

	log_max = math.log10(max_total_force) if max_total_force > 0 else 0
	log_min = math.log10(min_total_force) if min_total_force > 0 else 0
	log_range = log_max - log_min

	#print(f"Min: {log_max} Max: {log_min}")

	for x in range(cols):
		for y in range(rows):
			forces = force_grid[x][y]
			mag = forces.length()

			if mag > 0 and log_range > 0:
				log_mag = math.log10(mag)
				normalized_val = (log_mag - log_min) / log_range
				sharper = normalized_val ** 20
				color_int = int(sharper * 255)
			else:
				color_int = 0

			color_int = max(0, min(255, color_int))
			angle = math.degrees(math.atan2(forces.y, forces.x)) + 90
			center = pygame.Vector2(x * 20, y * 20)
			color_int = int(min(255, color_int*constants.opacityVal))
			if color_int < constants.thresh: color_int = 0
			color = pygame.Color(color_int, color_int, color_int)
			draw_arrow(target_surface, center, angle, color, 5)