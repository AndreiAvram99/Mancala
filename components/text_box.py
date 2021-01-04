from config import *


class TextBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = pygame.font.SysFont('arial', 30).render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = True
                pygame.draw.rect(SCREEN, COLOR_ACTIVE, self.rect)
                self.txt_surface = pygame.font.SysFont('arial', 25).render(self.text, True, (0, 0, 0))
                SCREEN.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
            else:
                self.active = False
                pygame.draw.rect(SCREEN, COLOR_INACTIVE, self.rect)
                self.txt_surface = pygame.font.SysFont('arial', 25).render(self.text, True, (0, 0, 0))
                SCREEN.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    pygame.draw.rect(SCREEN, COLOR_ACTIVE, self.rect)

                elif len(self.text) <= NAME_MAX_LEN - 1:
                    self.text += event.unicode
                    # Re-render the text.

                self.txt_surface = pygame.font.SysFont('arial', 25).render(self.text, True, (0, 0, 0))
                SCREEN.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

    def draw_component(self):
        SCREEN.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(SCREEN, self.color, self.rect)
