from abc import ABC, abstractmethod


class Point:
    _MAX_VALUE: int = 30

    def __init__(self, x: int, y: int):
        if (x < 0 or y < 0)or (x > 30 or y > 30):
            raise NotImplementedError
        else:
            self._x = x
            self._y = y

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y


class Field(ABC):
    @abstractmethod
    def __init__(self, point: Point):
        self.coordinates = point


class Wall(Field):
    """Wall defines a field that blocking passage through labyrinth"""
    def __init__(self, point: Point):
        super(Wall, self).__init__(point)
        self.tmp_char = '1'

    def previous_corridor(self):
        """Returns a reference (or coords?) to neighbour corridor that is closest to entrance
            or null if previous corridor is entrance"""
        pass


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


class Entrance(Corridor):
    """Class Entrance defines labyrinth entrance and:
        - provide logic to make sure that labyrinth has only one entrance"""
    def __init__(self, point: Point):
        super(Entrance, self).__init__(point)


class Exit(Corridor):
    """Class Exit defines labyrinth exit and:
        - provides logic to make sure labyrinth has only one way out
        - ensure that given field is not entrance
        - ensure that given field is not next to entrance """
    def __init__(self, point: Point):
        super(Exit, self).__init__(point)


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

