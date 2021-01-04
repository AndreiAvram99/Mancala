from components.text_box import TextBox
from config import *
from components.scene import Scene
from components.button import Button
from components.game_board import GameBoard


class SceneManager:
    def __init__(self):
        self.screen = SCREEN
        self.scenes = self.__create_scenes()
        self.current_scene = self.scenes[MAIN_MENU_SCENE]

    def set_current_scene(self, scene: Scene):
        """ SceneManager class method
            This method set the current scene

            Parameters:
            scene (Scene): Scene type object, representing the scene I want to set as the current one
        """

        self.current_scene = scene

    def get_current_scene(self):
        """ SceneManager class method
            This method return the current scene

            Returns:
            Scene:Returning value
        """

        return self.current_scene

    def draw_current_scene(self):
        """ This method call draw_components() method from Scene class
        which draw all the components of a scene.
            If the scene has no components, the function raise an exception
        """

        if self.current_scene.draw_components() == -1:
            raise Exception("ERROR: list of components for " +
                            self.current_scene.name +
                            " is empty")

    @staticmethod
    def __create_scenes():
        """ SceneManager class staticmethod
                    This method create the scenes: instantiate the scene components and
                    add them to the corresponding scenes.
        """

        back_button = Button("Back", 10, 10, w=80, h=50)
        main_menu_scene = Scene("main_menu", 'custom_background.png')
        choose_opponent_scene = Scene("choose_opponent", 'custom_background.png')
        game_scene = Scene("game_scene", 'normal_background.png')
        rules_scene = Scene("rules_scene", 'info_background.png')
        select_names_scene = Scene("select_names_scene", 'custom_background.png')

        #Create menu scene
        play_button = Button("Play", (SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, 200)
        rules_button = Button("Rules", (SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, 275)
        quit_button = Button("Quit", (SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, 350)
        main_menu_components = [play_button, rules_button, quit_button]
        main_menu_scene.add_components(main_menu_components)

        #Create choose opponent scene
        pvp_button = Button("Player vs Player", (SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, 200)
        pvai_button = Button("Player vs AI", (SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, 275)
        choose_opponent_scene_components = [back_button, pvp_button, pvai_button]
        choose_opponent_scene.add_components(choose_opponent_scene_components)

        #Create select names scene
        first_player_tb = TextBox((SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, 200, 200, 40)
        second_player_tb = TextBox((SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, 265, 200, 40)
        play_button = Button("Play", (SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, 350)
        select_names_scene_components = [back_button, play_button, first_player_tb, second_player_tb]
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
