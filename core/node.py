"""
This module houses the Node class.
"""
from enum import Enum, auto


class Node:
    """
    Represents a space/hex/spot on the board, which has a row, a column,
    and a NodeValue indicating what occupies that space (player/empty/invalid).
    """

    def __init__(self, node_value, row=None, column=None):
        """
        Initializes data members and constructs a Node object.

        :param node_value: a NodeValue
        :param row: an int
        :param column: an int
        """
        self._node_value = node_value
        self._row = row
        self._column = column

    def __repr__(self):
        """
        Returns the node's information in COMP3981's testing format.

        :return: the node's information as a string
        """
        if self.row is not None and self.column is not None:
            if self.node_value.value == 1:
                return f"{self.get_front_end_coords()}b"
            elif self.node_value.value == 2:
                return f"{self.get_front_end_coords()}w"
            else:
                return f"{self.get_front_end_coords()} - {self.node_value.value}"
        else:
            return f"{self.node_value.value}"

    @staticmethod
    def get_row_from_alpha(alpha):
        """
        Gets the row number from char.

        :param alpha: a char from 'A' to 'I'
        :return: the row corresponding to that char as an int
        """
        return 74 - ord(alpha)

    @staticmethod
    def get_start_nodes(start_layout):
        """
        Gets all valid, non-empty starting nodes of a starting layout.

        :param start_layout: one of DEFAULT_START, BELGIAN_DAISY_START, or GERMAN_DAISY_START
        :return: a list of valid, non-empty starting nodes of said layout
        """
        nodes = set()
        for row in range(len(start_layout)):
            for column in range(len(start_layout)):
                node_val = start_layout[row][column]
                if node_val == NodeValue.BLACK.value:
                    nodes.add(Node(NodeValue.BLACK, row, column))
                elif node_val == NodeValue.WHITE.value:
                    nodes.add(Node(NodeValue.WHITE, row, column))
        return nodes

    @property
    def node_value(self):
        """
        Returns the node's value.

        :return: the node's value as NodeValue enum
        """
        return self._node_value

    @node_value.setter
    def node_value(self, new_value):
        """
        Sets the node's value to a new NodeValue
        """
        self._node_value = new_value

    @property
    def row(self):
        """
        Returns the row this node is on.

        :return: the row as an int
        """
        return self._row

    @property
    def column(self):
        """
        Returns the column this node is on.

        :return: the column as an int
        """
        return self._column

    @row.setter
    def row(self, value):
        """
        Sets the node's row to a new value.

        :param value: an int from 1 to 9
        """
        self._row = value

    @column.setter
    def column(self, value):
        """
        Sets the node's column to a new value.

        :param value: an int from 1 to 9
        """
        self._column = value

    def get_front_end_coords(self):
        """
        Returns this node's coordinates in the front-end display format (A1 - I9).

        :return: this node's coordinates in range A1 to I9
        """
        return f"{chr(abs(11 - self.row) + 63)}{self.column}"


class NodeValue(Enum):
    """
    Enumeration of the possible values that a node can have.
    """
    INVALID = 0
    BLACK = PLAYER_1 = auto()
    WHITE = PLAYER_2 = auto()
    EMPTY = auto()

    @staticmethod
    def get_node_value_from_num(number):
        """
        Returns the NodeValue enum corresponding to the given number.

        :param number: an int between 0 and 3 (inclusive)
        :return: a NodeValue
        """
        for node_val in NodeValue:
            if node_val.value == number:
                return node_val
