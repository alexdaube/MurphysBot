from common.vision.shape_type import ShapeType


class IslandDetector:
    def __init__(self, strategy):
        self.strategy = strategy

    def detect_islands(self, pictures):
        islands = [self.strategy.detect(picture) for picture in pictures]
        return self._filter_islands(islands)

    def _filter_islands(self, islands):
        i = 0
        confirmed = []
        same = []
        while len(islands[i]) > 0:
            island = islands[i][0]
            for j in range(0, len(islands)):
                contains = self.contains(island, islands[j])
                if contains > -1:
                    same.append(islands[j][contains])
                    del islands[j][contains]
            if len(same) > 1:
                confirmed.append(same[0])
                same = []
        return confirmed

    def contains(self, island, islands):
        for i in range(0, len(islands)):
            if island["type"] == islands[i]["type"] == ShapeType.Wall or \
                    (island["type"] == islands[i]["type"] and \
                                 island["color"] == islands[i]["color"]):
                return i
        return -1
