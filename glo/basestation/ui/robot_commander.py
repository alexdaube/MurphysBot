from PyQt4 import uic
from PyQt4.QtGui import QDialog, QMessageBox, QIntValidator


class RobotCommanderQDialog(QDialog):
    main_worker = None

    def __init__(self, parent=None, main_worker=None):
        super(RobotCommanderQDialog, self).__init__(parent)
        self.main_worker = main_worker
        uic.loadUi("basestation/ui/ui_robot_commander.ui", self)
        self.magnet_off_radiobutton.toggled.connect(self.disable_magnet)
        self.magnet_on_radiobutton.toggled.connect(self.enable_magnet)
        self.prehensor_up_radiobutton.toggled.connect(self.prehensor_up)
        self.prehensor_down_radiobutton.toggled.connect(self.prehensor_down)
        self.servomotor_vertical_angle_slider.valueChanged.connect(self.vertical_angle)
        self.servomotor_horizontal_angle_slider.valueChanged.connect(self.horizontal_angle)
        self.send_move_command_button.clicked.connect(self.send_move_command)
        self.send_rotate_command_button.clicked.connect(self.send_rotate_command)
        angle_validator = QIntValidator(-360, 360, self)
        self.angle_move_edit.setValidator(angle_validator)
        move_validator = QIntValidator(-2000, 2000, self)
        self.x_move_edit.setValidator(move_validator)
        self.y_move_edit.setValidator(move_validator)

    @staticmethod
    def stat_robot_commander(parent=None, main_worker=None, robot_ip=None):
        main_worker.start_robot_execution_with_state_list(robot_ip, ["CommandInjectionState"])
        dialog = RobotCommanderQDialog(parent, main_worker)
        dialog.exec_()
        command = dict()
        command["command"] = "quit"
        main_worker.send_command(command)

    def enable_magnet(self):
        if self.magnet_on_radiobutton.checked():
            command = dict()
            command["command"] = "magnet"
            command["enable"] = True
            self.main_worker.send_command(command)

    def disable_magnet(self):
        if self.magnet_off_radiobutton.checked():
            command = dict()
            command["command"] = "magnet"
            command["enable"] = False
            self.main_worker.send_command(command)

    def prehensor_up(self):
        if self.prehensor_up_radiobutton.checked():
            command = dict()
            command["command"] = "prehensor"
            command["position"] = "up"
            self.main_worker.send_command(command)

    def prehensor_down(self):
        if self.prehensor_down_radiobutton.checked():
            command = dict()
            command["command"] = "prehensor"
            command["position"] = "down"
            self.main_worker.send_command(command)

    def vertical_angle(self, vertical_angle):
        command = dict()
        command["command"] = "move_camera"
        command["vertical_angle"] = vertical_angle
        command["horizontal_angle"] = self.servomotor_horizontal_angle_slider.value()
        self.main_worker.send_command(command)

    def horizontal_angle(self, horizontal_angle):
        command = dict()
        command["command"] = "move_camera"
        command["vertical_angle"] = self.servomotor_vertical_angle_slider.value()
        command["horizontal_angle"] = horizontal_angle
        self.main_worker.send_command(command)

    def send_move_command(self):
        command = dict()
        if self.x_move_edit.text() != '' and self.y_move_edit.text() != '':
            command["x"] = int(self.x_move_edit.text())
            command["y"] = int(self.y_move_edit.text())
        if len(command) != 0:
            command["command"] = "move_robot"
            self.main_worker.send_command(command)
        else:
            message_box = QMessageBox(self)
            message_box.setText("Must provide x and y coordinate")
            message_box.exec_()

    def send_rotate_command(self):
        command = dict()
        if self.angle_move_edit.text() != '':
            command["angle"] = int(self.angle_move_edit.text())
        if len(command) != 0:
            command["command"] = "move_robot"
            self.main_worker.send_command(command)
        else:
            message_box = QMessageBox(self)
            message_box.setText("Must provide angle")
            message_box.exec_()
