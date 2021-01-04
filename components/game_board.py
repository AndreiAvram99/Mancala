from pygame import Rect

from config import *
from copy import deepcopy
from random import randrange
from random import randint


class GameBoard(object):
    def __init__(self):
        self.game_matrix = deepcopy(GAME_MATRIX)
        self.holes_per_line = HOLES_PER_LINE
        self.font = pygame.font.SysFont('arial', 15)
        self.text_base_color = DEFAULT_TEXT_COLOR
        self.last_drew_rocks = []
        self.winner = ""
        self.first_player_label = ""
        self.second_player_label = ""
        self.first_player_score_label = ""
        self.second_player_score_label = ""

    def set_players_names_labels(self, first_player_label: str, second_player_label: str):
        self.first_player_label = first_player_label
        self.second_player_label = second_player_label

    def set_players_scores_labels(self, first_player_score: int, second_player_score: int):
        self.first_player_score_label = str(first_player_score)
        self.second_player_score_label = str(second_player_score)

    def draw_component(self):
        game_board_img = pygame.image.load('game_board.png')
        SCREEN.blit(game_board_img, (0, 0))

        self.__draw_players_labels()
        self.__draw_rocks_nb_labels()
        self.__draw_rocks()
        self.__draw_final_game_message()

    def __draw_players_labels(self):
        #First player name plus score
        text_img = pygame.font.SysFont('arial', 30).render(self.first_player_label + ": " +
                                                           self.first_player_score_label,
                                                           True,
                                                           self.text_base_color)
        text_len = text_img.get_width()

        button_rect = Rect(50 - 5, 100, text_len + 15, 40)
        pygame.draw.rect(SCREEN, BUTTON_DEFAULT_BACKGROUND_BASE_COLOR, button_rect)
        SCREEN.blit(text_img, (50, 100))

        # Second player name plus score
        text_img = pygame.font.SysFont('arial', 30).render(self.second_player_label + ": " +
                                                           self.second_player_score_label,
                                                           True,
                                                           self.text_base_color)
        text_len = text_img.get_width()
        button_rect = Rect(30 + 87 * (HOLES_PER_LINE - 1) - text_len / 3 - 5, 235 + 318, text_len + 15, 40)
        pygame.draw.rect(SCREEN, BUTTON_DEFAULT_BACKGROUND_BASE_COLOR, button_rect)
        SCREEN.blit(text_img, (30 + 87 * (HOLES_PER_LINE - 1) - text_len / 3,
                               235 + 318))

    def __draw_rocks_nb_labels(self):
        # Labels for pits
        for line in range(HOLES_PER_COLUMN):
            for column in range(1, HOLES_PER_LINE - 1):
                text_img = self.font.render(str(self.game_matrix[line][column]),
                                            True,
                                            self.text_base_color)
                text_len = text_img.get_width()
                SCREEN.blit(text_img, (95 + 87 * column - text_len / 3,
                                       230 + 185 * line))

        # Labels for first mancala
        text_img = self.font.render(str(self.game_matrix[0][0]),
                                    True,
                                    self.text_base_color)
        text_len = text_img.get_width()
        SCREEN.blit(text_img, (97 - text_len / 3,
                               230))

        # Labels for second mancala
        text_img = self.font.render(str(self.game_matrix[1][-1]),
                                    True,
                                    self.text_base_color)
        text_len = text_img.get_width()
        SCREEN.blit(text_img, (95 + 87 * (HOLES_PER_LINE - 1) - text_len / 3,
                               230 + 258))

    @staticmethod
    def __draw_rock(attributes):
        pygame.draw.circle(SCREEN, attributes[0], [attributes[1], attributes[2]], attributes[3])

    def __draw_rocks(self):
        last_drew_rocks_copy = deepcopy(self.last_drew_rocks)
        self.last_drew_rocks.clear()

        for line in range(HOLES_PER_COLUMN):
            for column in range(1, HOLES_PER_LINE - 1):
                last_drew_rocks_per_pit = []
                target = column - 1 + line * (HOLES_PER_LINE - 2)
                if len(last_drew_rocks_copy) != 0 and \
                        self.game_matrix[line][column] == len(last_drew_rocks_copy[target]):
                    for counter in range(len(last_drew_rocks_copy[column - 1 + line * (HOLES_PER_LINE - 2)])):
                        self.__draw_rock(last_drew_rocks_copy[column - 1 + line * (HOLES_PER_LINE - 2)][counter])
                    self.last_drew_rocks.append(last_drew_rocks_copy[column - 1 + line * (HOLES_PER_LINE - 2)])
                else:
                    for counter in range(self.game_matrix[line][column]):
                        if line == 0:
                            rock_line = randrange(240 + EPS, 325 - EPS)
                        else:
                            rock_line = randrange(435 + EPS, 520 - EPS)
                        rock_column = randrange(160 + (column - 1) * 85 + EPS, 210 + (column - 1) * 85 - EPS)
                        rock_radius = randrange(5, 7)
                        rock_color_index = randint(0, len(ROCKS_COLORS) - 1)
                        rock_color = ROCKS_COLORS[rock_color_index]
                        last_drew_rocks_per_pit.append([rock_color, rock_column, rock_line, rock_radius])
                        self.__draw_rock([rock_color, rock_column, rock_line, rock_radius])
                    self.last_drew_rocks.append(last_drew_rocks_per_pit)

        if last_drew_rocks_copy and self.game_matrix[0][0] == len(last_drew_rocks_copy[-2]):
            for counter in range(len(last_drew_rocks_copy[-2])):
                self.__draw_rock(last_drew_rocks_copy[-2][counter])
            self.last_drew_rocks.append(last_drew_rocks_copy[-2])
        else:
            last_drew_rocks_per_pit = []
            for counter in range(self.game_matrix[0][0]):
                rock_line = randrange(240 + EPS, 510 - EPS)
                rock_column = randrange(160 - 85 + EPS, 210 - 85 - EPS)
                rock_radius = randrange(5, 7)
                rock_color_index = randint(0, len(ROCKS_COLORS) - 1)
                rock_color = ROCKS_COLORS[rock_color_index]
                last_drew_rocks_per_pit.append([rock_color, rock_column, rock_line, rock_radius])
                self.__draw_rock([rock_color, rock_column, rock_line, rock_radius])
            self.last_drew_rocks.append(last_drew_rocks_per_pit)

        if last_drew_rocks_copy and self.game_matrix[1][-1] == len(last_drew_rocks_copy[-1]):
            for counter in range(len(last_drew_rocks_copy[-1])):
                self.__draw_rock(last_drew_rocks_copy[-1][counter])
            self.last_drew_rocks.append(last_drew_rocks_copy[-1])
        else:
            last_drew_rocks_per_pit = []
            for counter in range(self.game_matrix[1][-1]):
                rock_line = randrange(240 + EPS, 500 - EPS)
                rock_column = randrange(170 + 85 * (HOLES_PER_LINE - 2) + EPS, 220 + 85 * (HOLES_PER_LINE - 2) - EPS)
                rock_radius = randrange(5, 7)
                rock_color_index = randint(0, len(ROCKS_COLORS) - 1)
                rock_color = ROCKS_COLORS[rock_color_index]
                last_drew_rocks_per_pit.append([rock_color, rock_column, rock_line, rock_radius])
                self.__draw_rock([rock_color, rock_column, rock_line, rock_radius])
            self.last_drew_rocks.append(last_drew_rocks_per_pit)

    def __draw_final_game_message(self):
        if self.winner != '':
            new_font = pygame.font.SysFont('arial', 30)
            text_img = new_font.render(self.winner,
                                       True,
                                       DEFAULT_TEXT_COLOR)
            text_len = text_img.get_width()
            SCREEN.blit(text_img, ((SCREEN_WIDTH - text_len) / 2, 160))
