from config import *


class Label:
    """ Label docstring

        Description:
        _________
        This class deals with labels drawing

        Attributes:
        ---------
        text: `str`
            Label text
        x: `float`
            Label x position
        y: `float`
            Label y position
        text_base_color: `List[int]`
            Label text color
        font: `pygame.font.Font`
            Label text font

        PublicMethods:
        ---------
        set_xy(self, x, y)
        get_text(self)
        draw_component(self)
        get_text_len(self)
        """

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
        """ Set label coordinates
        :param x:
            Label x coordinates to set
        :param y:
            Label y coordinates to set
        :return:
        """
        self.x = x
        self.y = y

    def get_text(self):
        """ Return label text
        :return self.text: `str`
            Label text
        """
        return self.text

    def draw_component(self):
        """ Each graphic component has a method that allows it to be drawn (draw_component)
        This draw the label into the scene
        :return:
        """
        text_img = self.font.render(self.text, True, self.text_base_color)
        SCREEN.blit(text_img, (self.x, self.y))

    def get_text_len(self):
        """ Return the length of the label text
        :return len(self.text): `int`
            Length of label text
        """
        return len(self.text)
