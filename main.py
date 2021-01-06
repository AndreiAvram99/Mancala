from components.ranking import Ranking
from config import *
from ranking_manager import RankingManager
from scene_manager import SceneManager
from game_controller import GameController

# Background sound
pygame.mixer.init()
pygame.mixer.Channel(0).play(pygame.mixer.Sound("./resources/background_music.mp3"), -1)

# Init pygame
pygame.init()
clock = pygame.time.Clock()
run = True

# Instantiate scene_manager and game_controller
scene_manager = SceneManager()
ranking = Ranking()
ranking_manager = RankingManager(ranking)
game_controller = GameController(scene_manager.scenes[GAME_SCENE].scene_components[GAME_BOARD_COMPONENT])

# Init new_scene and current_scene with menu scene and draw menu scene
new_scene = current_scene = scene_manager.get_current_scene()
scene_manager.draw_current_scene()

while run:
    current_scene = scene_manager.get_current_scene()
    # Main menu scene
    if current_scene.name == "main_menu":
        if current_scene.scene_components[PLAY_BUTTON_COMPONENT].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[CHOOSE_OPPONENT_SCENE])
        if current_scene.scene_components[RULES_BUTTON_COMPONENT].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[RULES_SCENE])
        if current_scene.scene_components[RANKING_BUTTON_COMPONENT].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[RANKING_SCENE])
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
            game_controller.complete_game_dict()
            game_controller.reset_all()
        if current_scene.scene_components[PLAY_AGAIN_BUTTON_COMPONENT].action_button:
            game_controller.play_again_reset()
            scene_manager.draw_current_scene()

    # Rules scene
    if current_scene.name == "rules_scene":
        if current_scene.scene_components[BACK_BUTTON_COMPONENT].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[MAIN_MENU_SCENE])

    #Ranking scene
    if current_scene.name == "ranking_scene":
        if current_scene.scene_components[BACK_BUTTON_COMPONENT].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[MAIN_MENU_SCENE])

    # Checking to see if the scene has changed
    new_scene = scene_manager.get_current_scene()
    if new_scene != current_scene:
        scene_manager.draw_current_scene()
        if new_scene.name == "ranking_scene":
            ranking_manager.create_ranking()

    # Close window event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_controller.complete_game_dict()

            run = False

    clock.tick(30)
    pygame.display.update()

pygame.quit()
