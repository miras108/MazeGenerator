from corridor import *


class Entrance(Corridor):
    """Class Entrance defines labyrinth entrance and:
        - provide logic to make sure that labyrinth has only one entrance"""
    def __init__(self, point: Point):
        super(Entrance, self).__init__(point)


# Test purposes - delete later:
if __name__ == '__main__':
    c1 = Entrance(Point(2, 1))
    print(c1.coordinates.get_x(), c1.coordinates.get_y())