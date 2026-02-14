import pygame
import math
import constants



# initialize pygame
pygame.init()
running = True
gamestopped = False
playerdead = False
clock = pygame.time.Clock()

screen = pygame.display.set_mode((constants.width, constants.height))
pygame.display.set_caption("Gravity Ball")

#convert alpha keeps png transparent
rocket_img = pygame.image.load("sprites/rocket.png").convert_alpha()
#scales the image up..
rocket_img = pygame.transform.scale(rocket_img, (20, 20))

planet1_img = pygame.image.load("sprites/planet1.png").convert_alpha()
planet1_img = pygame.transform.scale(planet1_img, (100, 100))

planet2_img = pygame.image.load("sprites/planet2.png").convert_alpha()
planet2_img = pygame.transform.scale(planet2_img, (100, 100))

planet3_img = pygame.image.load("sprites/planet3.png").convert_alpha()
planet3_img = pygame.transform.scale(planet3_img, (100, 100))

planet4_img = pygame.image.load("sprites/planet4.png").convert_alpha()
planet4_img = pygame.transform.scale(planet4_img, (100, 100))

planet5_img = pygame.image.load("sprites/planet5.png").convert_alpha()
planet5_img = pygame.transform.scale(planet5_img, (100, 100))

goal_img = pygame.image.load("sprites/goalAura.png").convert_alpha()
goal_img = pygame.transform.scale(goal_img, (100, 100))


G = 6.67430e-11
#This scale stuff is stolen from a man on the internet
scale = 6e-11
dt = 864000 #TEN days in seconds

class Static_body:
    def __init__(self, x, y, mass, radius, color, image=None):
        self.x, self.y = x,y
        self.mass = mass
        self.radius = radius
        self.color = color
        self.image = image
    
    def draw(self, screen):
        
        screen_x = int(self.x * scale  + constants.width // 2)
        screen_y = int(self.y * scale  + constants.height // 2)

        if self.image:
            rect = self.image.get_rect(center=(screen_x, screen_y))
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
        self.x, self.y = x, y
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
                if r > (other.radius + self.radius)/scale:
                    #newtons formula f = G Mm / r^2
                    f = G * self.mass * other.mass / (r**2)
                    #break force up into x and y components
                    fx += f * dx / r
                    fy += f * dy / r
                else:
                    if not self.dead:
                        screen_x = int(self.x * scale  + constants.width // 2)
                        screen_y = int(self.y * scale  + constants.height // 2)

                        explosion = Explosion(screen_x,screen_y)
                        explosion_group.add(explosion)

                        self.dead = True
                        self.vx = 0
                        self.vy = 0
                        self.x = 10000000 // scale
                        self.y = 10000000 // scale
                    return

        #now that we have the force we can compute the acceleration velocity and position
        ax = fx / self.mass
        ay = fy / self.mass 
        self.vx += ax * dt
        self.vy += ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        
    
    def reset(self):
        self.dead = False
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
            pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)

bodies = [
    Static_body(0, 0, 5e31, 20, (255, 255, 0), planet1_img),
    Static_body(4e12, 2e12, 2e30, 20, (255,0,0), planet2_img),
    Static_body(6e12, 0, 1e30, 20, (0,0,0), planet3_img),
    Static_body(8e12, 0, 8e21, 20, (0,0,0), planet4_img),
    Static_body(-5e12, 0, 2e31, 20, (0,0,0), planet5_img),
    Static_body(8e12, -5e12, 8e28, 20, (0,0,0), goal_img),
    Moving_body(2.867e12, 0, 0, 6810, 8.681e25, 4, (100, 200, 255), rocket_img)
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

    explosion_group.update()
    explosion_group.draw(screen)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()