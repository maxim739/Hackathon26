import pygame
import math
import sys

# initialize pygame
pygame.init()
running = True
clock = pygame.time.Clock()

width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gravity Ball")

red = (255, 0, 0)
black = (0, 0, 0)

G = 6.67430e-11
scale = 6e-11
zoom_scale = 1e-9
dt = 864000 #ten days in seconds

zoomed = False

class Static_body:
    def __init__(self, x, y, mass, radius, color):
        self.x, self.y = x,y
        self.mass = mass
        self.radius = radius
        self.color = color
    
    def draw(self, screen):
        
        current_scale = zoom_scale if zoomed else scale

        screen_x = int(self.x * current_scale  + width // 2)
        screen_y = int(self.y * current_scale  + height // 2)
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)


class Moving_body:
    def __init__(self, x, y, vx, vy, mass, radius, color):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.mass = mass
        self.radius = radius
        self.color = color
    
    def update_position(self, bodies):
        fx = fy = 0
        for other in bodies:
            if other != self:
                dx = other.x - self.x
                dy = other.y - self.y
                r = math.sqrt(dx**2 + dy**2)
                if r > 0:
                    f = G * self.mass * other.mass / (r**2)
                    fx += f * dx / r
                    fy += f * dy / r
    
        ax = fx / self.mass
        ay = fy / self.mass 
        self.vx += ax * dt
        self.vy += ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

        current_scale = zoom_scale if zoomed else scale
    
    def draw(self, screen):

        current_scale = zoom_scale if zoomed else scale

        screen_x = int(self.x * current_scale + width // 2)
        screen_y = int(self.y * current_scale + height // 2)
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)

bodies = [
    Static_body(0, 0, 1.989e30, 8, (255, 255, 0)),
    Static_body(2e12, 0, 2e30, 8, (255,0,0)),
    Moving_body(2.867e12, 0, 0, 6810, 8.681e25, 4, (100, 200, 255))
]

while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                zoomed = not zoomed
    
    screen.fill((0,0,0))

    for body in bodies:
        if isinstance(body, Moving_body):
            body.update_position(bodies)
        body.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()