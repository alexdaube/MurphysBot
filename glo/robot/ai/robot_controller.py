import logging
from threading import Thread, Timer

import statistics as statistics

from common.map.decomposition_map.decomposition_map import DecompositionMap
from common.map.point_of_interest.island.island_factory import IslandFactory
from common.map.point_of_interest.point_of_interest_type import PointOfInterestType
from common.map.point_of_interest.treasure import Treasure
from common.map.position import Position
from robot.ai.state.stopped_state import StoppedState
from robot.ai.state_factory import StateFactory
from robot.communication.robot_client import RobotClient
from robot.vision.robot_vision import RobotVision


class RobotController:
    last_five_positions = []
    treasures = []
    position = {"x": 2000, "y": 461, "w": 180}
    island_description = PointOfInterestType.PENTAGON_ISLAND
    island_color = PointOfInterestType.GREEN_COLOR
    voltage = 0

    def __init__(self, client=None, vision=None, first_state=StoppedState, state_factory=None, pathfinding=None):
        self.robot_client = client or RobotClient()
        self.state_factory = state_factory or StateFactory()
        self.pathfinding = pathfinding or DecompositionMap(0, 0)
        self.vision = vision or RobotVision()
        self.current_state = self.state_factory.get_state(first_state, self)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.state_logger = logging.getLogger("RobotState")
        self.remote_logger = logging.getLogger("remote")

    def get_voltage(self):
        return self.voltage

    def activate(self):
        self.state_logger.warning("Activating {0}!".format(type(self.current_state).__name__))
        thread = Thread(target=self.current_state.handle, args=())
        thread.start()

    def set_state(self, state):
        if self.current_state and type(self.current_state) != state:
            self.state_logger.warning("Leaving {0}!".format(type(self.current_state).__name__))
        self.current_state.run = False
        self.current_state = self.state_factory.get_state(state, self)
        self.state_logger.info("Robot is now in {0}.".format(type(self.current_state).__name__))

    def inject_command(self, command):
        self.current_state.inject_command(command)

    def update_island_positions(self, positions):
        self.pathfinding = DecompositionMap(0, 0)
        for island in positions:
            average_point = self.vision.get_average_point(island["points"])
            poi = IslandFactory.create_island(island["POIType"], island["POIColor"],
                                              Position(average_point[0], average_point[1]))
            self.pathfinding.add_island(poi)
        self.logger.info("Controller Updated Island Positions")

    def add_treasures(self, treasure_positions, send=True):
        self.treasures = treasure_positions
        for treasure_position in treasure_positions:
            treasure = Treasure(Position(treasure_position[0], treasure_position[1]))
            self.remote_logger.info(
                "Treasure found at this position: X:{0}, Y:{1}".format(treasure.position.X, treasure.position.Y))
            self.pathfinding.add_treasure(treasure)
            if send:
                self.send_treasures(treasure_positions)

    def update_position(self, x, y, w):
        if x is None or y is None or w is None:
            return
        if len(self.last_five_positions) == 5:
            self.last_five_positions.pop(0)
        self.last_five_positions.append({"x": x, "y": y, "w": w})
        self.position["x"] = statistics.median([item["x"] for item in self.last_five_positions])
        self.position["y"] = statistics.median([item["y"] for item in self.last_five_positions])
        self.position["w"] = statistics.median([item["w"] for item in self.last_five_positions])
        self.logger.info('Controller Updated Robot pose')

    def set_destination(self, island_type):
        self.island_description = island_type
        for poi in self.pathfinding.point_of_interest_list:
            if poi.has_point_of_interest_type(island_type):
                self.island_description = poi.island_form
                self.island_color = poi.island_color

    def set_execution_states(self, state_list):
        self.state_factory.set_states_to_execute_in_order(state_list)

    def send_voltage(self, prehensor_controller):
        new_voltage = prehensor_controller.get_capacitor_tension()
        if new_voltage is None:
            return
        self.voltage = new_voltage
        try:
            self.robot_client.send_voltage({'voltage': self.voltage})
        except:
            pass
        Timer(0.8, self.send_voltage, [prehensor_controller]).start()

    def send_path(self, waypoints, destination):
        points = [[self.position["x"], self.position["y"]]]
        for i in range(len(waypoints)):
            points.append([waypoints[i].X, waypoints[i].Y])
        points.append([destination.X, destination.Y])
        self.robot_client.send_trajectory({'trajectory': points})

    def send_treasures(self, treasures):
        self.robot_client.send_treasures({'treasures': treasures})
