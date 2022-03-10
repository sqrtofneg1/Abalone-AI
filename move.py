from copy import deepcopy
from enum import Enum, auto

import node_arrays


class Move:
    def __init__(self, move_type, start_node, end_node, direction,
                 change_matrix=None):
        self._move_type = move_type
        self.start_node = start_node
        self.end_node = end_node
        self.direction = direction
        self.change_matrix = change_matrix

    def __repr__(self):
        """
        Returns the move notation in a debug-friendly format.

        :return: a string move notation : str
        """
        start_end = f"{self.start_node.get_front_end_coords()}-{self.end_node.get_front_end_coords()}" \
            if self.start_node != self.end_node else f"{self.start_node.get_front_end_coords()}"
        return f"{self.move_type.value[1]}" \
               f"-{start_end}" \
               f"-{self.direction.name}"

    @property
    def move_type(self):
        return self._move_type

    @move_type.setter
    def move_type(self, new_move_type):
        self._move_type = new_move_type

    def is_inline_move(self):
        if self.start_node == self.end_node:
            return False
        for i in range(1, 3):
            result_row_from_start = self.start_node.row + self.direction.value[0][0] * i
            result_column_from_start = self.start_node.column + self.direction.value[0][1] * i
            if (result_row_from_start == self.end_node.row) & (result_column_from_start == self.end_node.column):
                return True
            result_row_from_end = self.end_node.row + self.direction.value[0][0] * i
            result_column_from_end = self.end_node.column + self.direction.value[0][1] * i
            if (result_row_from_end == self.start_node.row) & (result_column_from_end == self.start_node.column):
                return True
        return False


class MoveType(Enum):
    """
    Notation for move types.
    """
    Unknown = None, 'u'
    Invalid = 0, 'x'
    Inline = auto(), 'i'
    Sidestep = auto(), 's'
    Push = auto(), 'p'
    Scoring = auto(), 'w'


class Direction(Enum):
    """
    Notation for direction of movement.
    """
    L = (0, -1), 9
    R = (0, 1), 3
    TL = (-1, 0), 11
    TR = (-1, 1), 1
    BL = (1, -1), 7
    BR = (1, 0), 5

    @staticmethod
    def left_directions():
        return {Direction.L, Direction.TL, Direction.BL}
