"""
This module houses the State class.
"""
from copy import deepcopy


import sys,os
sys.path.append(os.path.realpath('..'))

from core.node import NodeValue, Node
from core.move import MoveType
from layouts import layout_arrays


class State:
    """
    Represents a snapshot of the game which contains a game board,
    the player who has the turn, and the game score for each player.
    """

    def __init__(self, current_player, board):
        """
        Initializes a State object.

        :param current_player: an int equal to 1 or 2
        :param board: a 2D array of Nodes
        """
        self._player = current_player
        self._board = board  # 2d array of Nodes
        self.scores = [14 - self.get_nodes_count_for_player(1), 14 - self.get_nodes_count_for_player(2)]

    def __repr__(self):
        """
        Returns the state's information.

        :return: the state's information as a string
        """
        node_str = ""
        for row in self._board:
            for column in row:
                node_str = ' '.join((node_str, f"{column.node_value.value} "))
            node_str = ''.join((node_str, "\n"))
        return f"\nPlayer {self.player}'s turn --- " \
               f"P1 score: {self.scores[0]} --- P2 Score: {self.scores[1]}\n{node_str}"

    @staticmethod
    def get_start_state(start_layout):
        """
        Returns the State object for the start of the game corresponding
        to the given starting layout.

        :param start_layout: the 2d array of the starting layout
        :return: a State object
        """
        return State(1, State.get_board_from_nodes(Node.get_start_nodes(start_layout)))

    @staticmethod
    def get_board_from_nodes(nodes):
        """
        Returns the board (2d array of Nodes) for the given list of nodes.

        :param nodes: a list of Nodes
        :return: a 2d array of Nodes
        """
        board = [[None for col in range(11)] for row in range(11)]
        for node in nodes:
            board[node.row][node.column] = node  # Set all white/black nodes

        for row in range(11):
            for column in range(11):
                if not layout_arrays.VALID_NODES[row][column]:
                    board[row][column] = Node(NodeValue.INVALID, row, column)  # Set all invalid nodes
                if board[row][column] is None:
                    board[row][column] = Node(NodeValue.EMPTY, row, column)  # Set all remaining nodes to be empty nodes
        return board

    @property
    def player(self):
        """
        Returns the player who has the current turn.

        :return: an int equal to 1 or 2
        """
        return self._player

    @player.setter
    def player(self, value):
        """
        Sets the player who has the current turn.

        :param value: an int equal to 1 or 2
        """
        self._player = value

    @property
    def board(self):
        """
        Returns the board.

        :return: a 2d array of Nodes
        """
        return self._board

    @board.setter
    def board(self, new_board):
        """
        Sets the board to a new board.

        :param new_board: a 2d array of Nodes
        """
        self._board = new_board

    def get_node(self, row, column):
        """
        Returns the Node at the specified coordinates.

        :param row: an int
        :param column: an int
        :return: a Node
        """
        return self._board[row][column]

    def get_all_nodes_for_player(self, player):
        """
        Returns all Nodes belonging to the specified player.

        :param player: an int equal to 1 or 2
        :return: a set of Nodes
        """
        return {node for row in self._board for node in row if node.node_value.value == player}

    def get_nodes_count_for_player(self, player):
        """
        Returns the count of Nodes belonging to the specified player.

        :param player: an int equal to 1 or 2
        :return: an int
        """
        return len(self.get_all_nodes_for_player(player))

    def get_node_in_direction_of_node(self, node, direction):
        """
        Returns the node adjacent to given node in the specified direction.

        :param node: a Node object
        :param direction: a Direction enum object
        :return: a Node object
        """
        result_row = node.row + direction.value[0][0]
        result_column = node.column + direction.value[0][1]
        return self.get_node(result_row, result_column)

    def get_node_in_opposite_direction_of_node(self, node, direction):
        """
        Returns the node adjacent to given node in the opposite direction
        of specified.

        :param node: a Node object
        :param direction: a Direction enum object
        :return: a Node object
        """
        result_row = node.row - direction.value[0][0]
        result_column = node.column - direction.value[0][1]
        return self.get_node(result_row, result_column)

    def apply_move(self, move):
        """
        Applies the given move to this state to produce the resulting state.

        :param move: a Move object
        :return: a new State object
        """
        next_player = 2 if self.player == 1 else 1
        new_state = State(next_player, deepcopy(self.board))
        if move.move_type == MoveType.Scoring:
            new_state.scores[next_player - 1] += 1
        for row in new_state.board:
            for node in row:
                if node.node_value.value:  # if not NodeValue.INVALID
                    new_val = move.change_matrix.matrix[node.row][node.column]
                    if new_val.value:
                        new_state.board[node.row][node.column].node_value = new_val
        return new_state

