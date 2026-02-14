import pygame
import math
import constants


# initialize pygame
pygame.init()
running = True
clock = pygame.time.Clock()

screen = pygame.display.set_mode((constants.width, constants.height))
pygame.display.set_caption("Gravity Ball")


G = 6.67430e-11
#This scale stuff is stolen from a man on the internet
scale = 6e-11
dt = 864000 #TEN days in seconds
gamestopped = False

class Static_body:
    def __init__(self, x, y, mass, radius, color):
        self.x, self.y = x,y
        self.mass = mass
        self.radius = radius
        self.color = color
    
    def draw(self, screen):
        
        screen_x = int(self.x * scale  + constants.width // 2)
        screen_y = int(self.y * scale  + constants.height // 2)
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)


class Moving_body:
    def __init__(self, x, y, vx, vy, mass, radius, color):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.mass = mass
        self.radius = radius
        self.color = color
    
    def update_position(self, bodies):
        #Euler Numerical Integration.. Not stable long term but should be fine for our game? 
        #Might have to change it in the fututer

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
                if r > (other.radius + self.radius)/scale:
                    #newtons formula f = G Mm / r^2
                    f = G * self.mass * other.mass / (r**2)
                    #break force up into x and y components
                    fx += f * dx / r
                    fy += f * dy / r
                    print(r)
                else:
                    self.vx = 0
                    self.vy = 0

        #now that we have the force we can compute the acceleration velocity and position
        ax = fx / self.mass
        ay = fy / self.mass 
        self.vx += ax * dt
        self.vy += ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        
    
    def reset(self):
        self.x = 2.867e12
        self.y = 0
        self.vx = 0
        self.vy = 6810
    
    def stop(self):
        self.vx = 0
        self.vy = 0

    def draw(self, screen):

        screen_x = int(self.x * scale + constants.width // 2)
        screen_y = int(self.y * scale + constants.height // 2)
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
        
        #Added a reset and stop button also added new boolean called game gamestop
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                gamestopped = False
                for body in bodies:
                    if isinstance(body, Moving_body):
                        body.reset()
            if event.key == pygame.K_s:
                gamestopped = True
                for body in bodies:
                    if isinstance(body, Moving_body):
                        body.stop()
    
    screen.fill((0,0,0))

    for body in bodies:
        #This was CHAT... Had no clue how to make only moving bodies position update
        #Not sure what "isinstance" is
        if isinstance(body, Moving_body) and gamestopped == False:
            body.update_position(bodies)
        body.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()