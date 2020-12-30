from config import *
from scene_manager import SceneManager
from game_controller import GameController

pygame.mixer.init()
pygame.mixer.Channel(0).play(pygame.mixer.Sound("background_music.mp3"))

pygame.init()

scene_manager = SceneManager()
game_controller = GameController()

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
            scene_manager.set_current_scene(scene_manager.scenes[SETTINGS_SCENE])
        if current_scene.ui_components[2].action_button:
            run = False

    if current_scene.name == "choose_opponent":
        if current_scene.ui_components[0].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[GAME_SCENE])
            scene_manager.scenes[GAME_SCENE].ui_components[1].reset_board()
            game_controller.reset_turn()
            game_controller.reset_ai_player()
            scene_manager.scenes[GAME_SCENE].ui_components[1].winner = ""
        
        if current_scene.ui_components[1].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[GAME_SCENE])
            scene_manager.scenes[GAME_SCENE].ui_components[1].reset_board()
            game_controller.reset_turn()
            game_controller.set_ai_player()
            scene_manager.scenes[GAME_SCENE].ui_components[1].winner = ""

        if current_scene.ui_components[2].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[MAIN_MENU_SCENE])

    if current_scene.name == "game_scene":
        if current_scene.ui_components[0].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[CHOOSE_OPPONENT_SCENE])
        game_board = current_scene.ui_components[1]
        run = game_controller.play(game_board, scene_manager, game_controller.ai_player, run)

    if current_scene.name == "rules_scene":
        if current_scene.ui_components[0].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[MAIN_MENU_SCENE])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    new_scene = scene_manager.get_current_scene()
    if new_scene != current_scene:
        SCREEN.blit(pygame.image.load(new_scene.background), (0, 0))
        scene_manager.draw_current_scene()

    pygame.display.update()

pygame.quit()
