from abc import ABC, abstractmethod
from point import Point


class Field(ABC):
    @abstractmethod
    def __init__(self, point: Point):
        self.coordinates = point
