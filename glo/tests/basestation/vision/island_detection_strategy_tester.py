import json
import math

from common.vision.shape_type import ShapeType
from tests.common.vision.detection_strategy_tester import DetectionStrategyTester


class IslandDetectionStrategyTester(DetectionStrategyTester):
    PATH = "./data/world_pictures/islands"

    def test_method(self, testdata, calculateddata):
        testdata = testdata["from_list"]
        self.transform_circle_coords(calculateddata, testdata)
        self.eliminate_identical_shapes(calculateddata, testdata)

        errors = []
        for shape in testdata:
            errors.append("Shape not detected: " + json.dumps(shape))
        for shape in calculateddata:
            if shape["type"] == ShapeType.Wall:
                continue
            errors.append("Artifact: " + json.dumps(shape))
        return errors

    def transform_circle_coords(self, calculateddata, testdata):
        for testShape in testdata:
            if testShape["form_type"] == ShapeType.Circle:
                points = testShape["descriptor_points"]
                testShape["descriptor_points"] = [
                    {"x": (points[0]["x"] + points[1]["x"]) / 2, "y": (points[0]["y"] + points[1]["y"]) / 2}]

        for calcShape in calculateddata:
            if calcShape["type"] == ShapeType.Circle:
                points = calcShape["points"]
                calcShape["points"] = [[(points[0][0] + points[1][0]) / 2, (points[0][1] + points[1][1]) / 2]]

    def eliminate_identical_shapes(self, calculateddata, testdata):
        i, j = 0, 0
        while len(testdata) > 0 and len(calculateddata) > 0:
            if j >= len(calculateddata):
                j = 0
                i += 1
                if i >= len(testdata):
                    break

            testshape = testdata[i]
            calcshape = calculateddata[j]
            if self.shapes_match(calcshape, testshape) and \
                    self.positions_match(calcshape["points"], testshape["descriptor_points"]):
                del testdata[i]
                del calculateddata[j]
                i, j = 0, 0
            else:
                j += 1

    def shapes_match(self, calcshape, testshape):
        return testshape["form_type"] == calcshape["type"] and \
               testshape["form_color"] == calcshape["color"]

    def positions_match(self, calcpoints, testpoints):
        if len(calcpoints) != len(testpoints):
            return False
        i, j = 0, 0
        while i < len(testpoints):
            if j == len(calcpoints):
                return False
            testpoint = testpoints[i]
            calcpoint = calcpoints[j]
            if math.fabs(testpoint["x"] - calcpoint[0]) < 15 and math.fabs(testpoint["y"] - calcpoint[1]) < 15:
                i += 1
                j = 0
            else:
                j += 1

        return True
