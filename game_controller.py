from config import *


class GameController:
    def __init__(self):
        self.turn = FIRST_PLAYER_MARKER

    def change_turn(self):
        self.turn = 1 - self.turn

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
