from common.map.decomposition_map.decomposition_cell_qt_drawer import DecompositionCellQtDrawer
from common.map.map_drawer import MapDrawer


class DecompositionMapQtDrawer(MapDrawer):
    mymap = None
    cell_drawer = None

    def __init__(self, decomposition_map, decomposition_cell_drawer=DecompositionCellQtDrawer()):
        self.mymap = decomposition_map
        self.cell_drawer = decomposition_cell_drawer

    def draw_map(self, painter):
        self.__draw_line(painter, self.mymap.origin_x, self.mymap.origin_y, self.mymap.origin_x + self.mymap.size_x,
                         self.mymap.origin_y)
        self.__draw_line(painter, self.mymap.origin_x + self.mymap.size_x, self.mymap.origin_y,
                         self.mymap.origin_x + self.mymap.size_x, self.mymap.origin_y + self.mymap.size_y)
        self.__draw_line(painter, self.mymap.origin_x + self.mymap.size_x, self.mymap.origin_y + self.mymap.size_y,
                         self.mymap.origin_x, self.mymap.origin_y + self.mymap.size_y)
        self.__draw_line(painter, self.mymap.origin_x, self.mymap.origin_y + self.mymap.size_y, self.mymap.origin_x,
                         self.mymap.origin_y)
        for cell in self.mymap.get_cell_list():
            self.cell_drawer.draw_cell(cell, painter)

    def __draw_line(self, painter, x1, y1, x2, y2):
        painter.drawLine(x1, y1, x2, y2)
