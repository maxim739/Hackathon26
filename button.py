
import pygame

class Button:
    def __init__(self, text, x, y, width, height, inactive_color, active_color, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.action = action


    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()


        if (self.x + self.width) > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y:
            pygame.draw.rect(screen, self.active_color, (self.x, self.y, self.width, self.height))
            if click[0] == 1 and self.action is not None:
                self.action()
        else:
            pygame.draw.rect(screen, self.inactive_color, (self.x, self.y, self.width, self.height))    
