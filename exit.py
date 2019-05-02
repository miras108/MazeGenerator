from corridor import *


class Exit(Corridor):
    """Class Exit defines labyrinth exit and:
        - provides logic to make sure labyrinth has only one way out
        - ensure that given field is not entrance
        - ensure that given field is not next to entrance """
    def __init__(self, point: Point):
        super(Exit, self).__init__(point)


# Test purposes - delete later:
if __name__ == '__main__':
    c1 = Exit(Point(5, 7))
    print(c1.coordinates.get_x(), c1.coordinates.get_y())