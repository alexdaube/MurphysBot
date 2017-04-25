import unittest

from mock import MagicMock, Mock

from robot.ai.state.charge_state import ChargeState
from robot.ai.state.read_code_state import ReadCodeState


class TestChargeState(unittest.TestCase):
    called_charged_times = 0
    called_charging_times = 0
    get_voltage_called_times = 0

    def one_not_charged(self):
        if self.called_charged_times == 0:
            self.called_charged_times += 1
            return False
        else:
            return True

    def three_not_charged(self):
        if self.called_charged_times < 3:
            self.called_charged_times += 1
            return False
        else:
            return True

    def three_not_charging(self):
        if self.called_charging_times < 3:
            self.called_charging_times += 1
            return False
        else:
            return True

    def multiple_not_charged(self):
        if self.called_charged_times < 7:
            self.called_charged_times += 1
            return False
        else:
            return True

    def multiple_not_charging(self):
        if self.called_charging_times < 6:
            self.called_charging_times += 1
            return False
        else:
            return True

    def increasing_voltage(self):
        if self.get_voltage_called_times < 1:
            self.get_voltage_called_times += 1
            return 0
        else:
            return 1

    def fixed_voltage(self):
        if self.get_voltage_called_times < 1:
            self.get_voltage_called_times += 1
            return 0
        else:
            return 0

    def setUp(self):
        self.controller = Mock()
        self.movement_controller = Mock()
        self.prehensor_controller = Mock()
        self.charge_state = ChargeState(self.controller, self.movement_controller, self.prehensor_controller)

    def test_is_charging_given_voltage_increasing(self):
        self.controller.get_voltage = self.increasing_voltage

        is_charging = self.charge_state.is_charging()

        self.assertTrue(is_charging)

    def test_is_charging_given_voltage_fixed(self):
        self.controller.get_voltage = self.fixed_voltage

        is_charging = self.charge_state.is_charging()

        self.assertFalse(is_charging)

    def test_calls_next_state_at_the_end(self):
        self.charge_state.is_charged = MagicMock()
        self.charge_state.is_charged.return_value = True
        self.charge_state.is_charging = MagicMock()
        self.charge_state.is_charged.return_value = True

        self.charge_state.handle()

        self.controller.set_state.assert_called_with(ReadCodeState)
        self.controller.activate.assert_called_with()

    def test_moves_towards_station_given_not_charging(self):
        self.charge_state.is_charged = self.one_not_charged

        self.charge_state.handle()

        self.movement_controller.move_towards_charge_station.assert_called_with()

    def test_fine_moves_on_the_right_given_not_charging(self):
        self.charge_state.is_charged = self.three_not_charged
        self.charge_state.is_charging = self.three_not_charging

        self.charge_state.handle()

        self.movement_controller.fine_move_right.assert_called_with()

    def tests_fine_moves_on_the_left_given_not_charging_given_completely_moved_to_the_right(self):
        self.charge_state.is_charged = self.multiple_not_charged
        self.charge_state.is_charging = self.multiple_not_charging

        self.charge_state.handle()

        self.movement_controller.fine_move_left.assert_called_with()

    def tests_steps_back_given_fully_charged(self):
        self.charge_state.is_charged = self.multiple_not_charged
        self.charge_state.is_charging = self.multiple_not_charging

        self.charge_state.handle()

        self.movement_controller.back_away_from_recharge_station.assert_called_with()
