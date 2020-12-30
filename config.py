import pygame
DEFAULT_BUTTON_WIDTH = 220
DEFAULT_BUTTON_HEIGHT = 50
BUTTON_DEFAULT_BACKGROUND_BASE_COLOR = [60, 19, 0]
BUTTON_BACKGROUND_DIFFERENCE_COLOR = [20, 0, 10]
BUTTON_DEFAULT_TEXT_BASE_COLOR = [255, 255, 255]
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

MAIN_MENU_SCENE = 0
CHOOSE_OPPONENT_SCENE = 1
GAME_SCENE = 2
SETTINGS_SCENE = 3

AI_MARKER = 0
FIRST_PLAYER_MARKER = 0
SECOND_PLAYER_MARKER = 1

HOLES_PER_LINE = 8
HOLES_PER_COLUMN = 2
GAME_MATRIX = [[0, 4, 4, 4, 4, 4, 4, 0],
               [0, 4, 4, 4, 4, 4, 4, 0]]

ROCKS_COLORS = [(245, 49, 235), (242, 190, 58), (95, 219, 57), (3, 182, 252),
                (235, 64, 52), (27, 242, 235), (251, 255, 8), (252, 86, 111),
                (247, 228, 119), (52, 250, 210), (250, 52, 210), (247, 99, 30),
                (30, 247, 160), (245, 39, 145), (232, 155, 195), (211, 232, 155)]
EPS = 12
