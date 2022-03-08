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
        self.p1_marbles = self.get_marble_count(1)
        self.p2_marbles = self.get_marble_count(2)

    def __repr__(self):
        node_str = ""
        for row in self._board:
            for column in row:
                node_str = ''.join((node_str, f"{column.node_value.value} "))
            node_str = ''.join((node_str, "\n"))
        return f"Turn: player {self.player} {node_str}\nP1 marbles: {self.p1_marbles} P2 marbles: {self.p2_marbles}"

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

    def get_node(self, row, column):
        return self._board[row][column]

    def get_all_marbles_for_player(self, player):
        return {node for row in self._board for node in row if node.node_value.value == player}

    def get_marble_count(self, player):
        return len(self.get_all_marbles_for_player(player))

    def apply_move(self, move):
        if self.player == 1:
            self.player = 2  # this is an option, updating itself
            # new_state_rep = StateRepresentation(2, updated_board)  # this is the other option, new StateRep
        else:
            self.player = 1
            # new_state_rep = StateRepresentation(1, updated_board)
        pass

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, value):
        self._player = value
