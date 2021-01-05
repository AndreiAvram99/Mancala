from config import *
from scene_manager import SceneManager
from game_controller import GameController

games_file = open('resources/games/games_file', 'a')

# Background sound
pygame.mixer.init()
pygame.mixer.Channel(0).play(pygame.mixer.Sound("./resources/background_music.mp3"), -1)

# Init pygame
pygame.init()
clock = pygame.time.Clock()
run = True

# Instantiate scene_manager and game_controller
scene_manager = SceneManager()
game_controller = GameController(scene_manager.scenes[GAME_SCENE].scene_components[GAME_BOARD_COMPONENT])
# print(game_controller.__doc__)

# Init new_scene and current_scene with menu scene and draw menu scene
new_scene = current_scene = scene_manager.get_current_scene()
scene_manager.draw_current_scene()

# game_dict is used to save last games info
game_dict = {"ai_player": False,
             "last_winner": "",
             "first_player/ai_name": "",
             "second_player_name": "",
             "first_player/ai_score": 0,
             "second_player_score": 0,
             "nb_of_draw_games": 0}

while run:
    current_scene = scene_manager.get_current_scene()

    # Main menu scene
    if current_scene.name == "main_menu":
        if current_scene.scene_components[PLAY_BUTTON_COMPONENT].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[CHOOSE_OPPONENT_SCENE])
        if current_scene.scene_components[RULES_BUTTON_COMPONENT].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[RULES_SCENE])
        if current_scene.scene_components[QUIT_BUTTON_COMPONENT].action_button:
            run = False

    # Choose opponent scene
    if current_scene.name == "choose_opponent":
        chose_option = False

        if current_scene.scene_components[BACK_BUTTON_COMPONENT].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[MAIN_MENU_SCENE])

        if current_scene.scene_components[PLAY_VS_PLAYER_BUTTON_COMPONENT].action_button:
            game_controller.reset_ai_player()
            chose_option = True

        if current_scene.scene_components[PLAY_VS_AI_BUTTON_COMPONENT].action_button:
            game_controller.set_ai_player()
            chose_option = True

        if chose_option:
            scene_manager.set_current_scene(scene_manager.scenes[SELECT_NAMES_SCENE])
            game_controller.reset_board()
            game_controller.reset_turn()
            game_controller.reset_nb_of_draw_games()
            game_controller.reset_winner()
            game_controller.reset_scores()

    # Select names scene
    if current_scene.name == "select_names_scene":
        if current_scene.scene_components[BACK_BUTTON_COMPONENT].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[CHOOSE_OPPONENT_SCENE])

        if current_scene.scene_components[PLAY_BUTTON_COMPONENT].action_button:
            if len(current_scene.scene_components[FIRST_PLAYER_TB_COMPONENT].text) and \
                    len(current_scene.scene_components[SECOND_PLAYER_TB_COMPONENT].text):
                scene_manager.set_current_scene(scene_manager.scenes[GAME_SCENE])
                game_controller.set_players_names(current_scene.scene_components[FIRST_PLAYER_TB_COMPONENT].text,
                                                  current_scene.scene_components[SECOND_PLAYER_TB_COMPONENT].text)

        names_tb = [current_scene.scene_components[FIRST_PLAYER_TB_COMPONENT],
                    current_scene.scene_components[SECOND_PLAYER_TB_COMPONENT]]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            for tb in names_tb:
                tb.handle_event(event)

    # Game scene
    if current_scene.name == "game_scene":
        run = game_controller.play()

        if current_scene.scene_components[BACK_BUTTON_COMPONENT].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[CHOOSE_OPPONENT_SCENE])
            game_controller_dict = game_controller.__dict__
            if game_controller_dict["first_player_score"] != 0 or \
                    game_controller_dict["second_player_score"] != 0 or \
                    game_controller_dict["nb_of_draw_games"] != 0:
                game_dict["ai_player"] = game_controller_dict["ai_player"]
                game_dict["last_winner"] = game_controller_dict["winner"]
                game_dict["first_player/ai_name"] = game_controller_dict["first_player_name"]
                game_dict["second_player_name"] = game_controller_dict["second_player_name"]
                game_dict["first_player/ai_score"] = game_controller_dict["first_player_score"]
                game_dict["second_player_score"] = game_controller_dict["second_player_score"]
                game_dict["nb_of_draw_games"] = game_controller_dict["nb_of_draw_games"]
                games_file.write('\n')
                games_file.write(str(game_dict))
            game_controller.reset_board()
            game_controller.reset_turn()
            game_controller.reset_nb_of_draw_games()
            game_controller.reset_winner()
            game_controller.reset_scores()

        if current_scene.scene_components[PLAY_AGAIN_BUTTON_COMPONENT].action_button:
            game_controller.reset_turn()
            game_controller.reset_board()
            game_controller.reset_winner()
            game_controller.set_is_new_game()
            scene_manager.draw_current_scene()

    # Rules scene
    if current_scene.name == "rules_scene":
        if current_scene.scene_components[BACK_BUTTON_COMPONENT].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[MAIN_MENU_SCENE])

    # Checking to see if the scene has changed
    new_scene = scene_manager.get_current_scene()
    if new_scene != current_scene:
        scene_manager.draw_current_scene()

    # Close window event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    clock.tick(30)
    pygame.display.update()

pygame.quit()
