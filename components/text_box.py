from config import *


class TextBox:
    """ TextBox docstring

            Description:
            _________
            This class deals with text box drawing and functionality

            Attributes:
            ---------
            rect: `pygame.Rect`
                Text box background
            color: `Tuple[int,int,int]`
                Text box background color
            text: `str`
                Text box text
            font: `pygame.font.Font`
                Text box text font
            active: `boolean`
                Flag:
                    True for clicked in text box
                    False for clicked outside the text box

            PublicMethods:
            ---------
            remove_component(self, index)
            add_component(self, component: object)
            add_components(self, components: List[object])
            draw_components(self)
            """
    def __init__(self, x, y, w=DEFAULT_TB_WIDTH, h=DEFAULT_TB_HEIGHT, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = TB_COLOR_INACTIVE
        self.text = text
        self.text_img = pygame.font.SysFont('arial', 30).render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        """ Check for mouse button down or key down events
        If the player clicked into the tex box it changes its state to active
        If the player press keys and the text box is active change the text attribute and redraw the component
        :param event:
            pygame event
        :return:
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect
            if self.rect.collidepoint(event.pos):
                self.active = True
                pygame.draw.rect(SCREEN, TB_COLOR_ACTIVE, self.rect)
                self.text_img = pygame.font.SysFont('arial', 25).render(self.text, True, (0, 0, 0))
                SCREEN.blit(self.text_img, (self.rect.x + 5, self.rect.y + 5))
            else:
                self.active = False
                pygame.draw.rect(SCREEN, TB_COLOR_INACTIVE, self.rect)
                self.text_img = pygame.font.SysFont('arial', 25).render(self.text, True, (0, 0, 0))
                SCREEN.blit(self.text_img, (self.rect.x + 5, self.rect.y + 5))

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    pygame.draw.rect(SCREEN, TB_COLOR_ACTIVE, self.rect)

                elif len(self.text) <= NAME_MAX_LEN - 1:
                    self.text += event.unicode

                self.text_img = pygame.font.SysFont('arial', 25).render(self.text, True, (0, 0, 0))
                SCREEN.blit(self.text_img, (self.rect.x + 5, self.rect.y + 5))

    def draw_component(self):
        """ Each graphic component has a method that allows it to be drawn (draw_component)
        This draw the text box into the scene
        :return:
        """
        SCREEN.blit(self.text_img, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(SCREEN, self.color, self.rect)
