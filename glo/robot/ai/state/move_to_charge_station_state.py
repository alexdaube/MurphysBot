import time

from common.map.point_of_interest.point_of_interest_type import PointOfInterestType
from common.map.point_of_interest.recharge_station import RechargeStation
from common.map.position import Position
from robot.ai.broad_movement_controller import BroadMovementController
from robot.ai.state.charge_state import ChargeState
from robot.ai.state.robot_state import RobotState


class MoveToChargeStationState(RobotState):
    charge_station_position = Position(2100, 400)
    threshold = 50

    def __init__(self, controller, movement_controller=None):
        super(MoveToChargeStationState, self).__init__(controller)
        self.movement_controller = movement_controller or BroadMovementController()

    def handle(self):
        self.controller.pathfinding.add_recharge_station(RechargeStation(self.charge_station_position))
        self.waypoints, self.charge_station_position = self.controller.pathfinding.calculate_dijkstra_path(
            Position(self.controller.position["x"], self.controller.position["y"]),
            PointOfInterestType.RECHARGE_STATION)
        self.controller.send_path(self.waypoints, self.charge_station_position)
        while not self.has_arrived() and self.run:
            time.sleep(0.1)
            print "Move to charge station loop"
            self.movement_controller.move(self.charge_station_position, self.waypoints, self.controller.position)
        self.movement_controller.face_wall('top', self.controller.position)
        self.next_state()

    def has_arrived(self):
        return self.movement_controller.is_at_position(self.controller.position, self.charge_station_position,
                                                       self.threshold)

    def next_state(self):
        if not self.run:
            return
        self.controller.set_state(ChargeState)
        self.controller.activate()
