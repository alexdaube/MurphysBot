from common.vision.camera import Camera
from robot.vision.charge_station_detector import ChargeStationDetector
from robot.vision.island_detector import IslandDetector
from robot.vision.treasure_detector import TreasureDetector


class RobotVision(object):
    def __init__(self, island_detector=None, treasure_detector=None, charge_station_detector=None, camera=None):
        self.island_detector = island_detector or IslandDetector()
        self.treasure_detector = treasure_detector or TreasureDetector()
        self.charge_station_detector = charge_station_detector or ChargeStationDetector()
        self.camera = camera or Camera(0)

    def detect_island(self, island_description, island_color, average_point=True, black_out=-1):
        picture = self.camera.get_current_frame()
        if black_out > -1:
            picture[black_out:, :] = [0, 0, 0]
        islands = self.island_detector.detect_island(picture, island_description, island_color)
        if isinstance(islands, list):
            for island in islands:
                island["points"] = self.get_average_point(island["points"])
        else:
            if islands is not None and average_point:
                islands["points"] = self.get_average_point(islands["points"])
        return islands, picture

    def detect_treasures(self, average_point=False, black_out=-1, in_wall=True):
        picture = self.camera.get_current_frame()
        if black_out > -1:
            picture[black_out:, :] = [0, 0, 0]
        treasures = self.treasure_detector.detect_treasures(picture, in_wall)
        if average_point:
            for i in range(0, len(treasures)):
                treasures[i] = self.get_average_point(treasures[i])
        return treasures, picture

    def detect_recharge_station(self):
        picture = self.camera.get_current_frame()
        recharge_station = self.charge_station_detector.detect_charge_station(picture)
        return recharge_station, picture

    @staticmethod
    def get_average_point(points):
        sum_x, sum_y = 0, 0
        for i in range(0, len(points)):
            sum_x += points[i][0]
            sum_y += points[i][1]
        return [sum_x / len(points), sum_y / len(points)]
