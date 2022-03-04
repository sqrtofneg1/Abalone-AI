from enum import Enum


class Move:
    def __init__(self, start_node, end_node, direction):
        self.start_node = start_node
        self.end_node = end_node
        self.direction = direction


class Direction(Enum):
    """
    Notation for direction of movement.
    """
    L = (0, -1), 'Left'
    R = (0, 1), 'Right'
    TL = (-1, 0), 'Top-Left'
    TR = (-1, 1), 'Top-Right'
    BL = (1, -1), 'Bottom-Left'
    BR = (1, 0), 'Bottom-Right'

    @staticmethod
    def all_directions():
        return {Direction.L, Direction.R, Direction.TL, Direction.TR, Direction.BL, Direction.BR}
