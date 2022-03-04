"""
NAME
    Node

DESCRIPTION:
    This module contains methods/functions/variables that belong and support the Node class that is below.
"""
from enum import Enum


class Node:
    def __init__(self, state, row=None, column=None):
        """
        Initializes data members and constructs a Node object.
        """
        self._state = state
        self.row = row
        self.column = column

    def get_state(self):
        """
        This method returns the self._state variable
        """
        return self._state

    def set_state(self, state):
        """
        This method sets the  self._state variable to the state parameter
        """
        self._state = state

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
        Gets all non-invalid, non-empty starting nodes of a starting layout
        :param start_layout: one of DEFAULT_START, BELGIAN_DAISY_START, or GERMAN_DAISY_START
        :return: a list of non-invalid, non-empty starting nodes of said layout
        """
        nodes = set()
        for row in range(len(start_layout)):
            for column in range(len(start_layout)):
                node_val = start_layout[row][column]
                if node_val == NodeState.BLACK.value:
                    nodes.add(Node(NodeState.BLACK, row, column))
                elif node_val == NodeState.WHITE.value:
                    nodes.add(Node(NodeState.WHITE, row, column))
        return nodes

    def __repr__(self):
        if self.row is not None and self.column is not None:
            return f"{chr(abs(11 - self.row) + 63)}{self.column} - {self._state.value}"
        else:
            return f"{self._state.value}"


class NodeState(Enum):
    INVALID = 0
    BLACK = 1
    PLAYER_1 = 1
    WHITE = 2
    PLAYER_2 = 2
    EMPTY = 3
