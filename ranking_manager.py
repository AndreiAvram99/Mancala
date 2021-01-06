import ast
import operator

from components.ranking import Ranking


class RankingManager:
    def __init__(self, ranking_component: Ranking):
        self.ai_winners_dict = {}
        self.players_winners_dict = {}
        self.ranking_component = ranking_component

    def __create_ranking_dicts(self):
        self.ai_winners_dict = {}
        self.players_winners_dict = {}
        winners_file = open('resources/games/games_file', 'r')
        file_line = winners_file.readline()

        while file_line:
            game_info = ast.literal_eval(file_line)
            first_player_name = game_info['first_player/ai_name']
            second_player_name = game_info['second_player_name']
            first_player_score = game_info['first_player/ai_score']
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

    def create_ranking(self):
        self.__create_ranking_dicts()
        self.players_winners_dict = dict(sorted(self.players_winners_dict.items(),
                                                key=operator.itemgetter(1),
                                                reverse=True))
        self.ai_winners_dict = dict(sorted(self.ai_winners_dict.items(),
                                           key=operator.itemgetter(1),
                                           reverse=True))

        self.ranking_component.draw_ranking(self.ai_winners_dict, self.players_winners_dict)
