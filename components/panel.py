from config import *


class Panel:
    """ Panel docstring

    Description:
        _________
        This class deals with panels drawing

        Attributes:
        ---------
        x: `float`
            Panel x position
        y: `float`
            Panel y position
        w: `float`
            Panel width
        h: `float`
            Panel height
        panel_color: `List[int]`
            Panel color

        PublicMethods
        ---------
        draw_component(self)

    """
    def __init__(self, x, y, w, h, panel_color=PANEL_BACKGROUND_COLOR):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.panel_color = panel_color

    def draw_component(self):
        """ Each graphic component has a method that allows it to be drawn (draw_component)
        This draw the panel into the scene
        Returns:
        """
        panel_shape = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(SCREEN, self.panel_color, panel_shape)
