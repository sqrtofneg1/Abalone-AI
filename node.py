"""
NAME
    Node

DESCRIPTION:
    This module contains methods/functions/variables that belong and support the Node class that is below.
"""
from enum import Enum


class Node:
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
        if self.row is not None and self.column is not None:
            return f"{self.get_front_end_coords()} - {self.node_value.value}"
        else:
            return f"{self.node_value.value}"

    @staticmethod
    def get_row_from_alpha(alpha):
        """
        Gets the row number from char
        :param alpha: a char from 'A' to 'I'
        :return: the row corresponding to that char
        """
        return -ord(alpha) + 74

    @staticmethod
    def get_start_nodes(start_layout):
        """
        Gets all valid, non-empty starting nodes of a starting layout
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
        This method returns the self._node_value variable
        """
        return self._node_value

    @node_value.setter
    def node_value(self, new_value):
        """
        This method sets the  self._node_value variable to the state parameter
        """
        self._node_value = new_value

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    @row.setter
    def row(self, value):
        self._row = value

    @column.setter
    def column(self, value):
        self._column = value

    def get_front_end_coords(self):
        return f"{chr(abs(11 - self.row) + 63)}{self.column}"


class NodeValue(Enum):
    INVALID = 0
    BLACK = 1
    PLAYER_1 = 1
    WHITE = 2
    PLAYER_2 = 2
    EMPTY = 3
