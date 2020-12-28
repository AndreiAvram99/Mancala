import pygame
from pygame.locals import *
from config import *


class Button(object):

    def __init__(self,
                 text: str,
                 x: float,
                 y: float,
                 background_base_color=BUTTON_DEFAULT_BACKGROUND_BASE_COLOR,
                 text_base_color=BUTTON_DEFAULT_TEXT_BASE_COLOR):

        self.text = text
        self.x = x
        self.y = y
        self.w = BUTTON_WIDTH
        self.h = BUTTON_HEIGHT
        self.background_base_color = background_base_color
        self.background_hover_color = (122, 65, 65)
        self.text_base_color = text_base_color
        self.clicked = False
        self.font = pygame.font.SysFont('arial', 30)

    def draw_button(self):
        action = False

        #get mouse positions
        mouse_positions = pygame.mouse.get_pos()

        #create pygame Rect object for the button
        button_rect = Rect(self.x, self.y, self.w, self.h)

        if button_rect.collidepoint(mouse_positions):
            if pygame.mouse.get_pressed(3)[0] == 1:
                self.clicked = True
            elif pygame.mouse.get_pressed(3)[0] == 0 and self.clicked == True:
                self.clicked = False
                action = True
            else:
                pygame.draw.rect(screen, self.background_hover_color, button_rect)
        else:
            pygame.draw.rect(screen, self.background_base_color, button_rect)

        #add text to button
        text_img = self.font.render(self.text, True, self.text_base_color)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.w / 2) - int(text_len / 2), self.y + 5))
        return action


pygame.init()
screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Button Demo")

test = Button("Test", 75, 200)
test_2 = Button("New_button", 100, 300, (124, 244, 33), (32, 123, 123))
run = True
bg = (122, 122, 122)


while run:

    screen.fill(bg)

    if test.draw_button():
        print("merge")
    if test_2.draw_button():
        print("merge si asta")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
