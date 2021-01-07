from config import *


class Panel:
    def __init__(self, x, y, w, h, panel_color = PANEL_BACKGROUND_COLOR):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.panel_color = panel_color

    def draw_component(self):
        panel_shape = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(SCREEN, self.panel_color, panel_shape)
