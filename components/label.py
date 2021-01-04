from config import *


class Label(object):

    def __init__(self,
                 text: str,
                 x=0,
                 y=0,
                 text_base_color=DEFAULT_TEXT_COLOR,
                 font_size=30):

        self.text = text
        self.x = x
        self.y = y
        self.text_base_color = text_base_color
        self.font = pygame.font.SysFont('arial', font_size)

    def set_xy(self, x, y):
        self.x = x
        self.y = y

    def get_text(self):
        return self.text

    def draw_component(self):
        text_img = self.font.render(self.text, True, self.text_base_color)
        SCREEN.blit(text_img, (self.x, self.y))

    def get_label_text_len(self):
        return len(self.text)
