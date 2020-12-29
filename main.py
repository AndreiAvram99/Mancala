from config import *
from scene_manager import SceneManager

pygame.init()

gm = SceneManager()

run = True
while run:
    current_scene = gm.get_current_scene()
    SCREEN.blit(pygame.image.load(current_scene.background), (0, 0))

    gm.draw_current_scene()

    if current_scene.name == "main_menu":
        if current_scene.ui_components[0].action_button:
            gm.set_current_scene(gm.scenes[CHOOSE_OPPONENT_SCENE])
        if current_scene.ui_components[1].action_button:
            gm.set_current_scene(gm.scenes[SETTINGS_SCENE])
        if current_scene.ui_components[2].action_button:
            run = False

    if current_scene.name == "choose_opponent":
        if current_scene.ui_components[0].action_button:
            gm.set_current_scene(gm.scenes[GAME_SCENE])
        if current_scene.ui_components[1].action_button:
            gm.set_current_scene(gm.scenes[GAME_SCENE])
        if current_scene.ui_components[2].action_button:
            gm.set_current_scene(gm.scenes[MAIN_MENU_SCENE])

    if current_scene.name == "game_scene":
        if current_scene.ui_components[0].action_button:
            gm.set_current_scene(gm.scenes[CHOOSE_OPPONENT_SCENE])

    if current_scene.name == "settings_scene":
        if current_scene.ui_components[0].action_button:
            gm.set_current_scene(gm.scenes[MAIN_MENU_SCENE])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
