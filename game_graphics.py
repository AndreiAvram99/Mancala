import pygame
from pygame.locals import *
from typing import List

from config import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
ceva = True


class Scene(object):
    def __init__(self, name, background):
        self.name = name
        self.ui_components = []
        self.background = background

    def add_component(self, component: object):
        self.ui_components.append(component)

    def add_components(self, components: List[object]):
        self.ui_components += components

    def draw_components(self):
        if len(self.ui_components) == 0:
            return -1

        for component in self.ui_components:
            component.draw_component()


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
        self.background_hover_color = (120, 19, 0)
        self.text_base_color = text_base_color
        self.clicked = False
        self.font = pygame.font.SysFont('arial', 30)

    def draw_component(self):
        button_rect = Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(screen, self.background_base_color, button_rect)

        text_img = self.font.render(self.text, True, self.text_base_color)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.w / 2) - int(text_len / 2), self.y + 5))

    def action_button(self):
        action = False

        # get mouse positions
        mouse_positions = pygame.mouse.get_pos()

        # create pygame Rect object for the button
        button_rect = Rect(self.x, self.y, self.w, self.h)

        if button_rect.collidepoint(mouse_positions):
            if pygame.mouse.get_pressed(3)[0] == 1:
                self.clicked = True
            elif pygame.mouse.get_pressed(3)[0] == 0 and self.clicked:
                self.clicked = False
                action = True
            else:
                pygame.draw.rect(screen, self.background_hover_color, button_rect)
        else:
            pygame.draw.rect(screen, self.background_base_color, button_rect)

        # add text to button
        text_img = self.font.render(self.text, True, self.text_base_color)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.w / 2) - int(text_len / 2), self.y + 5))

        return action


class GameManager:
    def __init__(self):
        self.screen = screen
        self.scenes = self.__create_scenes()
        self.current_scene = self.scenes[0]

    def set_current_scene(self, scene: Scene):
        self.current_scene = scene

    def get_current_scene(self):
        return self.current_scene

    def draw_current_scene(self):
        self.current_scene.draw_components()
        global ceva
        ceva = False

    @staticmethod
    def __create_scenes():
        back_button = Button("Back", 10, 10, w=80, h=50)

        main_menu_scene = Scene("main_menu", 'custom_background.png')
        choose_opponent_scene = Scene("choose_opponent", 'custom_background.png')
        game_scene = Scene("game_scene", 'normal_background.png')
        settings_scene = Scene("settings_scene", 'normal_background.png')

        #Create menu scene
        play_button = Button("Play", (SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, 200)
        settings_button = Button("Settings", (SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, 275)
        quit_button = Button("Quit", (SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, 350)
        main_menu_components = [play_button, settings_button, quit_button]
        main_menu_scene.add_components(main_menu_components)

        #Create choose opponent scene
        pvp_button = Button("Player vs Player", (SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, 200)
        pvai_button = Button("Player vs AI", (SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, 275)
        choose_opponent_scene_components = [pvp_button, pvai_button, back_button]
        choose_opponent_scene.add_components(choose_opponent_scene_components)

        #Create game scene
        game_scene_components = [back_button]
        game_scene.add_components(game_scene_components)

        #Create settings scene
        settings_scene_components = [back_button]
        settings_scene.add_components(settings_scene_components)

        scenes = [main_menu_scene, choose_opponent_scene, game_scene, settings_scene]
        return scenes


gm = GameManager()


run = True
while run:
    current_scene = gm.get_current_scene()
    screen.blit(pygame.image.load(current_scene.background), (0, 0))
    gm.draw_current_scene()

    if current_scene.name == "main_menu":
        if current_scene.ui_components[0].action_button():
            gm.set_current_scene(gm.scenes[1])
        if current_scene.ui_components[1].action_button():
            gm.set_current_scene(gm.scenes[3])
        if current_scene.ui_components[2].action_button():
            run = False

    if current_scene.name == "choose_opponent":
        if current_scene.ui_components[0].action_button():
            gm.set_current_scene(gm.scenes[2])
        if current_scene.ui_components[1].action_button():
            gm.set_current_scene(gm.scenes[2])
        if current_scene.ui_components[2].action_button():
            gm.set_current_scene(gm.scenes[0])

    if current_scene.name == "game_scene":
        if current_scene.ui_components[0].action_button():
            gm.set_current_scene(gm.scenes[1])

    if current_scene.name == "settings_scene":
        if current_scene.ui_components[0].action_button():
            gm.set_current_scene(gm.scenes[0])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
