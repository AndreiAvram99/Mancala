from copy import deepcopy

from components.game_board import GameBoard
from config import *
from random import randint


class GameController:
    def __init__(self, game_board: GameBoard):
        self.turn = FIRST_PLAYER_MARKER
        self.ai_player = False
        self.game_board = game_board
        self.winner = ""
        self.last_pit = (0, 0)
        self.first_player_name = ""
        self.second_player_name = ""
        self.first_player_score = 0
        self.second_player_score = 0
        self.is_new_game = True

    def reset_ai_player(self):
        self.ai_player = False

    def set_ai_player(self):
        self.ai_player = True

    def set_players_names(self, first_player_name, second_player_name):
        self.first_player_name = first_player_name
        self.second_player_name = second_player_name
        self.game_board.set_players_names_labels(first_player_name, second_player_name)
        self.game_board.set_players_scores_labels(self.first_player_score, self.second_player_score)

    def reset_scores(self):
        self.first_player_score = 0
        self.second_player_score = 0

    def change_turn(self):
        self.turn = 1 - self.turn

    def reset_turn(self):
        self.turn = 0

    def reset_board(self):
        self.game_board.game_matrix = deepcopy(GAME_MATRIX)

    def set_winner(self, winner):
        self.winner = winner
        self.game_board.winner = winner

    def reset_winner(self):
        self.game_board.winner = ""

    def set_is_new_game(self):
        self.is_new_game = True

    def __start_column_left_crossing(self, column, nb_of_rocks, turn):
        for index in range(column - 1, -1 + turn, -1):
            self.game_board.game_matrix[0][index] += 1
            nb_of_rocks -= 1
            if nb_of_rocks == 0:
                self.last_pit = (0, index)
                break
        return nb_of_rocks

    def __full_left_crossing(self, nb_of_rocks, turn):
        for index in range(len(self.game_board.game_matrix[0]) - 2, -1 + turn, -1):
            self.game_board.game_matrix[0][index] += 1
            nb_of_rocks -= 1
            if nb_of_rocks == 0:
                self.last_pit = (0, index)
                break
        return nb_of_rocks

    def __start_column_right_crossing(self, column, nb_of_rocks, turn):
        for index in range(column + 1, len(self.game_board.game_matrix[1]) - (1 - turn)):
            self.game_board.game_matrix[1][index] += 1
            nb_of_rocks -= 1
            if nb_of_rocks == 0:
                self.last_pit = (1, index)
                break
        return nb_of_rocks

    def __full_right_crossing(self, nb_of_rocks, turn):
        for index in range(1, len(self.game_board.game_matrix[1]) - (1 - turn), 1):
            self.game_board.game_matrix[1][index] += 1
            nb_of_rocks -= 1
            if nb_of_rocks == 0:
                self.last_pit = (1, index)
                break
        return nb_of_rocks

    def __make_move(self, line, column, turn):
        nb_of_rocks = self.game_board.game_matrix[line][column]

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

        if self.game_board.game_matrix[self.last_pit[0]][self.last_pit[1]] == 1 \
                and self.last_pit[0] == turn \
                and self.last_pit[1] != HOLES_PER_LINE - 1 \
                and self.last_pit[1] != 0:

            if turn == 0:
                self.game_board.game_matrix[0][0] += (1 + self.game_board.game_matrix[1][self.last_pit[1]])
            else:
                self.game_board.game_matrix[1][HOLES_PER_LINE - 1] += (
                        1 + self.game_board.game_matrix[0][self.last_pit[1]])
            self.game_board.game_matrix[turn][self.last_pit[1]] = 0
            self.game_board.game_matrix[1 - turn][self.last_pit[1]] = 0

        self.game_board.game_matrix[line][column] = 0
        self.game_board.game_matrix[1][0] = self.game_board.game_matrix[0][0]
        self.game_board.game_matrix[0][-1] = self.game_board.game_matrix[1][-1]

    def __end_game(self):
        finish = False
        winner = ""
        if sum(self.game_board.game_matrix[0][1:-1]) == 0:
            self.game_board.game_matrix[1][-1] += sum(self.game_board.game_matrix[1][1:-1])
            self.game_board.game_matrix[0][-1] = self.game_board.game_matrix[1][-1]
            finish = True
        elif sum(self.game_board.game_matrix[1][1:-1]) == 0:
            self.game_board.game_matrix[0][0] += sum(self.game_board.game_matrix[0][1:-1])
            self.game_board.game_matrix[1][0] = self.game_board.game_matrix[0][0]
            finish = True

        if finish:
            for line in range(HOLES_PER_COLUMN):
                for column in range(1, HOLES_PER_LINE - 1):
                    self.game_board.game_matrix[line][column] = 0

            if self.game_board.game_matrix[0][0] > self.game_board.game_matrix[1][HOLES_PER_LINE - 1]:
                winner = self.first_player_name + " win!"
                self.first_player_score += 1
            elif self.game_board.game_matrix[0][0] < self.game_board.game_matrix[1][HOLES_PER_LINE - 1]:
                winner = self.second_player_name + " win!"
                self.second_player_score += 1
            else:
                winner = "Draw"

        return winner

    @staticmethod
    def valid_move(line, column, turn, nb_of_rocks):
        if nb_of_rocks == 0:
            return False
        if line == -1 or column == -1:
            return False
        if line != turn:
            return False
        return True

    @staticmethod
    def get_matrix_pos_from_mouse(mouse_positions):
        line = -1
        column = -1

        if 230 <= mouse_positions[1] <= 325:
            line = 0
        elif 415 <= mouse_positions[1] <= 520:
            line = 1

        for index in range(HOLES_PER_LINE - 2):
            if 160 + index * 85 <= mouse_positions[0] <= 210 + 85 * index:
                column = index + 1
        return [line, column]

    def play(self, run: bool):
        for event in pygame.event.get():
            if self.ai_player and self.turn == AI_MARKER:
                available_positions = []
                for pit in enumerate(self.game_board.game_matrix[0][1:-1]):
                    if pit[1] != 0:
                        available_positions.append(pit[0] + 1)
                if len(available_positions):
                    if len(available_positions) != 1:
                        column = randint(1, len(available_positions) - 1)
                    else:
                        column = 0
                    self.__make_move(0, available_positions[column], self.turn)
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound("pit_select_sound.mp3"))
                    self.game_board.draw_component()
                    self.change_turn()

            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                matrix_positions = self.get_matrix_pos_from_mouse(pos)
                if self.valid_move(matrix_positions[0],
                                   matrix_positions[1],
                                   self.turn,
                                   self.game_board.game_matrix[matrix_positions[0]]
                                   [matrix_positions[1]]):

                    self.__make_move(matrix_positions[0], matrix_positions[1], self.turn)
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound("pit_select_sound.mp3"))
                    self.game_board.draw_component()

                    if not (self.last_pit == (0, 0) or
                            self.last_pit == (1, HOLES_PER_LINE - 1)):
                        self.change_turn()

            if self.is_new_game:
                winner = self.__end_game()
                if winner != '':
                    self.game_board.set_players_scores_labels(self.first_player_score, self.second_player_score)
                    self.is_new_game = False
                    self.set_winner(winner)
                    self.game_board.draw_component()

            if event.type == pygame.QUIT:
                run = False
        return run
