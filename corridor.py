from field import *


class Corridor(Field):
    def __init__(self, point: Point):
        super(Corridor, self).__init__(point)
        self.tmp_char = '0'

    def previous_corridor(self):
        """Returns a reference (or coords?) to neighbour corridor that is closest to entrance
            or null if previous corridor is entrance"""
        pass

    def next_corridors(self):
        """Returns a list of references (or coords?) to neighbours corridors that are closer to exit
            or empty list if next corridor is exit"""
        pass

    def way_to_inter_point(self):
        """Returns a list of references (or coords?) to closest InterPoints"""
        pass


# Test purposes - delete later:
if __name__ == '__main__':
    c1 = Corridor(Point(5, 2))
    print(c1.coordinates.get_x(), c1.coordinates.get_y())
