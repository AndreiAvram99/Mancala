from copy import deepcopy

from components.game_board import GameBoard
from config import *
from random import randint


class GameController:
    """ GameController docstring

        Description:
        _________
        This class deals with the logic of the game: make a move depending on the type of players,
        decide who the winner is and communicate with the "GameBoard" class to draw the changes.
        It also remembers the score of each player for a certain game and the number of games ended in a draw.

        Attributes:
        ---------
        turn: `int`
            This attribute remember which player's turn it is.
        ai_player: `boolean`
            This attribute knows if it's AI's turn
        game_board: `GameBoard`
            Game board component
        winner: `str`
            Represents the winner of the game, if there is no winner it is Null else
            otherwise remember the name of the winner or "Draw" in case of a draw
        last_pit: `(int, int)`
            Remember the last pit coordinates in which a rock was placed
        first_player_name: `str`
            Contains the name of the first player
        second_player_name: `str`
            Contains the name of the second player
        first_player_score: `int`
            Contains first player score for games with the same players
        second_player_score: `int`
            Contains second player score for games with the same players
        is_new_game: `boolean`
            Check if the play again button has been pressed
        nb_of_draw_games: `int`
            Counts the number of draw games with the same players
        game_dict: `dict`
            Store information about all games
        turn_association: `dict`
            Associate a name with player turn

        PublicMethods:
        ---------
        complete_game_dict(self)
        play_again_reset(self)
        reset_all(self)
        reset_ai_player(self)
        set_ai_player(self)
        reset_nb_of_draw_games(self)
        set_players_names_and_scores(self, first_player_name, second_player_name)
        reset_scores(self)
        change_turn(self)
        reset_turn(self)
        reset_board(self)
        set_winner(self, winner)
        reset_winner(self)
        set_is_new_game(self)
        valid_move(self, line, column, turn)
        play(self)

        PrivateMethods:
        ---------
        __start_column_left_crossing(self, column, nb_of_rocks)
        __full_left_crossing(self, nb_of_rocks, turn)
        __start_column_right_crossing(self, column, nb_of_rocks)
        __full_right_crossing(self, nb_of_rocks, turn)
        __make_move(self, line, column, turn)
        __clear_left_rocks(self)
        __end_game(self)

        StaticMethods:
        ---------
        get_matrix_pos_from_mouse(mouse_positions)

    """
    def __init__(self, game_board: GameBoard):
        self.turn = randint(0, 1)
        self.ai_player = False
        self.game_board = game_board
        self.winner = ""
        self.last_pit = (0, 0)
        self.first_player_name = ""
        self.second_player_name = ""
        self.first_player_score = 0
        self.second_player_score = 0
        self.is_new_game = True
        self.nb_of_draw_games = 0
        self.game_dict = {}
        self.turn_association = {}

    def complete_game_dict(self):
        """ Restores the dictionary if more games have been added.
        :return:
        """
        if self.first_player_score != 0 or self.second_player_score != 0:
            games_file = open('resources/games/games_file', 'a')
            self.game_dict = self.__dict__.copy()
            self.game_dict.pop('game_board')
            self.game_dict.pop('game_dict')
            games_file.write(str(self.game_dict) + '\n')

    def play_again_reset(self):
        """ Reset attributes in case of play again with the same players
        :return:
        """
        self.reset_turn()
        self.reset_board()
        self.reset_winner()
        self.set_is_new_game()
        self.game_board.draw_component()
        self.game_board.draw_turn(self.turn_association[self.turn])

    def reset_all(self):
        """ Reset attributes in case of change players
        :return:
        """
        self.reset_board()
        self.reset_turn()
        self.reset_winner()
        self.set_is_new_game()
        self.reset_nb_of_draw_games()
        self.reset_scores()

    def reset_ai_player(self):
        """Reset the flag for AI when the player return to the choose opponent scene
        :return:
        """
        self.ai_player = False

    def set_ai_player(self):
        """Set the flag for AI if the player has chosen AI opponent
        :return:
        """
        self.ai_player = True

    def reset_nb_of_draw_games(self):
        """Reset the number of draw games if the player returned to the choose opponent scene
        :return:
        """
        self.nb_of_draw_games = 0

    def set_players_names_and_scores(self, first_player_name, second_player_name):
        """ Set the players names and sends them to the game board to draw them
        :param first_player_name: `str`
            Contains first player name
        :param second_player_name: `str`
            Contains second player name
        :return:
        """
        self.first_player_name = first_player_name
        self.second_player_name = second_player_name
        self.turn_association = {0: self.first_player_name, 1: self.second_player_name}
        self.game_board.set_players_names_labels(first_player_name, second_player_name)
        self.game_board.set_players_scores_labels(self.first_player_score, self.second_player_score)

    def reset_scores(self):
        """ Reset scores for both players when the player return to choose opponent scene
        :return:
        """
        self.first_player_score = 0
        self.second_player_score = 0

    def change_turn(self):
        """ Change players turn
        :return:
        """
        self.turn = 1 - self.turn

    def reset_turn(self):
        """ Reset the turn when a game is over
        :return:
        """
        self.turn = randint(0, 1)

    def reset_board(self):
        """ Reset game board configuration when a game is over
        :return:
        """
        self.game_board.game_matrix = deepcopy(GAME_MATRIX)

    def set_winner(self, winner):
        """ Set the winner and sends it to the game board to draw it in case of a draw,
        the game board draws the "Draw" message
        :param winner: `str`
            Represent the winner's name
        :return:
        """
        self.winner = winner
        self.game_board.winner = winner

    def reset_winner(self):
        """ Reset the winner when start a new game
        :return:
        """
        self.game_board.winner = ""

    def set_is_new_game(self):
        """ Set is_new_game attribute if play again button or back button was pressed"""
        self.is_new_game = True

    def __start_column_left_crossing(self, column, nb_of_rocks):
        """ Cross the matrix to the left from a specified column to first player mancala and add rocks in
        crossing pits until the first(top) player reaches his/her mankala or number of rocks equal to 0.
        If number of rocks equal to 0 then the method set the last pit.
        :param column: `int`
            Start column for crossing
        :param nb_of_rocks: `int`
            Start number of rocks
        :return nb_of_rocks: `int`
            Remaining rocks
        """
        for index in range(column - 1, -1, -1):
            self.game_board.game_matrix[0][index] += 1
            nb_of_rocks -= 1
            if nb_of_rocks == 0:
                self.last_pit = (0, index)
                break
        return nb_of_rocks

    def __full_left_crossing(self, nb_of_rocks, turn):
        """ Crossing the first line pits and add rocks in them from right to left.
        If it is the turn of the first(top) player the function add a rock in player's mancala else not
        :param nb_of_rocks: `int`
            Start number of rocks
        :param turn: `int`
            Player turn
        :return nb_of_rocks: `int`
            Remaining rocks
        """
        for index in range(PITS_PER_LINE - 2, -1 + turn, -1):
            self.game_board.game_matrix[0][index] += 1
            nb_of_rocks -= 1
            if nb_of_rocks == 0:
                self.last_pit = (0, index)
                break
        return nb_of_rocks

    def __start_column_right_crossing(self, column, nb_of_rocks):
        """ Cross the matrix to the right from a specified column to second player mancala and add rocks in
        crossing pits until the second(bottom) player reaches his/her mankala or number of rocks equal to 0.
        If number of rocks equal to 0 then the method set the last pit.
        :param column: `int`
            Start column for crossing
        :param nb_of_rocks: `int`
            Start number of rocks
        :return nb_of_rocks: `int`
            Remaining rocks
        """
        for index in range(column + 1, PITS_PER_LINE, 1):
            self.game_board.game_matrix[1][index] += 1
            nb_of_rocks -= 1
            if nb_of_rocks == 0:
                self.last_pit = (1, index)
                break
        return nb_of_rocks

    def __full_right_crossing(self, nb_of_rocks, turn):
        """ Crossing the second line pits and add rocks in them from left to right.
        If it is the turn of the second(bottom) player the function add a rock in player's mancala else not
        :param nb_of_rocks: `int`
            Start number of rocks
        :param turn: `int`
            Player turn
        :return nb_of_rocks: `int`
            Remaining rocks
        """
        for index in range(1, PITS_PER_LINE - (1 - turn), 1):
            self.game_board.game_matrix[1][index] += 1
            nb_of_rocks -= 1
            if nb_of_rocks == 0:
                self.last_pit = (1, index)
                break
        return nb_of_rocks

    def __make_move(self, line, column, turn):
        """ First time a normal move is made depending on the player turn: if it is the turn of the first(top) player
        it runs at first  __start_column_left_crossing and if there are still rocks, the following functions are
        performed until the rocks are finished: __full_right_crossing and __full_left_crossing in this order.
        For the second(bottom) player the procedure is similar but the functions are executed in reverse order and at
        the beginning __start_column_right_crossing is executed
        After that it is checked if the last pit was empty and its line belongs to the current player and the rocks
        from the opposite line and the respective rock are taken and added in that player's mancala.

        :param line: `int`
            Pit's line
        :param column: `int`
            Pit's column
        :param turn: `int`
            Player turn
        :return:
        """
        nb_of_rocks = self.game_board.game_matrix[line][column]
        self.game_board.game_matrix[line][column] = 0
        # Normal move
        if turn == 0:
            nb_of_rocks = self.__start_column_left_crossing(column, nb_of_rocks)
            while nb_of_rocks:
                nb_of_rocks = self.__full_right_crossing(nb_of_rocks, turn=0)
                if nb_of_rocks:
                    nb_of_rocks = self.__full_left_crossing(nb_of_rocks, turn=0)

        if turn == 1:
            nb_of_rocks = self.__start_column_right_crossing(column, nb_of_rocks)
            while nb_of_rocks:
                nb_of_rocks = self.__full_left_crossing(nb_of_rocks, turn=1)
                if nb_of_rocks:
                    nb_of_rocks = self.__full_right_crossing(nb_of_rocks, turn=1)

        # Special move
        if self.game_board.game_matrix[self.last_pit[0]][self.last_pit[1]] == 1 \
                and self.last_pit[0] == turn \
                and self.last_pit[1] != PITS_PER_LINE - 1 \
                and self.last_pit[1] != 0:
            if turn == 0:
                self.game_board.game_matrix[0][0] += (1 + self.game_board.game_matrix[1][self.last_pit[1]])
            else:
                self.game_board.game_matrix[1][PITS_PER_LINE - 1] += (1 +
                                                                      self.game_board.game_matrix[0][self.last_pit[1]])
            self.game_board.game_matrix[turn][self.last_pit[1]] = 0
            self.game_board.game_matrix[1 - turn][self.last_pit[1]] = 0

        self.game_board.game_matrix[1][0] = self.game_board.game_matrix[0][0]
        self.game_board.game_matrix[0][-1] = self.game_board.game_matrix[1][-1]

    def __clear_left_rocks(self):
        """
        When the game is over this method clear the left rocks
        :return:
        """
        for line in range(PITS_PER_COLUMN):
            for column in range(1, PITS_PER_LINE - 1):
                self.game_board.game_matrix[line][column] = 0
        self.game_board.draw_component()

    def __end_game(self):
        """ Check if a player has run out of rocks on his line.
        If this happens the other player receives the remaining rocks on his line.
        In the end, the winner is determined by who has more rocks in mancala.
        If the players has the same number of rocks it is a draw

        :return local_winner: `str`
            Winner of the current game
        """
        finish = False
        local_winner = ""

        # First line sum
        if sum(self.game_board.game_matrix[0][1:-1]) == 0:
            self.game_board.game_matrix[1][-1] += sum(self.game_board.game_matrix[1][1:-1])
            self.game_board.game_matrix[0][-1] = self.game_board.game_matrix[1][-1]
            finish = True
        # Second line sum
        elif sum(self.game_board.game_matrix[1][1:-1]) == 0:
            self.game_board.game_matrix[0][0] += sum(self.game_board.game_matrix[0][1:-1])
            self.game_board.game_matrix[1][0] = self.game_board.game_matrix[0][0]
            finish = True

        if finish:
            self.__clear_left_rocks()
            if self.game_board.game_matrix[0][0] > self.game_board.game_matrix[1][-1]:
                local_winner = self.first_player_name
                self.first_player_score += 1
            elif self.game_board.game_matrix[0][0] < self.game_board.game_matrix[1][-1]:
                local_winner = self.second_player_name
                self.second_player_score += 1
            else:
                local_winner = "Draw"

        return local_winner

    def valid_move(self, line, column, turn):
        """ Check if  the move is valid
        (don't click out of pits,
         don't click other player's pits,
         don't click on an empty pit).

        :param line: `int`
            Pit's line
        :param column: `int`
            Pit's column
        :param turn: `int`
            Player turn
        :return True/False: `boolean`
            Returned value depends on the move.
            If it was a valid move, return True
            else return False
        """
        if line == -1 or column == -1:
            self.game_board.draw_component()
            self.game_board.draw_invalid_move_label("Invalid move('click outside your pits')")
            return False
        if line != turn:
            self.game_board.draw_component()
            self.game_board.draw_invalid_move_label("Invalid move('click opponent's pit')")
            return False
        nb_of_rocks = self.game_board.game_matrix[line][column]
        if nb_of_rocks == 0:
            self.game_board.draw_component()
            self.game_board.draw_invalid_move_label("Invalid move('you don't have rocks in this pit')")
            return False
        return True

    @staticmethod
    def get_matrix_pos_from_mouse(mouse_positions):
        """ Extract game matrix positions from mouse positions
        :param mouse_positions: `(float, float)`
            Mouse coordinate
        :return [line, column]: `[int, int]`
            Game matrix coordinates
        """
        line = -1
        column = -1

        if 230 <= mouse_positions[1] <= 325:
            line = 0
        elif 415 <= mouse_positions[1] <= 520:
            line = 1

        for index in range(PITS_PER_LINE - 2):
            if 160 + index * 85 <= mouse_positions[0] <= 210 + 85 * index:
                column = index + 1
        return [line, column]

    def play(self):
        """ This method deals with the logic of the game.
        If ai_player is set then the game alternates AI moves with player moves else
        the game will execute only player move.
        For AI the method choose random from a list of valid positions
        At the end, a winner is established and the scores are updated
        :return True/False: `boolean`
            If the player press force quit the function return False to finish instant the game
        """

        for event in pygame.event.get():

            # AI move
            if self.ai_player and self.turn == AI_MARKER:
                # Generate an available position
                available_positions = []
                for pit in enumerate(self.game_board.game_matrix[0][1:-1]):
                    if pit[1] != 0:
                        available_positions.append(pit[0] + 1)
                if len(available_positions):
                    column = randint(0, len(available_positions) - 1)
                    self.__make_move(line=0, column=available_positions[column], turn=self.turn)
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound("resources/pit_select_sound.mp3"))
                    self.game_board.draw_component()
                    if not (self.last_pit == (0, 0)):
                        self.change_turn()
                    self.game_board.draw_turn(self.turn_association[self.turn])

            # Player move
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                matrix_positions = GameController.get_matrix_pos_from_mouse(pos)
                if not self.winner:
                    if self.valid_move(matrix_positions[0], matrix_positions[1], self.turn):

                        self.__make_move(matrix_positions[0], matrix_positions[1], self.turn)
                        pygame.mixer.Channel(2).play(pygame.mixer.Sound("resources/pit_select_sound.mp3"))
                        self.game_board.draw_component()

                        if not (self.last_pit == (0, 0) or
                                self.last_pit == (1, PITS_PER_LINE - 1)):
                            self.change_turn()
                        self.game_board.draw_turn(self.turn_association[self.turn])

            if self.is_new_game:
                self.winner = self.__end_game()
                if self.winner != '':
                    if self.winner == "Draw":
                        self.nb_of_draw_games += 1
                    self.game_board.set_players_scores_labels(self.first_player_score, self.second_player_score)
                    self.game_board.draw_component()
                    self.game_board.draw_final_game_message(self.winner)
                    self.is_new_game = False

            if event.type == pygame.QUIT:
                self.complete_game_dict()
                return False
        return True
