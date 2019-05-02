from field import *
from corridor import *
from wall import *
from random import *


class Labyrinth:
    """Fix all primitive objects into labyrinth"""
    def __init__(self, width, height):
        self._area_width = width
        self._area_height = height
        fields = (Corridor, Wall)

        self.area = []
        for i in range(self._area_height):
            for j in range(self._area_width):
                field = choice(fields)
                self.area.append(field(Point(i, j)))

    def print(self):
        counter = 0
        for field in self.area:
            print(field.tmp_char, end='\t')
            if counter == self._area_width - 1:
                print('\n')
                counter = 0
            else:
                counter += 1


# Test purposes - delete later:
if __name__ == '__main__':
    lab = Labyrinth(10, 10)
    lab.print()