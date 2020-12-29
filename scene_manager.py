from config import *
from components.scene import Scene
from components.button import Button


class SceneManager:
    def __init__(self):
        self.screen = SCREEN
        self.scenes = self.__create_scenes()
        self.current_scene = self.scenes[0]

    def set_current_scene(self, scene: Scene):
        self.current_scene = scene

    def get_current_scene(self):
        return self.current_scene

    def draw_current_scene(self):
        if self.current_scene.draw_components() == -1:
            raise Exception("ERROR: list of components for " +
                            self.current_scene.name +
                            " is empty")

    @staticmethod
    def __create_scenes():
        back_button = Button("Back", 10, 10, w=80, h=50)

        main_menu_scene = Scene("main_menu", 'custom_background.png')
        choose_opponent_scene = Scene("choose_opponent", 'custom_background.png')
        game_scene = Scene("game_scene", 'normal_background.png')
        settings_scene = Scene("settings_scene", 'normal_background.png')

        #Create menu scene
        play_button = Button("Play", (SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, 200)
        settings_button = Button("Settings", (SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, 275)
        quit_button = Button("Quit", (SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, 350)
        main_menu_components = [play_button, settings_button, quit_button]
        main_menu_scene.add_components(main_menu_components)

        #Create choose opponent scene
        pvp_button = Button("Player vs Player", (SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, 200)
        pvai_button = Button("Player vs AI", (SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2, 275)
        choose_opponent_scene_components = [pvp_button, pvai_button, back_button]
        choose_opponent_scene.add_components(choose_opponent_scene_components)

        #Create game scene
        game_scene_components = [back_button]
        game_scene.add_components(game_scene_components)

        #Create settings scene
        settings_scene_components = [back_button]
        settings_scene.add_components(settings_scene_components)

        scenes = [main_menu_scene, choose_opponent_scene, game_scene, settings_scene]
        return scenes
