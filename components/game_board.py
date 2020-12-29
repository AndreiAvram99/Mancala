from config import *


class GameBoard(object):
    def __init__(self):
        self.game_matrix = GAME_MATRIX
        self.holes_per_line = HOLES_PER_LINE
        self.last_hole = (0, 0)

    def valid_move(self, line, column, turn):
        if self.game_matrix[line][column] == 0:
            return False
        if line != turn:
            return False
        if column == 0 or column == len(self.game_matrix[turn]) - 1:
            return False
        return True

    def start_column_left_crossing(self, column, nb_of_rocks, turn):
        for index in range(column - 1, -1 + turn, -1):
            self.game_matrix[0][index] += 1
            nb_of_rocks -= 1
            if nb_of_rocks == 0:
                self.last_hole = (0, index)
                break
        return nb_of_rocks

    def full_left_crossing(self, nb_of_rocks, turn):
        for index in range(len(self.game_matrix[0]) - 2, -1 + turn, -1):
            self.game_matrix[0][index] += 1
            nb_of_rocks -= 1
            if nb_of_rocks == 0:
                self.last_hole = (0, index)
                break
        return nb_of_rocks

    def start_column_right_crossing(self, column, nb_of_rocks, turn):
        for index in range(column + 1, len(self.game_matrix[1]) - (1 - turn)):
            self.game_matrix[1][index] += 1
            nb_of_rocks -= 1
            if nb_of_rocks == 0:
                self.last_hole = (1, index)
                break
        return nb_of_rocks

    def full_right_crossing(self, nb_of_rocks, turn):
        for index in range(1, len(self.game_matrix[1]) - (1 - turn), 1):
            self.game_matrix[1][index] += 1
            nb_of_rocks -= 1
            if nb_of_rocks == 0:
                self.last_hole = (1, index)
                break
        return nb_of_rocks

    def make_move(self, line, column, turn):
        if self.valid_move(line, column, turn):
            nb_of_rocks = self.game_matrix[line][column]

            if turn == 0:
                nb_of_rocks = self.start_column_left_crossing(column, nb_of_rocks, turn=0)
                while nb_of_rocks:
                    nb_of_rocks = self.full_right_crossing(nb_of_rocks, turn=0)
                    if nb_of_rocks:
                        nb_of_rocks = self.full_left_crossing(nb_of_rocks, turn=0)

            if turn == 1:
                nb_of_rocks = self.start_column_right_crossing(column, nb_of_rocks, turn=1)
                while nb_of_rocks:
                    nb_of_rocks = self.full_left_crossing(nb_of_rocks, turn=1)
                    if nb_of_rocks:
                        nb_of_rocks = self.full_right_crossing(nb_of_rocks, turn=1)

            if self.game_matrix[turn][self.last_hole[1]] == 1 \
                    and self.last_hole[0] == turn:
                if turn == 0:
                    self.game_matrix[0][0] += (1 + self.game_matrix[1][self.last_hole[1]])
                else:
                    self.game_matrix[1][HOLES_PER_LINE - 1] += (1 + self.game_matrix[0][self.last_hole[1]])
                self.game_matrix[turn][self.last_hole[1]] = 0
                self.game_matrix[1-turn][self.last_hole[1]] = 0

            self.game_matrix[line][column] = 0
            self.game_matrix[1][0] = self.game_matrix[0][0]
            self.game_matrix[0][len(self.game_matrix[line]) - 1] = self.game_matrix[1][len(self.game_matrix[line]) - 1]

    def end_game(self):
        finish = False
        if sum(self.game_matrix[0]) == 0:
            self.game_matrix[1][HOLES_PER_LINE - 1] += sum(self.game_matrix[1])
            self.game_matrix[0][HOLES_PER_LINE - 1] = self.game_matrix[1][HOLES_PER_LINE - 1]
            finish = True
        elif sum(self.game_matrix[1]) == 0:
            self.game_matrix[0][0] += sum(self.game_matrix[0])
            self.game_matrix[1][0] = self.game_matrix[0][0]
            finish = True

        if finish:
            if self.game_matrix[0][0] > self.game_matrix[1][HOLES_PER_LINE - 1]:
                print("player 0 win")
            else:
                print("player 1 win")

        return finish


gb = GameBoard()

gb.make_move(0, 2, 0)
print(gb.game_matrix)
print(gb.last_hole)
gb.make_move(1, 2, 1)
print(gb.game_matrix)
print(gb.last_hole)
gb.make_move(1, 3, 1)
print(gb.game_matrix)
print(gb.last_hole)
gb.make_move(1, 6, 1)
print(gb.game_matrix)
print(gb.last_hole)
gb.make_move(1, 1, 1)
print(gb.game_matrix)
print(gb.last_hole)
