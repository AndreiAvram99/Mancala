from components.label import Label
from config import *


class Ranking:
    """ Ranking docstring

            Description:
            _________
            This class deals with drawing the ranking

            Attributes:
            ---------
            text_color: `[int, int, int]`
                Ranking text color
            font_size: `int`
                Ranking text size

            PublicMethods:
            ---------
            draw_ranking(self, ai_winners_list: list, players_winners_list: list)
    """
    def __init__(self,
                 text_color=DEFAULT_TEXT_COLOR,
                 font_size=50):
        self.text_color = text_color
        self.font_size = font_size

    def draw_ranking(self, ai_winners_list: list, players_winners_list: list):
        """ Receive winners list from RankingManager, create the labels with the winners and their score and
        draw them
        :param ai_winners_list:  `list`
            First (FIRST_PLAYERS_NB) AI players winners
        :param players_winners_list: `list`
            First (FIRST_PLAYERS_NB) players winners
        :return:
        """
        label = Label("AI TOP " + str(FIRST_PLAYERS_NB),
                      80,
                      120,
                      [249, 166, 2],
                      self.font_size)
        label.draw_component()

        label = Label("PLAYERS TOP " + str(FIRST_PLAYERS_NB),
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
