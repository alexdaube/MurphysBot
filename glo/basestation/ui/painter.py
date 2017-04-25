# -*- coding: utf-8 -*-

import numpy as np
from PyQt4.QtCore import QPoint, QString
from PyQt4.QtGui import QPainter, QPen, QColor, QFont

from common.constants import TABLE_WIDTH


class Painter(object):
    def __init__(self):
        self.pen = QPen()
        self.pen.setWidth(5)
        self.font = QFont('arial', 10)
        self.wall = 0

    def __get_painter(self, image, color):
        painter = QPainter()
        self.pen.setColor(color)
        painter.begin(image)
        painter.setPen(self.pen)
        painter.setFont(self.font)
        return painter

    def draw_shapes(self, elems, image):
        image_ratio = float(image.width()) / float(TABLE_WIDTH)
        painter = self.__get_painter(image, QColor(204, 51, 0))
        painter.drawLine(0, elems["walls"][0] * image_ratio, image.width(), elems["walls"][0] * image_ratio)
        painter.drawLine(0, elems["walls"][1] * image_ratio, image.width(), elems["walls"][1] * image_ratio)
        self.wall = elems["walls"][0]
        if elems["islands"]:
            for shape in elems["islands"]:
                for point in shape["points"]:
                    painter.drawPoint(QPoint(point[0] * image_ratio,
                                             (point[1] + self.wall) * image_ratio))
                mid_point = np.array(shape["points"]).mean(axis=0).tolist()
                painter.drawText(QPoint(mid_point[0] * image_ratio, (mid_point[1] + self.wall) * image_ratio),
                                 QString(shape["type"] + " " + shape["color"]))

        self.draw_robot(elems, painter, image_ratio)

        painter.end()

    def draw_trajectory(self, trajectory, image, color):
        if trajectory is None:
            return
        image_ratio = float(image.width()) / float(TABLE_WIDTH)
        painter = self.__get_painter(image, color)
        for i in range(1, len(trajectory)):
            painter.drawLine(trajectory[i - 1][0] * image_ratio, (trajectory[i - 1][1] + self.wall) * image_ratio,
                             trajectory[i][0] * image_ratio, (trajectory[i][1] + self.wall) * image_ratio)

        painter.end()

    def draw_treasures(self, treasures, image):
        if treasures is None or len(treasures) == 0:
            return
        image_ratio = float(image.width()) / float(TABLE_WIDTH)
        painter = self.__get_painter(image, QColor(0, 0, 255))
        for treasure in treasures:
            painter.drawPoint(QPoint(treasure[0] * image_ratio, (treasure[1] + self.wall) * image_ratio))
            painter.drawText(QPoint(treasure[0] * image_ratio, (treasure[1] + self.wall) * image_ratio),
                             "holy treasure")
        painter.end()

    def draw_robot(self, elems, painter, image_ratio):
        if 'robot' in elems:
            robot = elems['robot']
            if 'x' in robot and 'y' in robot and 'w' in robot:
                painter.drawPoint(QPoint(robot['x'] * image_ratio, (robot['y'] + elems["walls"][0]) * image_ratio))
                painter.drawText(QPoint(robot['x'] * image_ratio, (robot['y'] + elems["walls"][0]) * image_ratio),
                                 QString('robot,' + str(robot['w'])))
