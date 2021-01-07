import ast
from config import *
from components.ranking import Ranking


class RankingManager:
    """ RankingManager docstring

        Description:
        _________
        This class deals with creating the ranking and send it to Ranking class which draw it

        Attributes:
        ---------
        ai_winners_dic: `dict`
            Dictionary with AI players and their score
        players_winners_dict: `dict`
            Dictionary with players and their score
        ranking_component: `Ranking`
            Draw players(normal + AI) results into the scene

        PublicMethods:
        ---------
        create_ranking(self)

        PrivateMethods:
        ---------
        __create_ranking_dicts(self)

        StaticMethods:
        ---------
        __get_first_players(dictionary: dict)
        __sort_dict_by_values(dictionary: dict)

    """
    def __init__(self, ranking_component: Ranking):
        self.ai_winners_dict = {}
        self.players_winners_dict = {}
        self.ranking_component = ranking_component

    def __create_ranking_dicts(self):
        """ From games_file create the dictionaries with players, AI players and their score
        :return:
        """
        self.ai_winners_dict = {}
        self.players_winners_dict = {}
        winners_file = open('resources/games/games_file', 'r')
        file_line = winners_file.readline()

        while file_line:
            game_info = ast.literal_eval(file_line)
            first_player_name = game_info['first_player_name']
            second_player_name = game_info['second_player_name']
            first_player_score = game_info['first_player_score']
            second_player_score = game_info['second_player_score']

            if game_info['ai_player']:
                if first_player_name not in self.ai_winners_dict.keys():
                    self.ai_winners_dict[first_player_name] = 0
                self.ai_winners_dict[first_player_name] += first_player_score
                if second_player_name not in self.players_winners_dict.keys():
                    self.players_winners_dict[second_player_name] = 0
                self.players_winners_dict[second_player_name] += second_player_score
            else:
                if first_player_name not in self.players_winners_dict.keys():
                    self.players_winners_dict[first_player_name] = 0
                self.players_winners_dict[first_player_name] += first_player_score
                if second_player_name not in self.players_winners_dict.keys():
                    self.players_winners_dict[second_player_name] = 0
                self.players_winners_dict[second_player_name] += second_player_score

            file_line = winners_file.readline()

    @staticmethod
    def __get_first_players(dictionary: dict):
        """ This method receive a dictionary and return a list with first (FIRST_PLAYERS_NB) players and their score
        :param dictionary: `dict`
            The dictionary from which the list will be extracted
        :return first_players_list: `list`
            List with first (FIRST_PLAYERS_NB) players and their score
        """
        if len(dictionary) < FIRST_PLAYERS_NB:
            first_players_list = list(dictionary.items())[:len(dictionary)]
        else:
            first_players_list = list(dictionary.items())[:FIRST_PLAYERS_NB]
        return first_players_list

    @staticmethod
    def __sort_dict_by_values(dictionary: dict):
        """This method receive a dictionary and sort it
        :param dictionary: `dict`
            The dictionary to be sorted
        :return sorted_dict: `dict`
            Sorted dictionary
        """
        sorted_values = sorted(dictionary.values(), reverse=True)
        sorted_dict = {}
        for i in sorted_values:
            for k in dictionary.keys():
                if dictionary[k] == i:
                    sorted_dict[k] = dictionary[k]
        return sorted_dict

    def create_ranking(self):
        """ Call __sort_dict_by_values and __get_first_players and send the result to Ranking class
        which will draw it into the scene
        :return:
        """
        self.__create_ranking_dicts()
        self.players_winners_dict = self.__sort_dict_by_values(self.players_winners_dict)
        self.ai_winners_dict = self.__sort_dict_by_values(self.ai_winners_dict)
        self.ranking_component.draw_ranking(self.__get_first_players(self.ai_winners_dict),
                                            self.__get_first_players(self.players_winners_dict))
