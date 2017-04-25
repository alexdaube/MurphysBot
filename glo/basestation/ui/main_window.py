import math
import time

from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtGui import QMainWindow

from basestation.communication import addresses
from basestation.ui.robot_commander import RobotCommanderQDialog
from basestation.ui.state_selector import StateSelectorQDialog


class MainWindow(QMainWindow):
    def __init__(self, main_worker):
        super(MainWindow, self).__init__()
        uic.loadUi("basestation/ui/ui_mainwindow.ui", self)
        self.main_worker = main_worker
        self.show()
        self.connect(self.main_worker, QtCore.SIGNAL('set_image(QImage)'), self.set_image)
        self.connect(self.main_worker, QtCore.SIGNAL('set_voltage'), self.set_voltage)
        self.connect(self.main_worker, QtCore.SIGNAL('set_letter'), self.set_letter)
        self.connect(self.main_worker, QtCore.SIGNAL('set_description'), self.set_description)
        self.connect(self.main_worker, QtCore.SIGNAL('set_time'), self.set_time)
        self.connect(self.main_worker, QtCore.SIGNAL('add_message'), self.add_message)
        self.connect(self.main_worker, QtCore.SIGNAL('set_robot_position'), self.set_robot_position)
        self.txb_robot_ip.textChanged.connect(self.update_address)
        self.btn_start.clicked.connect(self.start)
        menu = QtGui.QMenu()
        menu.addAction('Start', self.start)
        menu.addAction('Start with execution state list', self.start_with_execution_state)
        menu.addAction('Start robot commander mode', self.start_robot_commander)
        self.btn_start.setMenu(menu)
        self.btn_reset_islands.clicked.connect(self.reset_islands)

        self.status_bar_label = QtGui.QLabel()
        self.statusBar().addPermanentWidget(self.status_bar_label)
        self.robot_x = '0'
        self.robot_y = '0'
        self.robot_w = '0'
        message = "robot: (0, 0, 0)"
        self.status_bar_label.setText(message)

        self.main_worker.start()

    def reset_islands(self):
        self.main_worker.world_vision.islands = None

    def start(self):
        print "start"
        if self.main_worker.start_robot_execution(self.txb_robot_ip.text()):
            self.main_worker.time_started = time.time()

    def start_with_execution_state(self):
        print "start with state"
        result, states_list = StateSelectorQDialog.get_states_to_execute(self)
        if result:
            print states_list
            if self.main_worker.start_robot_execution_with_state_list(self.txb_robot_ip.text(), states_list):
                self.main_worker.time_started = time.time()

    def start_robot_commander(self):
        RobotCommanderQDialog.stat_robot_commander(self, self.main_worker, self.txb_robot_ip.text())

    def set_time(self, time_started):
        if time_started > time.time():
            return
        diff = time.time() - time_started
        minutes = int(math.floor(diff / 60))
        seconds = int(diff - minutes * 60)
        self.lbl_timer.setText(str(minutes) + "m" + str(seconds) + "s")

    def set_image(self, image):
        self.lbl_image.setPixmap(QtGui.QPixmap.fromImage(image))

    def set_voltage(self, voltage):
        self.lbl_voltage.setText(str(voltage) + "V")

    def set_letter(self, letter):
        self.lbl_letter.setText(letter)

    def set_description(self, destination):
        self.lbl_description.setText(destination)

    def set_robot_position(self, position):
        if 'x' in position:
            self.robot_x = str(round(position['x'], 1))
        if 'y' in position:
            self.robot_y = str(round(position['y'], 1))
        if 'w' in position:
            self.robot_w = str(round(position['w'], 1))
        message = "robot: (" + self.robot_x + ", " + self.robot_y + ", " + self.robot_w + ")"
        self.status_bar_label.setText(message)

    def add_message(self, message):
        self.txb_messages.append(self.lbl_timer.text() + ": " + message)
        self.txb_messages.verticalScrollBar().setValue(self.txb_messages.verticalScrollBar().maximum())

    def update_address(self):
        addresses.ROBOT_ADDRESS = self.txb_robot_ip.text()
