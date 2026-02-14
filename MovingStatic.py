import pygame
import math


# initialize pygame
pygame.init()
running = True
clock = pygame.time.Clock()

width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gravity Ball")


G = 6.67430e-11
scale = 6e-11
dt = 864000 #ten days in seconds

class Static_body:
    def __init__(self, x, y, mass, radius, color):
        self.x, self.y = x,y
        self.mass = mass
        self.radius = radius
        self.color = color
    
    def draw(self, screen):
        
        screen_x = int(self.x * scale  + width // 2)
        screen_y = int(self.y * scale  + height // 2)
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)


class Moving_body:
    def __init__(self, x, y, vx, vy, mass, radius, color):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.mass = mass
        self.radius = radius
        self.color = color
    
    def update_position(self, bodies):
        #Euler Integration.. Not stable long term

        #intialize force in x and y
        fx = fy = 0

        #loop through bodies list
        for other in bodies:
            if other != self:
                #get distance between bodies
                dx = other.x - self.x
                dy = other.y - self.y
                r = math.sqrt(dx**2 + dy**2)

                #this is to get rid of dividing by zero 
                if r > 0:
                    #newtons formula f = G Mm / r^2
                    f = G * self.mass * other.mass / (r**2)
                    #break force up into x and y components
                    fx += f * dx / r
                    fy += f * dy / r

        #now that we have the force we can compute the acceleration velocity and position
        ax = fx / self.mass
        ay = fy / self.mass 
        self.vx += ax * dt
        self.vy += ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
    
    def draw(self, screen):

        screen_x = int(self.x * scale + width // 2)
        screen_y = int(self.y * scale + height // 2)
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
    
    screen.fill((0,0,0))

    for body in bodies:
        if isinstance(body, Moving_body):
            body.update_position(bodies)
        body.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()