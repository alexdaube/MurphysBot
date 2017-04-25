class PointOfInterestType:
    TREASURE = "treasure"
    RECHARGE_STATION = "recharge_station"
    ISLAND = "island"
    TRIANGLE_ISLAND = "triangle_island"
    SQUARE_ISLAND = "square_island"
    PENTAGON_ISLAND = "pentagon_island"
    CIRCLE_ISLAND = "circle_island"
    RED_COLOR = 0xFF0000FF
    GREEN_COLOR = 0x00FF00FF
    BLUE_COLOR = 0x0000FFFF
    YELLOW_COLOR = 0xFFFF00FF

    @staticmethod
    def from_string(value):
        if value == "cercle":
            return PointOfInterestType.CIRCLE_ISLAND
        elif value == "rectangle":
            return PointOfInterestType.SQUARE_ISLAND
        elif value == "triangle":
            return PointOfInterestType.TRIANGLE_ISLAND
        elif value == "pentagone":
            return PointOfInterestType.PENTAGON_ISLAND
        elif value == "rouge":
            return PointOfInterestType.RED_COLOR
        elif value == "vert":
            return PointOfInterestType.GREEN_COLOR
        elif value == "jaune":
            return PointOfInterestType.YELLOW_COLOR
        elif value == "bleu":
            return PointOfInterestType.BLUE_COLOR
        else:
            return "You dun goofed"
