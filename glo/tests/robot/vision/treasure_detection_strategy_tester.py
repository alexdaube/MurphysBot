import json
import math

from tests.common.vision.detection_strategy_tester import DetectionStrategyTester


class TreasureDetectionStrategyTester(DetectionStrategyTester):
    PATH = "./data/world_pictures/treasures"

    def test_method(self, testdata, calculateddata):
        testdata = testdata["from_list"]
        self.eliminate_identical_shapes(calculateddata, testdata)

        errors = []
        for shape in testdata:
            errors.append("Shape not detected: " + json.dumps(shape))
        for shape in calculateddata:
            errors.append("Artifact: " + json.dumps(shape))
        return errors

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
            if self.positions_match(calcshape, testshape["descriptor_points"]):
                del testdata[i]
                del calculateddata[j]
                i, j = 0, 0
            else:
                j += 1

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
