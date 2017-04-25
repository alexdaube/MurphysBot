from PyQt4.QtCore import QPoint, Qt

from common.map.decomposition_map.decomposition_cell_drawer import DecompositionCellDrawer


class DecompositionCellQtDrawer(DecompositionCellDrawer):
    def draw_cell(self, cell, painter):
        top_left = QPoint(cell.top_left.X, cell.top_left.Y)
        top_right = QPoint(cell.top_right.X, cell.top_right.Y)
        bottom_right = QPoint(cell.bottom_right.X, cell.bottom_right.Y)
        bottom_left = QPoint(cell.bottom_left.X, cell.bottom_left.Y)

        painter.setBrush(Qt.gray)
        painter.drawConvexPolygon(top_left, top_right, bottom_right, bottom_left)
