import math as math


class Position(object):
    X = None
    Y = None

    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __eq__(self, other):
        if self.X == other.X and self.Y == other.Y:
            return True
        else:
            return False

    def calculate_distance(self, position):
        return math.sqrt(math.pow(self.X - position.X, 2) + math.pow(self.Y - position.Y, 2))

    def calculate_angle(self, position):
        """
        :param position: a second position
        :return angle: the angle between two position in degree
        The angle is calculated from the y-axis clockwise
        Result is undefine (0) if the position is the same
        """
        if self.__eq__(position):
            return 0
        else:
            x_distance = position.X - self.X
            y_distance = position.Y - self.Y

            if y_distance > 0:
                if x_distance == 0:
                    return 0
                else:
                    return math.degrees(math.atan(x_distance / y_distance))
            elif y_distance < 0:
                if x_distance > 0:
                    return math.degrees(math.atan(x_distance / -y_distance)) + 90
                elif x_distance < 0:
                    return math.degrees(math.atan(x_distance / -y_distance)) - 90
                else:
                    return 180
            else:
                if x_distance > 0:
                    return 90
                else:
                    return -90
