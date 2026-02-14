import pygame
import math
import constants


class Static_body:
    def __init__(self, x, y, mass, radius, color):
        self.screen_x = x
        self.screen_y = y
        self.x = x / constants.scale
        self.y = y / constants.scale
        self.mass = mass
        self.radius = radius
        self.color = color
    
    def draw(self, screen, width, height):
        pygame.draw.circle(screen, self.color, (self.screen_x, self.screen_y), self.radius)


class Moving_body:
    def __init__(self, x, y, vx, vy, mass, radius, color):
        self.screen_x = x
        self.screen_y = y
        self.x = x / constants.scale
        self.y = y / constants.scale
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
                if r > (other.radius + self.radius)/constants.scale:
                    #newtons formula f = G Mm / r^2
                    f = constants.G * self.mass * other.mass / (r**2)
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
        self.vx += ax * constants.dt
        self.vy += ay * constants.dt
        self.x += self.vx * constants.dt
        self.y += self.vy * constants.dt
        
    
    def reset(self):
        self.x = 2.867e12
        self.y = 0
        self.vx = 0
        self.vy = 6810
    
    def stop(self):
        self.vx = 0
        self.vy = 0

    def draw(self, screen, width, height):

        screen_x = int(self.x * constants.scale + width // 2)
        screen_y = int(self.y * constants.scale + height // 2)
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)