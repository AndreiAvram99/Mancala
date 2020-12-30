from config import *
from copy import deepcopy
from random import randrange
from random import randint


class GameBoard(object):
    def __init__(self):
        self.game_matrix = deepcopy(GAME_MATRIX)
        self.holes_per_line = HOLES_PER_LINE
        self.last_pit = (0, 0)
        self.font = pygame.font.SysFont('arial', 15)
        self.text_base_color = (255, 255, 255)
        self.winner = ""

    def reset_board(self):
        self.game_matrix = deepcopy(GAME_MATRIX)

    def __start_column_left_crossing(self, column, nb_of_rocks, turn):
        for index in range(column - 1, -1 + turn, -1):
            self.game_matrix[0][index] += 1
            nb_of_rocks -= 1
            if nb_of_rocks == 0:
                self.last_pit = (0, index)
                break
        return nb_of_rocks

    def __full_left_crossing(self, nb_of_rocks, turn):
        for index in range(len(self.game_matrix[0]) - 2, -1 + turn, -1):
            self.game_matrix[0][index] += 1
            nb_of_rocks -= 1
            if nb_of_rocks == 0:
                self.last_pit = (0, index)
                break
        return nb_of_rocks

    def __start_column_right_crossing(self, column, nb_of_rocks, turn):
        for index in range(column + 1, len(self.game_matrix[1]) - (1 - turn)):
            self.game_matrix[1][index] += 1
            nb_of_rocks -= 1
            if nb_of_rocks == 0:
                self.last_pit = (1, index)
                break
        return nb_of_rocks

    def __full_right_crossing(self, nb_of_rocks, turn):
        for index in range(1, len(self.game_matrix[1]) - (1 - turn), 1):
            self.game_matrix[1][index] += 1
            nb_of_rocks -= 1
            if nb_of_rocks == 0:
                self.last_pit = (1, index)
                break
        return nb_of_rocks

    def make_move(self, line, column, turn):
        nb_of_rocks = self.game_matrix[line][column]

        if turn == 0:
            nb_of_rocks = self.__start_column_left_crossing(column, nb_of_rocks, turn=0)
            while nb_of_rocks:
                nb_of_rocks = self.__full_right_crossing(nb_of_rocks, turn=0)
                if nb_of_rocks:
                    nb_of_rocks = self.__full_left_crossing(nb_of_rocks, turn=0)

        if turn == 1:
            nb_of_rocks = self.__start_column_right_crossing(column, nb_of_rocks, turn=1)
            while nb_of_rocks:
                nb_of_rocks = self.__full_left_crossing(nb_of_rocks, turn=1)
                if nb_of_rocks:
                    nb_of_rocks = self.__full_right_crossing(nb_of_rocks, turn=1)

        if self.game_matrix[self.last_pit[0]][self.last_pit[1]] == 1 \
                and self.last_pit[0] == turn \
                and self.last_pit[1] != HOLES_PER_LINE - 1 \
                and self.last_pit[1] != 0:

            if turn == 0:
                self.game_matrix[0][0] += (1 + self.game_matrix[1][self.last_pit[1]])
            else:
                self.game_matrix[1][HOLES_PER_LINE - 1] += (1 + self.game_matrix[0][self.last_pit[1]])
            self.game_matrix[turn][self.last_pit[1]] = 0
            self.game_matrix[1 - turn][self.last_pit[1]] = 0

        self.game_matrix[line][column] = 0
        self.game_matrix[1][0] = self.game_matrix[0][0]
        self.game_matrix[0][-1] = self.game_matrix[1][-1]

    def end_game(self, ai_game):
        finish = False
        winner = ""
        if sum(self.game_matrix[0][1:-1]) == 0:
            self.game_matrix[1][-1] += sum(self.game_matrix[1][1:-1])
            self.game_matrix[0][-1] = self.game_matrix[1][-1]
            finish = True
        elif sum(self.game_matrix[1][1:-1]) == 0:
            self.game_matrix[0][0] += sum(self.game_matrix[0][1:-1])
            self.game_matrix[1][0] = self.game_matrix[0][0]
            finish = True

        if finish:
            for line in range(HOLES_PER_COLUMN):
                for column in range(1, HOLES_PER_LINE - 1):
                    self.game_matrix[line][column] = 0

            if self.game_matrix[0][0] > self.game_matrix[1][HOLES_PER_LINE - 1]:
                if ai_game:
                    winner = "AI win"
                    print("AI win")
                else:
                    winner = "Player 1 win"
                    print("Player 1 win")
            elif self.game_matrix[0][0] < self.game_matrix[1][HOLES_PER_LINE - 1]:
                winner = "Player 2 win"
                print("Player 2 win")
            else:
                winner = "Draw"
                print("Draw")

        return winner

    def draw_component(self):
        game_board_img = pygame.image.load('game_board.png')
        SCREEN.blit(game_board_img, (0, 0))

        for line in range(HOLES_PER_COLUMN):
            for column in range(1, HOLES_PER_LINE - 1):
                text_img = self.font.render(str(self.game_matrix[line][column]),
                                            True,
                                            self.text_base_color)
                text_len = text_img.get_width()
                SCREEN.blit(text_img, (95 + 87 * column - text_len / 3,
                                       230 + 185 * line))

        text_img = self.font.render(str(self.game_matrix[0][0]),
                                    True,
                                    self.text_base_color)
        text_len = text_img.get_width()
        SCREEN.blit(text_img, (97 - text_len / 3,
                               230))

        text_img = self.font.render(str(self.game_matrix[1][-1]),
                                    True,
                                    self.text_base_color)
        text_len = text_img.get_width()
        SCREEN.blit(text_img, (95 + 87 * (HOLES_PER_LINE - 1) - text_len / 3,
                               230 + 258))

        self.draw_rocks()

        self.draw_final_game_message()

    @staticmethod
    def draw_rock(color, x, y, r):
        pygame.draw.circle(SCREEN, color, [x, y], r)

    def draw_rocks(self):
        for line in range(HOLES_PER_COLUMN):
            for column in range(1, HOLES_PER_LINE - 1):
                for counter in range(self.game_matrix[line][column]):
                    if line == 0:
                        rock_line = randrange(240 + EPS, 325 - EPS)
                    else:
                        rock_line = randrange(435 + EPS, 520 - EPS)
                    rock_column = randrange(160 + (column - 1) * 85 + EPS, 210 + (column - 1) * 85 - EPS)
                    rock_radius = randrange(5, 7)
                    rock_color_index = randint(0, len(ROCKS_COLORS) - 1)
                    rock_color = ROCKS_COLORS[rock_color_index]
                    self.draw_rock(rock_color, rock_column, rock_line, rock_radius)

        for counter in range(self.game_matrix[0][0]):
            rock_line = randrange(240 + EPS, 510 - EPS)
            rock_column = randrange(160 - 85 + EPS, 210 - 85 - EPS)
            rock_radius = randrange(5, 7)
            rock_color_index = randint(0, len(ROCKS_COLORS) - 1)
            rock_color = ROCKS_COLORS[rock_color_index]
            self.draw_rock(rock_color, rock_column, rock_line, rock_radius)

        for counter in range(self.game_matrix[1][-1]):
            rock_line = randrange(240 + EPS, 510 - EPS)
            rock_column = randrange(160 + 85 * (HOLES_PER_LINE - 2) + EPS, 210 + 85 * (HOLES_PER_LINE - 2) - EPS)
            rock_radius = randrange(5, 7)
            rock_color_index = randint(0, len(ROCKS_COLORS) - 1)
            rock_color = ROCKS_COLORS[rock_color_index]
            self.draw_rock(rock_color, rock_column, rock_line, rock_radius)

    def draw_final_game_message(self):
        if self.winner != '':
            new_font = pygame.font.SysFont('arial', 30)
            text_img = new_font.render(self.winner,
                                       True,
                                       self.text_base_color)
            text_len = text_img.get_width()
            SCREEN.blit(text_img, ((SCREEN_WIDTH - text_len) / 2, 160))

    def set_winner(self, winner):
        self.winner = winner
