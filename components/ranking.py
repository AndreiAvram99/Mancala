from components.label import Label
from config import *


class Ranking:
    def __init__(self):
        self.first_players = FIRST_PLAYERS
        self.text_color = DEFAULT_TEXT_COLOR
        self.font_size = 50

    def draw_ranking(self, ai_winners_dict: dict, players_winners_dict: dict):
        if len(ai_winners_dict) < self.first_players:
            ai_winners_list = list(ai_winners_dict.items())[:len(ai_winners_dict)]
        else:
            ai_winners_list = list(ai_winners_dict.items())[:self.first_players]

        if len(players_winners_dict) < self.first_players:
            players_winners_list = list(players_winners_dict.items())[:len(players_winners_dict)]
        else:
            players_winners_list = list(players_winners_dict.items())[:self.first_players]

        label = Label("AI TOP " + str(self.first_players),
                      80,
                      120,
                      [249, 166, 2],
                      self.font_size)
        label.draw_component()

        label = Label("PLAYERS TOP " + str(self.first_players),
                      430,
                      120,
                      [249, 166, 2],
                      self.font_size)
        label.draw_component()

        counter = 0
        for component in ai_winners_list:
            label = Label(component[0] + " : " + str(component[1]),
                          100,
                          200 + counter * 50,
                          self.text_color,
                          self.font_size)
            label.draw_component()
            counter += 1

        counter = 0
        for component in players_winners_list:
            label = Label(component[0] + " : " + str(component[1]),
                          450,
                          200 + counter * 50,
                          self.text_color,
                          self.font_size)
            label.draw_component()
            counter += 1
