import pygame
import sys

# initialize pygame
pygame.init()
running = True
clock = pygame.time.Clock()

dt = 0

width = 1000
height = 600
screen_res = (width, height)
pygame.display.set_caption("Gravity Ball")

red = (255, 0, 0)
black = (0, 0, 0)

#creates position vector for ball
ball_pos = pygame.Vector2(100, 0)
ball_radius = 10
velocity = pygame.Vector2(0, 0)

screen = pygame.display.set_mode(screen_res)

gravity = 980

while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(black)

    velocity.y += gravity * dt

    ball_pos += velocity * dt

    if ball_pos.y + ball_radius > height:
        ball_pos.y = height - ball_radius

        # "energy" loss on bounce
        velocity.y *= -0.8
    
    pygame.draw.circle(screen, red, (int(ball_pos.x), int(ball_pos.y)), ball_radius)

    pygame.display.flip()

pygame.quit()
sys.exit()