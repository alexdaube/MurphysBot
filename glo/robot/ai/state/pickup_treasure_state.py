import time

from robot.ai.fine_movement_controller import FineMovementController
from robot.ai.state.move_to_island_state import MoveToIslandState
from robot.ai.state.robot_state import RobotState
from robot.hardware.hardware_controller import PrehensorController


class PickupTreasureState(RobotState):
    def __init__(self, controller, movement_controller=None, prehensor_controller=None):
        super(PickupTreasureState, self).__init__(controller)
        self.movement_controller = movement_controller or FineMovementController(controller.vision)
        self.prehensor_controller = prehensor_controller or PrehensorController()

    def handle(self):
        self.prehensor_controller.set_up_down('up')
        self.remote_logger.info("Moving Towards the treasure!")
        while not self.movement_controller.is_near_treasure() and self.run:
            self.movement_controller.move_towards_treasure()
        self.remote_logger.info("Putting prehensor down!")
        self.prehensor_controller.set_up_down('down')
        self.remote_logger.info("Setting up the magnet!")
        self.prehensor_controller.set_magnet(True)
        self.movement_controller.ram_it()
        time.sleep(1)
        self.movement_controller.back_away_slowly()
        self.prehensor_controller.set_up_down('up')
        self.next_state()

    def is_picked_up(self):
        is_picked_up = self.movement_controller.treasure_is_stuck()
        print is_picked_up
        return is_picked_up

    def next_state(self):
        if not self.run:
            self.prehensor_controller.set_up_down('up')
            self.prehensor_controller.set_magnet(False)
            return
        self.controller.set_state(MoveToIslandState)
        self.controller.activate()
