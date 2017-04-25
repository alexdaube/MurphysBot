from robot.ai.fine_movement_controller import FineMovementController
from robot.ai.state.robot_state import RobotState
from robot.ai.state.stopped_state import StoppedState
from robot.hardware.hardware_controller import PrehensorController


class DropTreasureState(RobotState):
    def __init__(self, controller, movement_controller=None, prehensor_controller=None):
        super(DropTreasureState, self).__init__(controller)
        self.movement_controller = movement_controller or FineMovementController(controller.vision)
        self.prehensor_controller = prehensor_controller or PrehensorController()

    def handle(self):
        while not self.movement_controller.is_aligned_with_island(self.controller.island_color) and self.run:
            self.movement_controller.fall_into_line_with_island(self.controller.island_description,
                                                                self.controller.island_color)
        self.remote_logger.info("Dropping the treasure!")
        self.prehensor_controller.set_up_down('down')
        self.prehensor_controller.set_magnet(False)
        self.prehensor_controller.set_up_down('up')
        self.movement_controller.back_away()
        self.movement_controller.spaz_out()
        self.remote_logger.warning("WINNING!")
        self.next_state()

    def next_state(self):
        if not self.run:
            return
        self.controller.set_state(StoppedState)
        self.controller.activate()
