from components.label import Label
from components.text_box import TextBox
from config import *
from components.scene import Scene
from components.button import Button
from components.game_board import GameBoard


class SceneManager:
    """ SceneManager docstring

    Description:
    _________
    This class creates the game scenes and manage the transfer between them

    Attributes:
    ---------
    screen: `pygame.Surface`
        Represents pygame window
    scenes: `List<Scene>`
        This list contains all the scenes
    current_scene: `Scene`
        This attribute contains the current scene

    PublicMethods:
    ---------
    set_current_scene(self, scene: Scene)
    get_current_scene(self)
    draw_current_scene(self)

    StaticMethods:
    ---------
    __create_scenes()
    """
    def __init__(self):
        self.screen = SCREEN
        self.scenes = self.__create_scenes()
        self.current_scene = self.scenes[MAIN_MENU_SCENE]

    def set_current_scene(self, scene: Scene):
        """This method set the current scene
        :param scene: `Scene`
            representing the scene that will be set as current scene
        :return:
        """
        self.current_scene = scene

    def get_current_scene(self):
        """This method return the current scene
        :return self.current_scene: represents the current scene
        """
        return self.current_scene

    def draw_current_scene(self):
        """This method call draw_components() method from Scene class
        which draw all the components of a scene.
            If the scene has no components, the function raise an exception
        :return:
        """
        if self.current_scene.draw_components() == -1:
            raise Exception("ERROR: list of components for " +
                            self.current_scene.name +
                            " is empty")

    @staticmethod
    def __create_scenes():
        """ This method create the scenes: instantiate the scene components and
        add them to the corresponding scenes.
        :return:
        """

        back_button = Button("Back", 10, 10, w=80, h=50)

        main_menu_scene = Scene("main_menu", './resources/custom_background.png')
        choose_opponent_scene = Scene("choose_opponent", './resources/custom_background.png')
        game_scene = Scene("game_scene", './resources/normal_background.png')
        rules_scene = Scene("rules_scene", './resources/info_background.png')
        select_names_scene = Scene("select_names_scene", './resources/custom_background.png')

        #Create menu scene
        play_button = Button("Play", (SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, FIRST_LINE_LAYOUT)
        rules_button = Button("Rules", (SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, SECOND_LINE_LAYOUT)
        quit_button = Button("Quit", (SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, THIRD_LINE_LAYOUT)
        main_menu_components = [quit_button, play_button, rules_button]
        main_menu_scene.add_components(main_menu_components)

        #Create choose opponent scene
        pvp_button = Button("Player vs Player", (SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, FIRST_LINE_LAYOUT)
        pvai_button = Button("Player vs AI", (SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, SECOND_LINE_LAYOUT)
        choose_opponent_scene_components = [back_button, pvp_button, pvai_button]
        choose_opponent_scene.add_components(choose_opponent_scene_components)

        #Create select names scene
        first_player_or_ai_label = Label("First player/AI name:")
        second_player_label = Label("Second player name:")
        first_player_or_ai_label.set_xy((SCREEN_WIDTH - DEFAULT_TB_WIDTH) / 2 - TB_R_PADDING, FIRST_LINE_LAYOUT)
        second_player_label.set_xy((SCREEN_WIDTH - DEFAULT_TB_WIDTH) / 2 - TB_R_PADDING, SECOND_LINE_LAYOUT)

        first_player_tb = TextBox((SCREEN_WIDTH - DEFAULT_TB_WIDTH) / 2, FIRST_LINE_LAYOUT)
        second_player_tb = TextBox((SCREEN_WIDTH - DEFAULT_TB_WIDTH) / 2, SECOND_LINE_LAYOUT)
        play_button = Button("Play", (SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, THIRD_LINE_LAYOUT)
        select_names_scene_components = [back_button, play_button, first_player_tb,
                                         second_player_tb, first_player_or_ai_label, second_player_label]
        select_names_scene.add_components(select_names_scene_components)

        #Create game scene
        play_again_button = Button("Play again", (SCREEN_WIDTH - 170), 10, w=160, h=50)
        game_board = GameBoard()
        game_scene_components = [back_button, game_board, play_again_button]
        game_scene.add_components(game_scene_components)

        #Create rules scene
        settings_scene_components = [back_button]
        rules_scene.add_components(settings_scene_components)

        scenes = [main_menu_scene, choose_opponent_scene, game_scene, rules_scene, select_names_scene]
        return scenes
