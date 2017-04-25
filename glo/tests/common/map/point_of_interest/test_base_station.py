import unittest

from mock.mock import Mock

from common.map.point_of_interest.point_of_interest_type import PointOfInterestType
from common.map.point_of_interest.recharge_station import RechargeStation


class TestBaseStation(unittest.TestCase):
    recharge_station = None
    recharge_station_position = Mock()

    def setUp(self):
        self.recharge_station = RechargeStation(self.recharge_station_position)

    def test_get_position_return_position(self):
        self.assertEqual(self.recharge_station_position, self.recharge_station.get_position())

    def test_has_point_of_interest_type_with_base_station_type_return_true(self):
        self.assertTrue(self.recharge_station.has_point_of_interest_type(PointOfInterestType.RECHARGE_STATION))

    def test_has_point_of_interest_type_with_other_type_than_base_station_type_return_false(self):
        self.assertFalse(self.recharge_station.has_point_of_interest_type(PointOfInterestType.TREASURE))
