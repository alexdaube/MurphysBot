import time

from common.constants import TABLE_HEIGHT
from common.map.point_of_interest.point_of_interest_type import PointOfInterestType
from common.map.position import Position
from robot.ai.broad_movement_controller import BroadMovementController
from robot.ai.state.pickup_treasure_state import PickupTreasureState
from robot.ai.state.robot_state import RobotState


class MoveToTreasureState(RobotState):
    treasure_position = Position(0, 0)
    threshold = 50

    def __init__(self, controller, movement_controller=None):
        super(MoveToTreasureState, self).__init__(controller)
        self.movement_controller = movement_controller or BroadMovementController()

    def handle(self):
        self.waypoints, self.treasure_position = self.controller.pathfinding.calculate_dijkstra_path(
            Position(self.controller.position["x"], self.controller.position["y"]),
            PointOfInterestType.TREASURE)
        self.controller.send_path(self.waypoints, self.treasure_position)
        while not self.has_arrived() and self.run:
            time.sleep(0.1)
            print "Move to treasure loop"
            self.movement_controller.move(self.treasure_position, self.waypoints, self.controller.position)
        wall = 'back'
        if self.treasure_position.Y == 0:
            wall = 'top'
        elif self.treasure_position.Y == TABLE_HEIGHT:
            wall = 'bottom'
        self.movement_controller.face_wall(wall, self.controller.position)
        self.next_state()

    def has_arrived(self):
        return self.movement_controller.is_at_position(self.controller.position, self.treasure_position, self.threshold)

    def next_state(self):
        if not self.run:
            return
        self.controller.set_state(PickupTreasureState)
        self.controller.activate()
