import pygame
import math
import constants


class Static_body:
    def __init__(self, x, y, mass, radius, color, image=None):
        self.screen_x = x
        self.screen_y = y
        self.x = x / constants.scale
        self.y = y / constants.scale
        self.mass = mass
        self.radius = radius
        self.color = color
        self.image = image
    
    def draw(self, screen, width, height):
        #pygame.draw.circle(screen, self.color, (self.screen_x, self.screen_y), self.radius)

        if self.image:
            rect = self.image.get_rect(center=(self.screen_x, self.screen_y))
            screen.blit(self.image, rect)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1,4):
            img = pygame.image.load(f"sprites/explosion{num}.png")
            img = pygame.transform.scale(img, (100,100))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 4
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

		#if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill() 

explosion_group = pygame.sprite.Group()


class Moving_body:
    def __init__(self, x, y, vx, vy, mass, radius, color, image=None):
        self.screen_x = x
        self.screen_y = y
        self.x = x / constants.scale
        self.y = y / constants.scale
        self.vx, self.vy = vx, vy
        self.mass = mass
        self.radius = radius
        self.color = color
        self.image = image
        self.dead = False

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
        
                else:
                    if not self.dead:
                        screen_x = int(self.x * constants.scale  + constants.width // 2)
                        screen_y = int(self.y * constants.scale  + constants.height // 2)

                        explosion = Explosion(screen_x,screen_y)
                        explosion_group.add(explosion)

                        self.dead = True
                        self.vx = 0
                        self.vy = 0
                    return

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

        screen_x = self.x * constants.scale 
        screen_y = self.y * constants.scale

        if self.image:
            #only roate when body is moving
            if self.vx != 0 or self.vy != 0:
                # atan2 returns angle between two axis in radians 
                # use math.degrees to change into degrees
                angle = math.degrees(math.atan2(self.vy, -self.vx))

                angle += 90
                # rotates the image... uses pygame transform
                rotated_image = pygame.transform.rotate(self.image, angle)

                #draws the image as a rect
                rect = rotated_image.get_rect(center=(screen_x, screen_y))
                screen.blit(rotated_image, rect)
            else:
                rect = self.image.get_rect(center=(screen_x, screen_y))
                screen.blit(self.image, rect)
        else:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)