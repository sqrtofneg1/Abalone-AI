from node import Node, NodeState
import node_arrays


class StateRepresentation:

    def __init__(self, current_player, board):
        self.player = current_player
        self.board = board  # 2d array of Nodes
        self.p1_marbles = self.get_marble_count(1)
        self.p2_marbles = self.get_marble_count(2)

    def get_node(self, row, column):
        return self.board[row][column]

    def get_marble_count(self, player):
        player_marbles = {node for row in self.board for node in row if node.get_state().value == player}
        return len(player_marbles)

    def get_node_in_direction_of_node(self, row, column, direction):
        result_row = row + direction.value[0]
        result_column = column + direction.value[1]
        return self.get_node(result_row, result_column)

    def apply_move(self, move):
        if self.player == 1:
            self.player = 2  # this is an option, updating itself
            # new_state_rep = StateRepresentation(2, updated_board)  # this is the other option, new StateRep
        else:
            self.player = 1
            # new_state_rep = StateRepresentation(1, updated_board)
        pass

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
                    board[row][column] = Node(NodeState.INVALID)  # Set all invalid nodes
                if board[row][column] is None:
                    board[row][column] = Node(NodeState.EMPTY)  # Set all remaining nodes to be empty nodes

        return board

    def __repr__(self):
        node_str = ""
        for row in self.board:
            node_str += "\n"
            for column in row:
                node_str += f" {column._state.value}"
        return f"Turn: player {self.player} {node_str}\nP1 marbles: {self.p1_marbles} P2 marbles: {self.p2_marbles}"
