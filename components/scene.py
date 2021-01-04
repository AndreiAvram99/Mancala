from typing import List


class Scene(object):
    def __init__(self, name, background):
        self.name = name
        self.ui_components = []
        self.background = background

    def remove_component(self, index):
        self.ui_components.pop(index)

    def add_component(self, component: object):
        self.ui_components.append(component)

    def add_components(self, components: List[object]):
        self.ui_components += components

    def draw_components(self):
        if len(self.ui_components) == 0:
            return -1

        for component in self.ui_components:
            component.draw_component()
        return 0
