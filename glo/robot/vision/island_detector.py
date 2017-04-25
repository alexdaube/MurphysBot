from robot.vision.robot_number_of_sides_island_strategy import RobotNumberOfSidesIslandStrategy


class IslandDetector(object):
    def __init__(self, strategy=RobotNumberOfSidesIslandStrategy()):
        self.strategy = strategy

    def detect_island(self, picture, island_description, island_color):
        islands = self.strategy.detect(picture)
        if island_description is not None or island_color is not None:
            return self._filter_islands(islands, island_description, island_color)
        else:
            return islands

    def _filter_islands(self, islands, island_description, island_color):
        for island in islands:
            if island["POIType"] == island_description and island["POIColor"] == island_color:
                return island
        for island in islands:
            if island["POIColor"] == island_color:
                return island
        return None
