from config import *
from components.game_board import GameBoard
from random import randint
from scene_manager import SceneManager


class GameController:
    def __init__(self):
        self.turn = FIRST_PLAYER_MARKER
        self.ai_player = False
        self.ceva = False

    def reset_ai_player(self):
        self.ai_player = False

    def set_ai_player(self):
        self.ai_player = True

    def change_turn(self):
        self.turn = 1 - self.turn

    def reset_turn(self):
        self.turn = 0

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

    def ai_play(self, game_board: GameBoard, scene_manager: SceneManager, run: bool):
        for event in pygame.event.get():
            if self.turn == AI_MARKER:
                available_positions = []
                for pit in enumerate(game_board.game_matrix[0][1:-1]):
                    if pit[1] != 0:
                        available_positions.append(pit[0] + 1)
                if len(available_positions):
                    if len(available_positions) != 1:
                        column = randint(1, len(available_positions) - 1)
                    else:
                        column = 0
                    game_board.make_move(0,
                                         available_positions[column],
                                         self.turn)
                    scene_manager.draw_current_scene()
                    self.change_turn()

            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                matrix_positions = self.get_matrix_pos_from_mouse(pos)
                if self.valid_move(matrix_positions[0],
                                   matrix_positions[1],
                                   self.turn,
                                   game_board.game_matrix[matrix_positions[0]]
                                                         [matrix_positions[1]]):

                    game_board.make_move(matrix_positions[0],
                                         matrix_positions[1],
                                         self.turn)

                    scene_manager.draw_current_scene()

                    if not (game_board.last_pit == (0, 0) or
                            game_board.last_pit == (1, HOLES_PER_LINE - 1)):
                        self.change_turn()

            winner = game_board.end_game(self.ai_player)
            if winner != '':
                game_board.set_winner(winner)

            if event.type == pygame.QUIT:
                run = False
        return run

    def other_player_play(self, game_board: GameBoard, scene_manager: SceneManager, run: bool):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                matrix_positions = self.get_matrix_pos_from_mouse(pos)
                if self.valid_move(matrix_positions[0],
                                   matrix_positions[1],
                                   self.turn,
                                   game_board.game_matrix[matrix_positions[0]]
                                                         [matrix_positions[1]]):

                    game_board.make_move(matrix_positions[0],
                                         matrix_positions[1],
                                         self.turn)
                    scene_manager.draw_current_scene()

                    if not (game_board.last_pit == (0, 0) or
                            game_board.last_pit == (1, HOLES_PER_LINE - 1)):
                        self.change_turn()

                    winner = game_board.end_game(self.ai_player)
                    if winner != '':
                        game_board.set_winner(winner)

            if event.type == pygame.QUIT:
                run = False
        return run
