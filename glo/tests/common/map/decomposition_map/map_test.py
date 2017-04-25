#!/usr/bin/python2
# -*- coding: utf-8 -*-
import sys
import time

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QImage

from common import constants
from common.map.decomposition_map.decomposition_map import DecompositionMap
from common.map.decomposition_map.decomposition_map_qt_drawer import DecompositionMapQtDrawer
from common.map.point_of_interest.island.island_factory import IslandFactory
from common.map.point_of_interest.point_of_interest_type import PointOfInterestType
from common.map.point_of_interest.recharge_station import RechargeStation
from common.map.point_of_interest.treasure import Treasure
from common.map.position import Position
from tests.common.map.decomposition_map.path_drawer import PathDrawer


class ImageGeneratorMainWindow(QtGui.QMainWindow):
    image_area = None
    image_pixmap = None
    image_label = None
    map_drawer = None
    path_drawer = None
    objective = None
    pathway = None
    robot_position = None

    def __init__(self, map_drawer, path_drawer, objective, pathway, robot_position):
        super(ImageGeneratorMainWindow, self).__init__()
        self.image_area = QtGui.QScrollArea()
        self.map_drawer = map_drawer
        self.path_drawer = path_drawer
        self.objective = objective
        self.pathway = pathway
        self.robot_position = robot_position
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Test image generator')
        self.resize(700, 700)
        self.init_menu()
        self.init_layout()
        self.show()

    def init_menu(self):
        exit_action = QtGui.QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit')
        exit_action.triggered.connect(self.close)
        menu = self.menuBar()
        file_menu = menu.addMenu('&File')
        file_menu.addAction(exit_action)

        save_map = QtGui.QAction('Export map to PNG', self)
        save_map.setShortcut('Ctrl+S')
        save_map.setStatusTip('Save the current map and path to a png')
        save_map.triggered.connect(self.connect_save_map_image)
        file_menu.addAction(save_map)

    def init_layout(self):
        main_layout = QtGui.QGridLayout()
        action_menu_layout = QtGui.QVBoxLayout()
        cwidget = QtGui.QWidget()
        cwidget.setLayout(main_layout)
        self.setCentralWidget(cwidget)
        action_menu_widget = QtGui.QWidget()
        action_menu_widget.setLayout(action_menu_layout)
        main_layout.addWidget(action_menu_widget, 1, 0)

        self.image_area.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.image_area, 1, 1)

        self.image_label = QtGui.QLabel()
        self.draw_map()
        self.image_area.setWidget(self.image_label)

    def draw_map(self):
        image = QImage(constants.TABLE_WIDTH + 1, constants.TABLE_HEIGHT + 1, QImage.Format_RGB32)
        self.image_pixmap = QtGui.QPixmap.fromImage(image)
        painter = QtGui.QPainter(self.image_pixmap)
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor("white"))
        painter.setPen(pen)
        self.map_drawer.draw_map(painter)
        self.path_drawer.draw_path(painter, self.robot_position, self.pathway, self.objective)
        self.image_label.setPixmap(self.image_pixmap)

        del painter
        self.image_label.update()

    def connect_save_map_image(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, "Save file", "map.png", ".png")
        if filename is not None:
            self.image_pixmap.save(filename, "PNG")


def main():
    map = DecompositionMap(0, 0, base_horizontal_cell_count=5, base_vertical_cell_count=10)
    island_factory = IslandFactory()

    # island out of map
    island1 = island_factory.create_island(PointOfInterestType.CIRCLE_ISLAND, PointOfInterestType.RED_COLOR,
                                           Position(2200, 2000))
    # island out of map
    island2 = island_factory.create_island(PointOfInterestType.TRIANGLE_ISLAND, PointOfInterestType.YELLOW_COLOR,
                                           Position(1360, 1260))

    island3 = island_factory.create_island(PointOfInterestType.PENTAGON_ISLAND, PointOfInterestType.GREEN_COLOR,
                                           Position(1850, 400))

    island4 = island_factory.create_island(PointOfInterestType.SQUARE_ISLAND, PointOfInterestType.BLUE_COLOR,
                                           Position(709, 1000))

    island5 = island_factory.create_island(PointOfInterestType.SQUARE_ISLAND, PointOfInterestType.RED_COLOR,
                                           Position(1200, 680))

    island6 = island_factory.create_island(PointOfInterestType.PENTAGON_ISLAND, PointOfInterestType.YELLOW_COLOR,
                                           Position(70, 500))

    island7 = island_factory.create_island(PointOfInterestType.TRIANGLE_ISLAND, PointOfInterestType.GREEN_COLOR,
                                           Position(70, 400))

    island8 = island_factory.create_island(PointOfInterestType.CIRCLE_ISLAND, PointOfInterestType.BLUE_COLOR,
                                           Position(1400, 10))

    treasure = Treasure(Position(constants.TABLE_WIDTH, constants.TABLE_HEIGHT / 3))

    treasure2 = Treasure(Position(constants.TABLE_WIDTH, constants.TABLE_HEIGHT * 2 / 3))

    recharge_station = RechargeStation(Position(350, constants.TABLE_HEIGHT))

    robot_position = Position(250, 250)

    map.add_treasure(treasure)
    map.add_treasure(treasure2)

    map.add_recharge_station(recharge_station)

    print("island 1")
    map.add_island(island1)
    print("island 2")
    map.add_island(island2)
    print("island 3")
    map.add_island(island3)
    print("island 4")
    map.add_island(island4)
    print("island 5")
    map.add_island(island5)
    print("island 6")
    map.add_island(island6)
    print("island 7")
    map.add_island(island7)
    print("island 8")
    map.add_island(island8)

    start = time.clock()
    print(start)
    # pathway, objective = map.calculate_dijkstra_path(robot_position, PointOfInterestType.TREASURE)
    # pathway, objective = map.calculate_dijkstra_path(robot_position, PointOfInterestType.CIRCLE_ISLAND)
    pathway, objective = map.calculate_dijkstra_path(robot_position, PointOfInterestType.RECHARGE_STATION)
    # pathway, objective = None, None
    end = time.clock()
    print(end)
    print(end - start)

    path_drawer = PathDrawer()
    map_drawer = DecompositionMapQtDrawer(map)
    app = QtGui.QApplication(sys.argv)
    w = ImageGeneratorMainWindow(map_drawer, path_drawer, objective, pathway, robot_position)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
