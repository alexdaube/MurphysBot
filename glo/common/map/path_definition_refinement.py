import math

from common.map.position import Position


def generate_way_point_list_with_max_distance(way_point_list, max_distance, no_split_threshold=0):
    if no_split_threshold < 0:
        no_split_threshold = 0
    elif no_split_threshold > 1:
        no_split_threshold = 1
    if max_distance > 0 and len(way_point_list) > 1:
        new_waypoints_list = list()
        previous = None
        for way_point in way_point_list:
            if previous is None:
                new_waypoints_list.append(way_point)
            else:
                distance_between_way_points = previous.calculate_distance(way_point)
                if distance_between_way_points > max_distance:
                    split_amount = round(math.floor(
                        float(distance_between_way_points) / float(max_distance) + float(1 - no_split_threshold)))
                    if previous.X != way_point.X:
                        __split_following_x(new_waypoints_list, previous, split_amount, way_point)
                    else:
                        __split_following_y(new_waypoints_list, previous, split_amount, way_point)
                    new_waypoints_list.append(way_point)
                else:
                    new_waypoints_list.append(way_point)
            previous = way_point
        return new_waypoints_list
    else:
        return way_point_list


def __split_following_y(new_waypoints_list, previous, split_amount, way_point):
    y_distance = (float(way_point.Y) - float(previous.Y)) / float(split_amount)
    for current_split in range(1, int(split_amount)):
        y_position = previous.Y + y_distance * float(current_split)
        new_waypoint = Position(previous.X, y_position)
        new_waypoints_list.append(new_waypoint)


def __split_following_x(new_waypoints_list, previous, split_amount, way_point):
    x_distance = (float(way_point.X) - float(previous.X)) / float(split_amount)
    line_slope = (float(way_point.Y) - float(previous.Y)) / (
        float(way_point.X) - float(previous.X))
    line_origin = previous.Y - previous.X * line_slope
    for current_split in range(1, int(split_amount)):
        x_position = previous.X + x_distance * float(current_split)
        y_position = line_origin + line_slope * x_position
        new_waypoint = Position(x_position, y_position)
        new_waypoints_list.append(new_waypoint)
