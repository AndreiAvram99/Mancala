import pygame

from config import SCREEN


class Scene:
    """ Scene docstring

        Description:
        _________
        This class deals with scenes drawing and add components

        Attributes:
        ---------
        name: `str`
            Scene name
        ui_components: `list`
            List of scene components
        background: `str`
            Path to background file

        PublicMethods:
        ---------
        remove_component(self, index)
        add_component(self, component: object)
        add_components(self, components: List[object])
        draw_components(self)
        """
    def __init__(self, name, background):
        self.name = name
        self.scene_components = []
        self.background = background

    def remove_component(self, index):
        """ Delete scene component at specified index
        :param index: `int`
            Index of the removed component
        :return:
        """
        self.scene_components.pop(index)

    def add_component(self, component):
        """ Add param component to the list with all components
        :param component:
            Added component
        :return:
        """
        self.scene_components.append(component)

    def add_components(self, components):
        """ Add a list of components to the list with all components
        :param components: `list`
            Added components
        :return:
        """
        self.scene_components += components

    def draw_components(self):
        """ Draw all the components of a list
        :return 0/-1:
            if length of the scene components list is 0 return -1(err)
            else return 0
        """
        SCREEN.blit(pygame.image.load(self.background), (0, 0))
        if len(self.scene_components) == 0:
            return -1

        for component in self.scene_components:
            component.draw_component()
        return 0
