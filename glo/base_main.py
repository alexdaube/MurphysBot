# coding=utf-8
import json
import math
import sys
import time
from Queue import Queue

import yaml
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QImage, QColor
from flask import Flask

from basestation.communication.base_station_api import BaseStationAPI
from basestation.communication.base_station_client import BaseStationClient
from basestation.ui.main_window import MainWindow
from basestation.ui.message_formatter import MessageFormatter
from basestation.ui.painter import Painter
from basestation.vision.island_detector import IslandDetector
from basestation.vision.robot_detector import RobotDetector
from basestation.vision.world_number_of_sides_island_strategy import WorldNumberOfSidesIslandStrategy
from basestation.vision.world_vision import WorldVision
from common.logger.logging_setup import configure_root_logger, configure_qt_logger, set_qt_loggers_level
from common.vision.camera_retrieve import CameraRetrieve
from common.vision.dot_pattern_detection_strategy import DotPatternDetectionStrategy


class MainWorker(QtCore.QThread):
    time_started = sys.maxint
    robot_pos = []

    def __init__(self, world_vision, painter, queue, updated_values):
        super(MainWorker, self).__init__()
        self.world_vision = world_vision
        self.painter = painter
        self.message_queue = queue
        self.updated_values = updated_values
        self.client = None
        self.running = False

    def run(self):
        self.running = True

        while self.running:
            time.sleep(0.1)
            self.display_information()

        self.terminate()

    def display_information(self):
        frame = self.world_vision.get_image()
        elems = self.world_vision.detect_elements()
        self.send_elements(elems)
        image = QImage(frame.tostring(), frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
        self.painter.draw_shapes(elems, image)
        self.add_robot_pos(elems["robot"])
        self.painter.draw_trajectory(self.robot_pos, image, QColor(0, 255, 0))
        self.painter.draw_trajectory(self.updated_values['trajectory'], image, QColor(255, 0, 0))
        self.painter.draw_treasures(self.updated_values['treasures'], image)
        self.emit(QtCore.SIGNAL('set_image(QImage)'), image)
        self.emit(QtCore.SIGNAL('set_voltage'), self.updated_values['voltage'])
        self.emit(QtCore.SIGNAL('set_letter'), self.updated_values['letter'])
        self.emit(QtCore.SIGNAL('set_description'), self.updated_values['description'])
        self.emit(QtCore.SIGNAL('set_time'), self.time_started)
        self.emit(QtCore.SIGNAL('set_robot_position'), elems["robot"])
        while not self.message_queue.empty():
            self.emit(QtCore.SIGNAL('add_message'), MessageFormatter.get_message(self.message_queue.get()))

    def add_robot_pos(self, robot):
        count = len(self.robot_pos)
        if len(robot) == 0:
            return
        if count == 0 or math.fabs(self.robot_pos[count - 1][0] - robot["x"]) > 5 \
                and math.fabs(self.robot_pos[count - 1][1] - robot["y"]) > 5:
            self.robot_pos.append([robot["x"], robot["y"]])

    def stop(self):
        self.running = False

    def send_elements(self, elems, send_islands=False):
        if self.client is not None:
            try:
                self.client.send_robot_position(json.dumps(elems["robot"]))
                if send_islands:
                    self.client.send_island_positions(json.dumps(elems["islands"]))
            except:
                self.message_queue.put(("warning", "Failed sending elements"))

    def start_robot_execution(self, ip):
        self.robot_pos = []
        self.client = BaseStationClient()
        try:
            elems = self.world_vision.detect_elements()
            self.send_elements(elems, True)
            answer = self.client.start_robot_execution()
            return answer.status_code == 200
        except:
            self.message_queue.put(("critical", "Connection failed: " + ip))
            self.client = None
            return False

    def start_robot_execution_with_state_list(self, ip, state_list):
        self.robot_pos = []
        self.client = BaseStationClient()
        try:
            elems = self.world_vision.detect_elements()
            self.send_elements(elems, True)
            answer = self.client.start_robot_execution_with_state_list({'states': state_list})
            return answer.status_code == 200
        except:
            self.message_queue.put(("critical", "Connection failed: " + ip))
            self.client = None
            return False

    def send_command(self, command):
        if self.client is not None:
            try:
                answer = self.client.send_command(command)
                return answer.status_code == 200
            except:
                self.message_queue.put(("warning", "Failed to send command"))


def main():
    qt_message_queue = Queue()
    updated_values = {'letter': "-", 'description': "-", 'voltage': 0.0, 'trajectory': None, 'treasures': None}
    configure_root_logger("base_station")
    configure_qt_logger(qt_message_queue)
    set_qt_loggers_level()
    app = QtGui.QApplication(sys.argv)

    # 0 => Laptop Camera
    # 1 => USB
    camera = CameraRetrieve(1)
    camera.start()

    f = open('./data/robot_pattern.yml')
    dot_pattern = yaml.safe_load(f)
    f.close()
    f = open('./data/pattern_colors.yml')
    dot_colors = yaml.safe_load(f)
    f.close()

    dot_pattern_detection = DotPatternDetectionStrategy(dot_pattern, dot_colors)
    robot_detector = RobotDetector(dot_pattern_detection)
    island_detector = IslandDetector(WorldNumberOfSidesIslandStrategy())
    world_vision = WorldVision(camera, robot_detector, island_detector)

    main_worker = MainWorker(world_vision, Painter(), qt_message_queue, updated_values)
    main_window = MainWindow(main_worker)

    main_worker.start()
    api = BaseStationAPI(Flask("BaseStationAPI"), updated_values)
    api.run(port=8000)

    app.exec_()
    main_worker.stop()
    camera.stop()
    api.stop()
    sys.exit()


if __name__ == "__main__":
    main()
