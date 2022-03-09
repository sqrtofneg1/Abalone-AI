from node import NodeValue
from move import Move, Direction
from state_representation import StateRepresentation


class StateSpaceGenerator:

    def __init__(self, state_rep):
        self.state_rep = state_rep

    def generate_state_space(self, state_rep):
        pass  # should return an array of Move objects

    def generate_one_marble_moves(self):
        curr_player_marbles = self.state_rep.get_all_marbles_for_player(self.state_rep.player)
        moves_generated = []
        for node in curr_player_marbles:
            direction_dict = self.get_adjacent_nodes_values(node)
            for direction, adj_node_value in direction_dict.items():
                if adj_node_value == NodeValue.EMPTY:
                    moves_generated.append(Move(node, node, direction))
        return moves_generated

    def generate_two_marble_moves(self):
        marble_selections = self.get_valid_two_marble_selections()
        all_moves = {Move(node1, node2, direction) for (node1, node2) in marble_selections for direction in Direction}
        valid_moves = {move for move in all_moves if self.is_valid_two_marble_move(move)}
        return valid_moves

    def get_valid_two_marble_selections(self):
        """
        Returns a set of tuples of nodes (Node1, Node2) for all valid 2 marble selections
        for the current player.
        :return: a set of tuples of nodes, the valid selections for two marbles
        """
        curr_player_marbles = self.state_rep.get_all_marbles_for_player(self.state_rep.player)
        return {(marble1, marble2) for marble1 in curr_player_marbles for marble2 in self.get_left_nodes(marble1)
                if marble1.node_value == marble2.node_value}

    def is_valid_two_marble_move(self, move):
        new_start_node = self.get_node_in_direction_of_node(move.start_node, move.direction)  # location of start node after move
        new_end_node = self.get_node_in_direction_of_node(move.end_node, move.direction)  # location of end node after move
        if move.is_inline_move():
            front_node = new_start_node if new_end_node == move.start_node else new_end_node
            # front_node is the node that potentially will be pushed, so if A1-B1-TL, then it would be C1
            if front_node.node_value == NodeValue.INVALID:  # edge of board
                return False
            if front_node.node_value == NodeValue.EMPTY:
                return True
            elif (front_node.node_value.value == abs(3 - move.start_node.node_value.value)) & \
                    (self.get_node_in_direction_of_node(front_node, move.direction).node_value == NodeValue.EMPTY):
                return True
        else:
            if (new_start_node.node_value == NodeValue.EMPTY) & \
                    (new_end_node.node_value == NodeValue.EMPTY):
                return True
        return False

    def get_node_in_direction_of_node(self, node, direction):
        result_row = node.row + direction.value[0][0]
        result_column = node.column + direction.value[0][1]
        return self.state_rep.get_node(result_row, result_column)

    def get_adjacent_nodes_values(self, node):
        """
        Returns a dictionary with the adjacent nodes' values in all 6 directions.

        :param node: a Node
        :return: dictionary of adjacent nodes' values
        """
        return {direction: self.get_node_in_direction_of_node(node, direction).node_value
                for direction in Direction}

    def get_left_nodes(self, node):
        """
        Returns a set with the adjacent nodes in left directions (TL, L, BL).
        Used when generating selections of 2 or 3 marbles in a row.
        :param node: a Node
        :return: set of Nodes in the left directions
        """
        return {self.get_node_in_direction_of_node(node, direction) for direction in Direction.left_directions()}


if __name__ == "__main__":
    import node_arrays

    stateSpaceGen = StateSpaceGenerator(StateRepresentation.get_start_state_rep(node_arrays.DEFAULT_START))
    print(stateSpaceGen.generate_one_marble_moves())  # implement a way to sort move outputs alphabetically?
    print(stateSpaceGen.get_valid_two_marble_selections())
    print(stateSpaceGen.generate_two_marble_moves())
