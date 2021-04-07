from enum import Enum

class SeamType(Enum):
    H = 0
    V = 1

class Seam:
    type = SeamType.H
    size = 0
    pixels = []

    def __init__(self, type, size):
        self.type = type
        self.size = size

        self.pixels = []
        for i in range(0, self.size):
            self.pixels.append(-1)
