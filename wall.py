from field import *


class Wall(Field):
    """Wall defines a field that blocking passage through labyrinth"""
    def __init__(self, point: Point):
        super(Wall, self).__init__(point)
        self.tmp_char = '1'

    def previous_corridor(self):
        """Returns a reference (or coords?) to neighbour corridor that is closest to entrance
            or null if previous corridor is entrance"""
        pass


# Test purposes - delete later:
if __name__ == '__main__':
    c1 = Wall(Point(5, 6))
    print(c1.coordinates.get_x(), c1.coordinates.get_y())