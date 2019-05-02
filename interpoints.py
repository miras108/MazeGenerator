from field import *
from corridor import Corridor

class InterPoints():
    """InterPoints class introduces a list of chosen points:
        - that passage must pass between entrance and exit
        - interPoints list is dynamically changing it's size - if user add point(s) then new passage is generated"""
    def __init__(self):
        self.points = []

    def add_point(self, field: Field):
        if field in self.points:
            self.delete_point(field)
        else:
            self.points.append(field)

    def delete_point(self, field: Field):
        self.points.remove(field)


# Test purposes - delete later:
if __name__ == '__main__':
    ip = InterPoints()
    c1 = Corridor(Point(5, 2))
    c2 = Corridor(Point(2, 1))
    ip.add_point(c1)
    ip.add_point(c2)
    ip.add_point(c1)
    #ip.add_point(Corridor(Point(2, 5)))
    for point in ip.points:
        print(point.coordinates.get_x(), point.coordinates.get_y())