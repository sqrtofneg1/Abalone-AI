from copy import deepcopy

from move import MoveType
from node import Node, NodeValue
import node_arrays


class StateRepresentation:

    def __init__(self, current_player, board):
        """
        Initializes a StateRepresentation object.

        :param current_player: an int equal to 1 or 2
        :param board: a 2D array of Nodes
        """
        self._player = current_player
        self._board = board  # 2d array of Nodes
        self.scores = [14 - self.get_marble_count(1), 14 - self.get_marble_count(2)]

    def __repr__(self):
        node_str = ""
        for row in self._board:
            for column in row:
                node_str = ' '.join((node_str, f"{column.node_value.value} "))
            node_str = ''.join((node_str, "\n"))
        return f"\nPlayer {self.player}'s turn --- P1 score: {self.scores[0]} --- P2 Score: {self.scores[1]}\n{node_str}"

    def get_node_in_direction_of_node(self, node, direction):
        result_row = node.row + direction.value[0][0]
        result_column = node.column + direction.value[0][1]
        return self.get_node(result_row, result_column)

    def get_node_in_opposite_direction_of_node(self, node, direction):
        result_row = node.row - direction.value[0][0]
        result_column = node.column - direction.value[0][1]
        return self.get_node(result_row, result_column)

    @staticmethod
    def get_start_state_rep(start_layout):
        return StateRepresentation(1, StateRepresentation.get_board_from_nodes(Node.get_start_nodes(start_layout)))

    @staticmethod
    def get_board_from_nodes(nodes):
        board = [[None for _ in range(11)] for _ in range(11)]
        for node in nodes:
            board[node.row][node.column] = node  # Set all white/black nodes

        for row in range(11):
            for column in range(11):
                if not node_arrays.VALID_NODES[row][column]:
                    board[row][column] = Node(NodeValue.INVALID, row, column)  # Set all invalid nodes
                if board[row][column] is None:
                    board[row][column] = Node(NodeValue.EMPTY, row, column)  # Set all remaining nodes to be empty nodes
        return board

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, value):
        self._player = value

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, value):
        self._board = value

    def get_node(self, row, column):
        return self._board[row][column]

    def get_all_marbles_for_player(self, player):
        return {node for row in self._board for node in row if node.node_value.value == player}

    def get_marble_count(self, player):
        return len(self.get_all_marbles_for_player(player))

    def apply_move(self, move):
        next_player = 2 if self.player == 1 else 1
        new_state_rep = StateRepresentation(next_player, deepcopy(self.board))
        if move.move_type == MoveType.Scoring:
            new_state_rep.scores[next_player - 1] += 1
        for row in new_state_rep.board:
            for node in row:
                if node.node_value.value:
                    new_val = move.change_matrix[node.row][node.column]
                    if new_val.value:
                        new_state_rep.board[node.row][node.column].node_value = new_val
        return new_state_rep
