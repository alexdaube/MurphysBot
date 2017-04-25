from abc import ABCMeta, abstractmethod


class DecompositionCellDrawer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def draw_cell(self, cell, painter):
        pass
