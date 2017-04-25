import time

from common.map.position import Position
from robot.ai.broad_movement_controller import BroadMovementController
from robot.ai.state.drop_treasure_state import DropTreasureState
from robot.ai.state.robot_state import RobotState


class MoveToIslandState(RobotState):
    island_position = Position(0, 0)
    threshold = 400

    def __init__(self, controller, movement_controller=None):
        super(MoveToIslandState, self).__init__(controller)
        self.movement_controller = movement_controller or BroadMovementController()

    def handle(self):
        self.waypoints, self.island_position = self.controller.pathfinding.calculate_dijkstra_path(
            Position(self.controller.position["x"], self.controller.position["y"]),
            self.controller.island_description)
        self.controller.send_path(self.waypoints, self.island_position)
        while not self.has_arrived() and self.run:
            time.sleep(0.1)
            print "Move to island loop"
            self.movement_controller.move(self.island_position, self.waypoints, self.controller.position)
        self.movement_controller.face_point(self.island_position, self.controller.position)
        self.next_state()

    def has_arrived(self):
        return self.movement_controller.is_at_position(self.controller.position, self.island_position, self.threshold)

    def next_state(self):
        if not self.run:
            return
        self.controller.set_state(DropTreasureState)
        self.controller.activate()
