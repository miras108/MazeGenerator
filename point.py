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


# Test purposes - delete later:
if __name__ == '__main__':
    p1 = Point(5, 7)
    p2 = Point(1, 30)
    print(p1.get_x(), p1.get_y())
    print(p2.get_x(), p2.get_y())