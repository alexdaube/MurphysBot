import requests

import addresses
from common.communication.base_client import BaseClient


class RobotClient(BaseClient):
    CODE_QUERY_PATH = '?code='
    ISLAND_API_PROTOCOL = 'https'
    VOLTAGE_PATH = 'voltage'
    TRAJECTORY_PATH = 'trajectory'
    TREASURES_PATH = 'treasures'
    DESTINATION_PATH = 'destination'
    LOG_PATH = 'log'
    COLOR_ACCESSOR = 'couleur'
    FORM_ACCESSOR = 'forme'

    def send_voltage(self, voltage):
        return requests.put(self._url(addresses.BASE_STATION_ADDRESS, addresses.BASE_STATION_PORT, self.VOLTAGE_PATH),
                            json=voltage, timeout=2)

    def send_trajectory(self, trajectory):
        return requests.put(
            self._url(addresses.BASE_STATION_ADDRESS, addresses.BASE_STATION_PORT, self.TRAJECTORY_PATH),
            json=trajectory, timeout=2)

    def send_treasures(self, treasures):
        return requests.put(self._url(addresses.BASE_STATION_ADDRESS, addresses.BASE_STATION_PORT, self.TREASURES_PATH),
                            json=treasures, timeout=2)

    def send_destination(self, destination):
        return requests.put(
            self._url(addresses.BASE_STATION_ADDRESS, addresses.BASE_STATION_PORT, self.DESTINATION_PATH),
            json=destination, timeout=2)

    def get_destination(self, letter):
        relative_path = self.CODE_QUERY_PATH + letter
        response = None
        for address in addresses.ISLAND_API_ADDRESSES:
            try:
                response = requests.get(
                    self._url(address, addresses.ISLAND_API_PORT, relative_path, self.ISLAND_API_PROTOCOL),
                    timeout=3, verify=False)
                break
            except requests.exceptions.ConnectTimeout:
                pass
        return self.__get_island(response.json())

    def send_log(self, message):
        return requests.post(self._url(addresses.BASE_STATION_ADDRESS, addresses.BASE_STATION_PORT, self.LOG_PATH),
                             json=message, timeout=2)

    def __get_island(self, destination):
        if self.COLOR_ACCESSOR in destination:
            return destination[self.COLOR_ACCESSOR]
        return destination[self.FORM_ACCESSOR]
