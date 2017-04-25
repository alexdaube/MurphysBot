from Queue import Queue

from robot.ai.broad_movement_controller import BroadMovementController
from robot.ai.state.robot_state import RobotState
from robot.ai.state.stopped_state import StoppedState
from robot.hardware.hardware_controller import PrehensorController, CameraController


class CommandInjectionState(RobotState):
    command_queue = Queue()

    def __init__(self, controller, movement_controller=None,
                 prehensor_controller=None, camera_controller=None):
        super(CommandInjectionState, self).__init__(controller)
        self.movement_controller = movement_controller or BroadMovementController()
        self.prehensor_controller = prehensor_controller or PrehensorController()
        self.camera_controller = camera_controller or CameraController()

    def inject_command(self, command):
        self.command_que.put(command)

    def handle(self):
        while self.run:
            if not self.command_queue.empty():
                self.run_command(self.command_queue.get())
        self.next_state()

    def next_state(self):
        if not self.run:
            return
        self.controller.set_state(StoppedState)
        self.controller.activate()

    def run_command(self, command):
        if command['command'] == "quit":
            self.run = False
        elif command['command'] == "magnet":
            self._run_magnet_command(command["enable"])
        elif command['command'] == "prehensor":
            self._run_prehensor_command(command["position"])
        elif command['command'] == "move_camera":
            self._run_move_camera_command(command["vertical_angle"], command["horizontal_angle"])
        elif command['command'] == "move_robot":
            self._run_move_robot_command(command["x"], command["y"])

    def _run_magnet_command(self, enable):
        if enable:
            self.prehensor_controller.set_magnet(True)
        else:
            self.prehensor_controller.set_magnet(False)

    def _run_prehensor_command(self, position):
        if position == "down":
            self.prehensor_controller.set_up_down('down')
        else:
            self.prehensor_controller.set_up_down('up')

    def _run_move_camera_command(self, vertical_angle, horizontal_angle):
        self.camera_controller.set_orientation(vertical_angle, horizontal_angle)

    def _run_move_robot_command(self, x, y):
        self._run_move_robot_command(x, y)
