
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
        self.font = pygame.font.Font('PixelPurl.ttf', 30)


    def draw(self, screen, selected=False):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()


        if selected:
            pygame.draw.rect(screen, self.active_color, (self.x, self.y, self.width, self.height))
        elif (self.x + self.width) > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y:
            pygame.draw.rect(screen, self.active_color, (self.x, self.y, self.width, self.height))
            if click[0] == 1 and self.action is not None:
                self.action()
        else:
            pygame.draw.rect(screen, self.inactive_color, (self.x, self.y, self.width, self.height))    

        #button text
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)
