from PyQt4 import QtCore
from PyQt4.QtGui import QPen, QColor


class PathDrawer(object):
    def draw_path(self, painter, robot, waypoints, ojective):
        self.__draw_robot(painter, robot)
        previous = robot
        for position in waypoints:
            self.__draw_position(painter, position)
            self.__draw_path(painter, previous, position)
            previous = position
        self.__draw_objective(painter, ojective)

    def __draw_path(self, painter, position1, position2):
        current_pen = painter.pen()
        pen = QPen()
        pen.setColor(QColor('red'))
        painter.setPen(pen)
        painter.drawLine(position1.X, position1.Y, position2.X, position2.Y)
        painter.setPen(current_pen)

    def __draw_objective(self, painter, position):
        current_pen = painter.pen()
        pen = QPen()
        pen.setColor(QColor('green'))
        painter.setPen(pen)
        qpoint = QtCore.QPoint(position.X, position.Y)
        painter.drawEllipse(qpoint, 5, 5)
        painter.setPen(current_pen)

    def __draw_robot(self, painter, position):
        current_pen = painter.pen()
        pen = QPen()
        pen.setColor(QColor('brown'))
        painter.setPen(pen)
        qpoint = QtCore.QPoint(position.X, position.Y)
        painter.drawEllipse(qpoint, 8, 8)
        painter.setPen(current_pen)

    def __draw_position(self, painter, position):
        current_pen = painter.pen()
        pen = QPen()
        pen.setColor(QColor('yellow'))
        painter.setPen(pen)
        qpoint = QtCore.QPoint(position.X, position.Y)
        painter.drawEllipse(qpoint, 5, 5)
        painter.setPen(current_pen)
