from pygame import Rect

from components.label import Label
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
        self.text_base_color = DEFAULT_TEXT_COLOR
        self.last_drew_rocks = []
        self.first_player_label_text = ""
        self.second_player_label_text = ""
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
        self.first_player_label_text = first_player_label
        self.second_player_label_text = second_player_label

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

    def __draw_rocks_nb_labels(self):
        """ For all pits and mancala draw number of rocks label
        :return:
        """
        # Labels for pits
        for line in range(PITS_PER_COLUMN):
            for column in range(1, PITS_PER_LINE - 1):
                text = str(self.game_matrix[line][column])
                label = Label(text, text_base_color=self.text_base_color, font_size=15)
                label.set_xy(95 + 87 * column - label.get_text_img_len() / 3,
                             230 + 185 * line)
                label.draw_component()

        # Labels for first mancala
        text = str(self.game_matrix[0][0])
        label = Label(text, text_base_color=self.text_base_color, font_size=15)
        label.set_xy(97 - label.get_text_img_len() / 3, 230)
        label.draw_component()

        # Labels for second mancala
        text = str(self.game_matrix[1][-1])
        label = Label(text, text_base_color=self.text_base_color, font_size=15)
        label.set_xy(95 + 87 * (PITS_PER_LINE - 1) - label.get_text_img_len() / 3, 488)
        label.draw_component()

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
                    for _ in range(self.game_matrix[line][column]):
                        if line == 0:
                            rock_line = randrange(240 + ROCKS_CENTER_EPS, 325 - ROCKS_CENTER_EPS)
                        else:
                            rock_line = randrange(435 + ROCKS_CENTER_EPS, 520 - ROCKS_CENTER_EPS)
                        rock_column = randrange(160 + (column - 1) * 85 + ROCKS_CENTER_EPS, 210 + (column - 1) * 85 - ROCKS_CENTER_EPS)
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
            for _ in range(self.game_matrix[0][0]):
                rock_line = randrange(240 + ROCKS_CENTER_EPS, 510 - ROCKS_CENTER_EPS)
                rock_column = randrange(160 - 85 + ROCKS_CENTER_EPS, 210 - 85 - ROCKS_CENTER_EPS)
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
            for _ in range(self.game_matrix[1][-1]):
                rock_line = randrange(240 + ROCKS_CENTER_EPS, 500 - ROCKS_CENTER_EPS)
                rock_column = randrange(170 + 85 * (PITS_PER_LINE - 2) + ROCKS_CENTER_EPS, 220 + 85 * (PITS_PER_LINE - 2) - ROCKS_CENTER_EPS)
                rock_radius = randrange(5, 7)
                rock_color_index = randint(0, len(ROCKS_COLORS) - 1)
                rock_color = ROCKS_COLORS[rock_color_index]
                last_drew_rocks_per_pit.append([rock_color, rock_column, rock_line, rock_radius])
                self.__draw_rock([rock_color, rock_column, rock_line, rock_radius])
            self.last_drew_rocks.append(last_drew_rocks_per_pit)

    def __draw_players_labels(self):
        """ For players names labels
        :return:
        """
        #First player name plus score        
        first_player_label_text = self.first_player_label_text + ": " + self.first_player_score_label
        first_player_label = Label(first_player_label_text, 50, 100, text_base_color=self.text_base_color)
        score_panel = Rect(50 - 5, 100, first_player_label.get_text_img_len() + 15, 40)
        pygame.draw.rect(SCREEN, PANEL_BACKGROUND_COLOR, score_panel)
        first_player_label.draw_component()

        # Second player name plus score
        second_player_label_text = self.second_player_label_text + ": " + self.second_player_score_label
        second_player_label = Label(second_player_label_text, text_base_color=self.text_base_color)
        second_player_label.set_xy(30 + 87 * (PITS_PER_LINE - 1) - second_player_label.get_text_img_len() / 3, 550)
        score_panel = Rect(25 + 87 * (PITS_PER_LINE - 1) - second_player_label.get_text_img_len() / 3,
                           550,
                           second_player_label.get_text_img_len() + 15,
                           40)
        pygame.draw.rect(SCREEN, PANEL_BACKGROUND_COLOR, score_panel)
        second_player_label.draw_component()

    def draw_final_game_message(self, winner: str):
        """ Draw final game message label
        :return:
        """
        if winner != "Draw":
            winner += " win!"
        winner_label = Label(winner, text_base_color=self.text_base_color)
        winner_label.set_xy((SCREEN_WIDTH - winner_label.get_text_img_len()) / 2,
                            SCREEN_HEIGHT - 440)
        winner_label.draw_component()
        
    def draw_turn(self, text):
        text += " turn"
        turn_panel = Rect(525 - PANEL_PADDING, 100, 230, 40)
        pygame.draw.rect(SCREEN, PANEL_BACKGROUND_COLOR, turn_panel)
        turn_label = Label(text, 525, 100, text_base_color=self.text_base_color)
        turn_label.draw_component()

    def draw_invalid_move_label(self, text):
        invalid_move_label = Label(text, text_base_color=self.text_base_color)
        invalid_move_label.set_xy((SCREEN_WIDTH - invalid_move_label.get_text_img_len()) / 2, SCREEN_HEIGHT - 440)
        invalid_move_label.draw_component()
