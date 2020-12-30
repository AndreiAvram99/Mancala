from config import *
from pygame.locals import *


class Button(object):

    def __init__(self,
                 text: str,
                 x: float,
                 y: float,
                 w=DEFAULT_BUTTON_WIDTH,
                 h=DEFAULT_BUTTON_HEIGHT,
                 background_base_color=BUTTON_DEFAULT_BACKGROUND_BASE_COLOR,
                 text_base_color=BUTTON_DEFAULT_TEXT_BASE_COLOR):

        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.background_base_color = background_base_color
        self.background_hover_color = list(map(lambda i, j: (i + j) % 255,
                                               self.background_base_color,
                                               BUTTON_BACKGROUND_DIFFERENCE_COLOR))
        self.text_base_color = text_base_color
        self.clicked = False
        self.font = pygame.font.SysFont('arial', 30)

    def draw_component(self):
        button_rect = Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(SCREEN, self.background_base_color, button_rect)

        text_img = self.font.render(self.text, True, self.text_base_color)
        text_len = text_img.get_width()
        SCREEN.blit(text_img, (self.x + int(self.w / 2) - int(text_len / 2), self.y + 5))

    @property
    def action_button(self):
        action = False

        # get mouse positions
        mouse_positions = pygame.mouse.get_pos()

        # create pygame Rect object for the button
        button_rect = Rect(self.x, self.y, self.w, self.h)

        if button_rect.collidepoint(mouse_positions):
            if pygame.mouse.get_pressed(3)[0] == 1:
                self.clicked = True
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("button_click_sound.mp3"))

            elif pygame.mouse.get_pressed(3)[0] == 0 and self.clicked:
                self.clicked = False
                action = True
            else:
                pygame.draw.rect(SCREEN, self.background_hover_color, button_rect)
        else:
            pygame.draw.rect(SCREEN, self.background_base_color, button_rect)

        # add text to button
        text_img = self.font.render(self.text, True, self.text_base_color)
        text_len = text_img.get_width()
        SCREEN.blit(text_img, (self.x + int(self.w / 2) - int(text_len / 2), self.y + 5))

        return action
