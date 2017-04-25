import requests

import addresses
from common.communication.base_client import BaseClient


class BaseStationClient(BaseClient):
    START_ROBOT_PATH = "start_robot"
    START_ROBOT_WITH_STATES_TO_EXECUTE_LIST_PATH = "start_robot_with_execution_states"
    ROBOT_POSITION_PATH = "robot_position"
    ISLAND_POSITIONS_PATH = "island_positions"
    SEND_COMMAND = "send_command"

    def start_robot_execution(self):
        return requests.post(self._url(addresses.ROBOT_ADDRESS, addresses.ROBOT_PORT, self.START_ROBOT_PATH), timeout=2)

    def start_robot_execution_with_state_list(self, state_list):
        return requests.put(self._url(addresses.ROBOT_ADDRESS, addresses.ROBOT_PORT,
                                      self.START_ROBOT_WITH_STATES_TO_EXECUTE_LIST_PATH),
                            json=state_list, timeout=2)

    def send_robot_position(self, position):
        return requests.put(self._url(addresses.ROBOT_ADDRESS, addresses.ROBOT_PORT, self.ROBOT_POSITION_PATH),
                            json=position,
                            timeout=2)

    def send_island_positions(self, positions):
        return requests.put(self._url(addresses.ROBOT_ADDRESS, addresses.ROBOT_PORT, self.ISLAND_POSITIONS_PATH),
                            json=positions,
                            timeout=2)

    def send_command(self, command):
        return requests.put(self._url(addresses.ROBOT_ADDRESS, addresses.ROBOT_PORT, self.SEND_COMMAND),
                            json=command,
                            timeout=2)
