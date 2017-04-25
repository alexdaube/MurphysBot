import time

from robot.ai.fine_movement_controller import FineMovementController
from robot.ai.state.read_code_state import ReadCodeState
from robot.ai.state.robot_state import RobotState
from robot.hardware.hardware_controller import PrehensorController


class ChargeState(RobotState):
    CHARGED_VOLTAGE = 4.9
    CHARGING_RATE = 0.03

    def __init__(self, controller, movement_controller=None, prehensor_controller=None):
        super(ChargeState, self).__init__(controller)
        self.movement_controller = movement_controller or FineMovementController(controller.vision)
        self.prehensor_controller = prehensor_controller or PrehensorController()

    def handle(self):
        self.prehensor_controller.set_magnet(False)
        if not self.is_charged():
            self._move_to_recharge_station()
            self._align_to_recharge_station()
            self._recharge()
            self._step_back()

        self.next_state()

    def _move_to_recharge_station(self):
        self.remote_logger.info("Moving towards the charge station")
        self.movement_controller.move_towards_charge_station()
        self.movement_controller.ram_it()
        self.movement_controller.ram_it()
        self.movement_controller.ram_it()

    def _align_to_recharge_station(self):
        self.remote_logger.info("Aligning with recharge station")
        move_counter = 0
        while not self.is_charged() and not self.is_charging() and self.run:
            if move_counter < 5:
                self.movement_controller.fine_move_right()
            elif move_counter < 15:
                self.movement_controller.fine_move_left()
            else:
                move_counter = 0
            move_counter += 1
        self.remote_logger.info("Aligned and charging!")

    def _recharge(self):
        self.remote_logger.info("Starting the charge!")
        while not self.is_charged() and self.run:
            time.sleep(0.5)

    def _step_back(self):
        self.movement_controller.back_away_from_recharge_station()

    def is_charging(self):
        first_voltage = self.controller.get_voltage()
        time.sleep(1)
        second_voltage = self.controller.get_voltage()
        return second_voltage - first_voltage > self.CHARGING_RATE

    def is_charged(self):
        return self.controller.get_voltage() >= self.CHARGED_VOLTAGE

    def next_state(self):
        if not self.run:
            return
        self.controller.set_state(ReadCodeState)
        self.controller.activate()
