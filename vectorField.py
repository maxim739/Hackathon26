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
	for x in range((constants.width // 20)+1):
		for y in range((constants.height // 20)+1):	# For each vector
			forces = pygame.Vector2(0, 0)
			for body in bodies:
				if isinstance(body, Static_body):
					# Need to add the sum of forces (w sign) to the 2D vector
					dx = (body.screen_x - (x*20))/constants.scale
					dy = (body.screen_y - (y*20))/constants.scale
					dist_sq = dx**2 + dy**2
					if (dist_sq <= 0):
						dist_sq = 10


					dist = math.sqrt(dist_sq)

					force_mag = (constants.G * body.mass * constants.rocketMass) / dist_sq
					forces.x += force_mag * (dx/dist)
					forces.y += force_mag * (dy/dist)

			angle = math.atan2(forces[1], forces[0])
			angle = (angle * (180 / math.pi)) + 90
			
			total_force = math.sqrt(forces[0]**2 + forces[1]**2)

			if total_force > 0:
				log_mag = math.log10(total_force)
				log_min = math.log10(constants.MIN_FORCE)
				log_max = math.log10(constants.MAX_FORCE)
				
				alpha = int(255 * (log_mag - log_min) / (log_max - log_min))
				alpha = max(0, min(255, alpha))
			else:
				alpha = 0
			
			alpha = int(min(255, alpha * constants.opacityVal))

			center = pygame.Vector2((x*20), (y*20))

			color = pygame.Color(alpha, alpha, alpha)

			draw_arrow(screen, center, angle, color, 5)

