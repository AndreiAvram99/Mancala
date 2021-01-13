from config import *
from pygame.locals import *


class Button:
    """ Button docstring

    Description:
    _________
    This class deals with buttons drawing and functionality

    Attributes:
    ---------
    text: `str`
        Button text
    x: `float`
        Button x coordinate
    y: `float`
        Button y coordinate
    w: `float`
        Button width
    h: `float`
        Button height
    background_base_color: `[int, int, int]`
        Button inactive color
    background_hover_color: `[int, int, int]`
        Button active color is calculated from base color
    text_base_color: `[int, int, int]`
        Button text color
    clicked: `boolean`
        Check if the button was pressed
    font: `pygame.font.Font`
        Button text font

    PublicMethods:
    ---------
    draw_component(self)
    action_button(self)
    """
    def __init__(self,
                 text: str,
                 x: float,
                 y: float,
                 w=DEFAULT_BUTTON_WIDTH,
                 h=DEFAULT_BUTTON_HEIGHT,
                 background_base_color=BUTTON_DEFAULT_BACKGROUND_BASE_COLOR,
                 text_base_color=DEFAULT_TEXT_COLOR):

        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.background_base_color = background_base_color
        self.background_hover_color = [(a + b) % 255 for a, b in zip(self.background_base_color,
                                                                     BUTTON_BACKGROUND_DIFFERENCE_COLOR)]
        self.text_base_color = text_base_color
        self.clicked = False
        self.font = pygame.font.SysFont('arial', 30)

    def draw_component(self):
        """ Each graphic component has a method that allows it to be drawn (draw_component)
        This draw the button into the scene
        :return:
        """
        button_rect = Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(SCREEN, self.background_base_color, button_rect)

        text_img = self.font.render(self.text, True, self.text_base_color)
        text_len = text_img.get_width()
        SCREEN.blit(text_img, (self.x + int(self.w / 2) - int(text_len / 2), self.y + 5))

    def action_button(self):
        """ Check if the button was clicked and release
        :return action: `boolean`
            The action value said if the button was activated(clicked and release) or not
        """
        action = False

        # get mouse positions
        mouse_positions = pygame.mouse.get_pos()

        # create pygame Rect object for the button
        button_rect = Rect(self.x, self.y, self.w, self.h)

        if button_rect.collidepoint(mouse_positions):
            if pygame.mouse.get_pressed(3)[0] == 1:
                self.clicked = True
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("resources/button_click_sound.mp3"))

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
