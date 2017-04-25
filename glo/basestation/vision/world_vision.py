from common.constants import TABLE_WIDTH, TABLE_HEIGHT
from common.vision.shape_type import ShapeType


class WorldVision:
    islands = None
    wall_position = [0, 0]
    MAX_OFFSET_X = 80
    MAX_OFFSET_Y = 40

    def __init__(self, camera, robot_detector, island_detector):
        self.camera = camera
        self.robot_detector = robot_detector
        self.island_detector = island_detector

    def detect_elements(self):
        if self.islands is None:
            self.islands = self.detect_islands()
        robot = self.detect_robot()
        return {"robot": robot, "islands": self.islands, "walls": self.wall_position}

    def detect_islands(self):
        pictures = [self.camera.get_current_frame() for i in range(5)]
        islands = self.island_detector.detect_islands(pictures)
        picture_width = len(pictures[0][0])
        islands = self._convert_island_coordinates(islands, picture_width)
        return islands

    def _convert_robot_coordinates(self, robot, width):
        if 'x' in robot:
            offset_x = robot['x'] - (float(TABLE_WIDTH) / 2)
            ratio_x = offset_x / (float(TABLE_WIDTH) / 2)
            robot['x'] -= ratio_x * self.MAX_OFFSET_X
        if 'y' in robot:
            offset_y = robot['y'] - (float(TABLE_HEIGHT) / 2)
            ratio_y = offset_y / (float(TABLE_HEIGHT) / 2)
            robot['y'] -= ratio_y * self.MAX_OFFSET_Y
        return robot

    def _convert_island_coordinates(self, islands, width):
        self._get_walls(islands)
        image_ratio = float(TABLE_WIDTH) / float(width)
        for i in range(0, len(islands)):
            if islands[i]["type"] == ShapeType.Treasure:
                islands[i]["point"][0] = (islands[i]["point"][0] * image_ratio)
                islands[i]["point"][1] = (islands[i]["point"][1] - self.wall_position[0]) * image_ratio
            else:
                for y in range(0, len(islands[i]["points"])):
                    islands[i]["points"][y][0] = (islands[i]["points"][y][0] * image_ratio)
                    islands[i]["points"][y][1] = (islands[i]["points"][y][1] - self.wall_position[0]) * image_ratio
        self.wall_position[0] *= image_ratio
        self.wall_position[1] *= image_ratio
        return islands

    def _get_walls(self, islands):
        for i in range(0, 2):
            wall_y = islands[i]["points"][0][1]
            self.wall_position[i] = wall_y
        del islands[0]
        del islands[0]

    def detect_robot(self):
        picture = self.camera.get_current_frame()
        picture_width = len(picture[0])
        image_ratio = float(TABLE_WIDTH) / float(picture_width)
        robot = self.robot_detector.detect_robot(picture)
        if len(robot):
            robot["x"] *= image_ratio
            robot["y"] = (robot["y"] * image_ratio) - self.wall_position[0]
        robot = self._convert_robot_coordinates(robot, picture_width)
        return robot

    def get_image(self):
        return self.camera.get_current_frame()
