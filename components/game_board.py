from pygame import Rect

from config import *
from copy import deepcopy
from random import randrange
from random import randint


class GameBoard:
    """ GameBoard docstring

        Description:
        _________
        This class deals with visual components of the game board

        Attributes:
        ---------
        game_matrix: `List[List[int]]`
            This attribute contains the current scene
        font: `pygame.font.Font`
            Pit's number of rocks label font
        text_base_color: `[int, int, int]`
            Pit's number of rocks label text color
        last_drew_rocks: `list`
            List of the rocks characteristics for every pit
        winner: `str`
            Game winner
        first_player_label: `str`
            First player name label
        second_player_label: `str`
            Second player name label
        first_player_score_label: `str`
            First player score label
        second_player_score_label: `str`
            Second player score label

        PublicMethods:
        ---------
        set_players_names_labels(self, first_player_label: str, second_player_label: str)
        set_players_scores_labels(self, first_player_score: int, second_player_score: int)
        def draw_component(self)

        PrivateMethods:
        ---------
        __draw_players_labels(self)
        __draw_rocks_nb_labels(self)
        __draw_final_game_message(self)

        StaticMethods:
        ---------
        __draw_rock(attributes)
        """

    def __init__(self):
        self.game_matrix = deepcopy(GAME_MATRIX)
        self.font = pygame.font.SysFont('arial', 15)
        self.text_base_color = DEFAULT_TEXT_COLOR
        self.last_drew_rocks = []
        self.winner = ""
        self.first_player_label = ""
        self.second_player_label = ""
        self.first_player_score_label = ""
        self.second_player_score_label = ""

    def set_players_names_labels(self, first_player_label: str, second_player_label: str):
        """ Set players names labels value
        :param first_player_label: `str`
            First player name
        :param second_player_label: `str`
            Second player name
        :return:
        """
        self.first_player_label = first_player_label
        self.second_player_label = second_player_label

    def set_players_scores_labels(self, first_player_score: int, second_player_score: int):
        """ Set players scores labels value
        :param first_player_score:
            First player score
        :param second_player_score:
            Second player score
        :return:
        """
        self.first_player_score_label = str(first_player_score)
        self.second_player_score_label = str(second_player_score)

    def draw_component(self):
        """ Each graphic component has a method that allows it to be drawn (draw_component)
        This draw the game_board and its components(player labels, number of rocks labels, rocks, final game message)
        into the scene
        :return:
        """
        game_board_img = pygame.image.load('resources/game_board.png')
        SCREEN.blit(game_board_img, (0, 0))

        self.__draw_players_labels()
        self.__draw_rocks_nb_labels()
        self.__draw_rocks()
        self.__draw_final_game_message()

    def __draw_players_labels(self):
        """ For players names labels
        :return:
        """
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
        button_rect = Rect(30 + 87 * (PITS_PER_LINE - 1) - text_len / 3 - 5, 235 + 318, text_len + 15, 40)
        pygame.draw.rect(SCREEN, BUTTON_DEFAULT_BACKGROUND_BASE_COLOR, button_rect)
        SCREEN.blit(text_img, (30 + 87 * (PITS_PER_LINE - 1) - text_len / 3,
                               235 + 318))

    def __draw_rocks_nb_labels(self):
        """ For all pits and mancala draw number of rocks label
        :return:
        """
        # Labels for pits
        for line in range(PITS_PER_COLUMN):
            for column in range(1, PITS_PER_LINE - 1):
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
        SCREEN.blit(text_img, (95 + 87 * (PITS_PER_LINE - 1) - text_len / 3,
                               230 + 258))

    @staticmethod
    def __draw_rock(attributes):
        """
        Draw a rock with specified attributes as param
        :param attributes:
            Rocks attributes([rock_color, rock_column, rock_line, rock_radius])
        :return:
        """
        pygame.draw.circle(SCREEN,
                           attributes[ROCK_COLOR_ATTR_INDEX],
                           [attributes[ROCK_COLUMN_ATTR_INDEX], attributes[ROCK_LINE_ATTR_INDEX]],
                           attributes[ROCKS_RADIUS_ATTR_INDEX])

    def __draw_rocks(self):
        """
        Draw the rocks for ever pit and mancala.
        If the number of rocks in a pit doesn't change the rocks will have the same attributes
        :return:
        """
        last_drew_rocks_copy = deepcopy(self.last_drew_rocks)
        self.last_drew_rocks.clear()

        for line in range(PITS_PER_COLUMN):
            for column in range(1, PITS_PER_LINE - 1):
                last_drew_rocks_per_pit = []
                target = column - 1 + line * (PITS_PER_LINE - 2)
                if len(last_drew_rocks_copy) != 0 and \
                        self.game_matrix[line][column] == len(last_drew_rocks_copy[target]):
                    for counter in range(len(last_drew_rocks_copy[target])):
                        self.__draw_rock(last_drew_rocks_copy[target][counter])
                    self.last_drew_rocks.append(last_drew_rocks_copy[target])
                else:
                    for counter in range(self.game_matrix[line][column]):
                        if line == 0:
                            rock_line = randrange(240 + EPS, 325 - EPS)
                        else:
                            rock_line = randrange(435 + EPS, 520 - EPS)
                        rock_column = randrange(160 + (column - 1) * 85 + EPS, 210 + (column - 1) * 85 - EPS)
                        rock_radius = randrange(4, 7)
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
                rock_column = randrange(170 + 85 * (PITS_PER_LINE - 2) + EPS, 220 + 85 * (PITS_PER_LINE - 2) - EPS)
                rock_radius = randrange(5, 7)
                rock_color_index = randint(0, len(ROCKS_COLORS) - 1)
                rock_color = ROCKS_COLORS[rock_color_index]
                last_drew_rocks_per_pit.append([rock_color, rock_column, rock_line, rock_radius])
                self.__draw_rock([rock_color, rock_column, rock_line, rock_radius])
            self.last_drew_rocks.append(last_drew_rocks_per_pit)

    def __draw_final_game_message(self):
        """ Draw final game message label
        :return:
        """
        if self.winner != '':
            new_font = pygame.font.SysFont('arial', 30)
            if self.winner != "Draw":
                self.winner += " win!"
            text_img = new_font.render(self.winner,
                                       True,
                                       DEFAULT_TEXT_COLOR)
            text_len = text_img.get_width()
            SCREEN.blit(text_img, ((SCREEN_WIDTH - text_len) / 2, 160))
