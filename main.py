from components.label import Label
from config import *
from scene_manager import SceneManager
from game_controller import GameController

pygame.mixer.init()
pygame.mixer.Channel(0).play(pygame.mixer.Sound("background_music.mp3"), -1)

pygame.init()
clock = pygame.time.Clock()

scene_manager = SceneManager()

AI_LABEL = Label(AI_LABEL_TEXT)
FIRST_PLAYER_LABEL = Label(FIRST_PLAYER_LABEL_TEXT)
SECOND_PLAYER_LABEL = Label(SECOND_PLAYER_LABEL_TEXT)
AI_LABEL.set_xy((SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2 - 120, 200)
FIRST_PLAYER_LABEL.set_xy((SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2 - 220, 200)
SECOND_PLAYER_LABEL.set_xy((SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2 - 260, 265)
scene_manager.scenes[SELECT_NAMES_SCENE].add_component(SECOND_PLAYER_LABEL)

game_controller = GameController(scene_manager.scenes[GAME_SCENE].ui_components[GAME_BOARD_COMPONENT])

run = True
new_scene = current_scene = scene_manager.get_current_scene()
SCREEN.blit(pygame.image.load(current_scene.background), (0, 0))
scene_manager.draw_current_scene()

while run:
    current_scene = scene_manager.get_current_scene()

    if current_scene.name == "main_menu":
        if current_scene.ui_components[0].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[CHOOSE_OPPONENT_SCENE])
        if current_scene.ui_components[1].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[RULES_SCENE])
        if current_scene.ui_components[2].action_button:
            run = False

    if current_scene.name == "choose_opponent":
        chose_option = False

        if current_scene.ui_components[0].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[MAIN_MENU_SCENE])

        if current_scene.ui_components[1].action_button:
            if scene_manager.scenes[SELECT_NAMES_SCENE].ui_components[-1].get_text() == FIRST_PLAYER_LABEL_TEXT\
               or scene_manager.scenes[SELECT_NAMES_SCENE].ui_components[-1].get_text() == AI_LABEL_TEXT:
                scene_manager.scenes[SELECT_NAMES_SCENE].remove_component(-1)

            scene_manager.scenes[SELECT_NAMES_SCENE].add_component(FIRST_PLAYER_LABEL)
            game_controller.reset_ai_player()
            chose_option = True

        if current_scene.ui_components[2].action_button:
            if scene_manager.scenes[SELECT_NAMES_SCENE].ui_components[-1].get_text() == FIRST_PLAYER_LABEL_TEXT\
               or scene_manager.scenes[SELECT_NAMES_SCENE].ui_components[-1].get_text() == AI_LABEL_TEXT:
                scene_manager.scenes[SELECT_NAMES_SCENE].remove_component(-1)

            scene_manager.scenes[SELECT_NAMES_SCENE].add_component(AI_LABEL)
            game_controller.set_ai_player()
            chose_option = True

        if chose_option:
            scene_manager.set_current_scene(scene_manager.scenes[SELECT_NAMES_SCENE])
            game_controller.reset_board()
            game_controller.reset_turn()
            game_controller.reset_winner()
            game_controller.reset_scores()

    if current_scene.name == "select_names_scene":
        if current_scene.ui_components[0].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[CHOOSE_OPPONENT_SCENE])

        if current_scene.ui_components[1].action_button:
            if len(current_scene.ui_components[2].text) and len(current_scene.ui_components[3].text):
                scene_manager.set_current_scene(scene_manager.scenes[GAME_SCENE])
                game_controller.set_players_names(current_scene.ui_components[2].text,
                                                  current_scene.ui_components[3].text)

        names_tb = [current_scene.ui_components[2], current_scene.ui_components[3]]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            for tb in names_tb:
                tb.handle_event(event)

    if current_scene.name == "game_scene":
        run = game_controller.play(run)

        if current_scene.ui_components[0].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[CHOOSE_OPPONENT_SCENE])

        if current_scene.ui_components[2].action_button:
            game_controller.reset_turn()
            game_controller.reset_board()
            game_controller.reset_winner()
            game_controller.set_is_new_game()
            scene_manager.draw_current_scene()

    if current_scene.name == "rules_scene":
        if current_scene.ui_components[0].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[MAIN_MENU_SCENE])

    new_scene = scene_manager.get_current_scene()
    if new_scene != current_scene:
        SCREEN.blit(pygame.image.load(new_scene.background), (0, 0))
        scene_manager.draw_current_scene()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    clock.tick(30)
    pygame.display.update()

pygame.quit()
