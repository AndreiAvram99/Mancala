from config import *
from scene_manager import SceneManager
from game_controller import GameController

pygame.init()

scene_manager = SceneManager()
game_controller = GameController()

run = True
while run:
    current_scene = scene_manager.get_current_scene()
    SCREEN.blit(pygame.image.load(current_scene.background), (0, 0))

    scene_manager.draw_current_scene()

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
        if current_scene.ui_components[1].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[GAME_SCENE])
        if current_scene.ui_components[2].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[MAIN_MENU_SCENE])

    if current_scene.name == "game_scene":
        if current_scene.ui_components[0].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[CHOOSE_OPPONENT_SCENE])

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                matrix_positions = game_controller.get_matrix_pos_from_mouse(pos)
                current_scene.ui_components[1].make_move(matrix_positions[0],
                                                         matrix_positions[1],
                                                         game_controller.turn)

                if not (current_scene.ui_components[1].last_hole == (0, 0)
                        or current_scene.ui_components[1].last_hole == (1, HOLES_PER_LINE - 1)):
                    game_controller.change_turn()

            if event.type == pygame.QUIT:
                run = False

    if current_scene.name == "settings_scene":
        if current_scene.ui_components[0].action_button:
            scene_manager.set_current_scene(scene_manager.scenes[MAIN_MENU_SCENE])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
