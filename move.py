from enum import Enum


class Move:
    def __init__(self, start_node, end_node, direction):
        self.start_node = start_node
        self.end_node = end_node
        self.direction = direction

    def __repr__(self):
        return f"{self.start_node.get_front_end_coords()}" \
               f"-{self.end_node.get_front_end_coords()}" \
               f"-{self.direction.name}"

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
    def left_directions():
        return {Direction.L, Direction.TL, Direction.BL}
