"""
This module houses the Move and ChangeMatrix classes.
"""
from enum import Enum

from core.node import NodeValue


class Move:
    """
    Represents the player's action of moving a selection of marbles
    on the board.
    """

    def __init__(self, move_type, start_node, end_node, direction,
                 change_matrix=None):
        """
        Initializes a Move object.

        :param move_type: a MoveType enum object
        :param start_node: a Node object
        :param end_node: a Node object
        :param direction: a Direction enum object
        :param change_matrix: a ChangeMatrix object
        """
        self._move_type = move_type
        self.start_node = start_node
        self.end_node = end_node
        self.direction = direction
        self._change_matrix = change_matrix

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
        """
        Returns this Move's type.

        :return: a MoveType enum object
        """
        return self._move_type

    @move_type.setter
    def move_type(self, new_move_type):
        """
        Sets a new move type for this Move.

        :param new_move_type: a MoveType enum object
        """
        self._move_type = new_move_type

    @property
    def change_matrix(self):
        """
        Returns the change matrix for this Move.

        :return: a ChangeMatrix object
        """
        return self._change_matrix

    def is_inline_move(self):
        """
        Checks whether the start and end nodes are inline.

        :return: True if start and end nodes are inline, False otherwise
        """
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


class ChangeMatrix:
    """
    A 2d array of all NodeValue.INVALIDs except for spaces that are modified as a result of
    a Move. This matrix is used to produce the resulting board after a Move.
    """

    def __init__(self, moving_player, original_positions, new_positions, pushed_nodes=None):
        """
        Initializes a ChangeMatrix object.

        :param moving_player: an int equal to 1 or 2
        :param original_positions: a list of nodes at pre-move locations
        :param new_positions: a list of nodes at post-move locations
        :param pushed_nodes: a list of nodes at locations after being pushed
        """
        self._matrix = self.generate_change_matrix_from_nodes(moving_player, original_positions,
                                                              new_positions, pushed_nodes)

    @staticmethod
    def generate_change_matrix_from_nodes(moving_player, original_positions, new_positions, pushed_nodes=None):
        """
        Returns a change matrix by setting all original positions to NodeValue.Empty, all
        new positions to the moving player's corresponding NodeValue, and all pushed nodes'
        ending positions to the opposing player's NodeValue.

        :param moving_player: an int equal to 1 or 2
        :param original_positions: a list of nodes at pre-move locations
        :param new_positions: a list of nodes at post-move locations
        :param pushed_nodes: a list of nodes at locations after being pushed
        :return: a 2d array of NodeValues
        """
        moving_player_value = NodeValue.get_node_value_from_num(moving_player)
        other_player_value = NodeValue.WHITE if moving_player_value == NodeValue.BLACK else NodeValue.BLACK
        change_matrix = [[NodeValue.INVALID for col in range(11)] for row in range(11)]
        for node in original_positions:
            change_matrix[node.row][node.column] = NodeValue.EMPTY
        for node in new_positions:
            change_matrix[node.row][node.column] = moving_player_value
        if pushed_nodes:
            for node in pushed_nodes:
                change_matrix[node.row][node.column] = other_player_value
        return change_matrix

    @property
    def matrix(self):
        """
        Returns the change matrix.

        :return: a 2d array of ints
        """
        return self._matrix


class MoveType(Enum):
    """
    Enumeration of all move types.
    """
    Inline = 1, 'i'
    Sidestep = 2, 's'
    Push = 3, 'p'
    Scoring = 4, 'w'
    # These 2 move types are only used in state generation
    Unknown = None, 'u'
    Invalid = 0, 'x'


class Direction(Enum):
    """
    Enumeration of all directions of movement.
    """
    L = (0, -1), 9
    R = (0, 1), 3
    TL = (-1, 0), 11
    TR = (-1, 1), 1
    BL = (1, -1), 7
    BR = (1, 0), 5

    @staticmethod
    def left_directions():
        """
        Returns all directions containing "Left" in them.

        :return: a set of Direction enum objects
        """
        return {Direction.L, Direction.TL, Direction.BL}


if __name__ == "__main__":
    print(f"{MoveType.Inline.value[0]._generate}")
