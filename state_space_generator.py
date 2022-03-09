from node import NodeValue
from move import Move, Direction
from state_representation import StateRepresentation


class StateSpaceGenerator:

    def __init__(self, state_rep):
        self.state_rep = state_rep

    def generate_state_space(self):
        all_valid_moves = set()
        all_valid_moves.update(self.generate_one_marble_moves())
        all_valid_moves.update(self.generate_two_marble_moves())
        all_valid_moves.update(self.generate_three_marble_moves())
        state_space = {self.state_rep.apply_move(move) for move in all_valid_moves}
        return state_space

    def generate_one_marble_moves(self):
        curr_player_marbles = self.state_rep.get_all_marbles_for_player(self.state_rep.player)
        moves_generated = set()
        for node in curr_player_marbles:
            direction_dict = self.get_adjacent_nodes_values(node)
            for direction, adj_node_value in direction_dict.items():
                if adj_node_value == NodeValue.EMPTY:
                    moves_generated.add(Move(node, node, direction))
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
        result_start_node = self.get_node_in_direction_of_node(move.start_node,
                                                               move.direction)  # location of start node after move
        result_end_node = self.get_node_in_direction_of_node(move.end_node,
                                                             move.direction)  # location of end node after move
        if move.is_inline_move():
            # push_node is the node that potentially will be pushed, so if A1-B1-TL, then it would be C1
            push_node = result_start_node if result_end_node == move.start_node else result_end_node

            if push_node.node_value == NodeValue.INVALID:  # edge of board
                return False
            if push_node.node_value == NodeValue.EMPTY:
                return True

            # if node being pushed is opposite colour
            if push_node.node_value.value == abs(3 - move.start_node.node_value.value):

                # if node behind pushed node is empty or off the board
                if (self.get_node_in_direction_of_node(push_node, move.direction).node_value == NodeValue.INVALID) | \
                        (self.get_node_in_direction_of_node(push_node, move.direction).node_value == NodeValue.EMPTY):
                    return True

        # sidestep move
        else:
            if (result_start_node.node_value == NodeValue.EMPTY) & \
                    (result_end_node.node_value == NodeValue.EMPTY):
                return True
        return False

    def generate_three_marble_moves(self):
        marble_selections = self.get_valid_three_marble_selections()
        all_moves = {Move(node1, node2, direction) for (node1, node2) in marble_selections for direction in Direction}
        valid_moves = {move for move in all_moves if self.is_valid_three_marble_move(move)}
        return valid_moves

    def get_valid_three_marble_selections(self):
        """
        Returns a set of tuples of nodes (Node1, Node2) for all valid 3 marble selections
        for the current player.
        :return: a set of tuples of nodes, the valid selections for three marbles
        """
        valid_marble_selections = set()
        curr_player_marbles = self.state_rep.get_all_marbles_for_player(self.state_rep.player)
        for marble1 in curr_player_marbles:
            for direction in Direction.left_directions():
                marble2 = self.get_node_in_direction_of_node(marble1, direction)
                if marble2.node_value is not NodeValue.INVALID:
                    marble3 = self.get_node_in_direction_of_node(marble2, direction)
                    if (marble1.node_value == marble2.node_value) & (marble1.node_value == marble3.node_value):
                        valid_marble_selections.add((marble1, marble3))
        return valid_marble_selections

    def is_valid_three_marble_move(self, move):
        result_start_node = self.get_node_in_direction_of_node(move.start_node, move.direction)  # location of start node after move
        result_end_node = self.get_node_in_direction_of_node(move.end_node, move.direction)  # location of end node after move

        middle_node = None
        for direction in Direction:
            if self.get_node_in_opposite_direction_of_node(move.end_node, direction) == \
                    self.get_node_in_direction_of_node(move.start_node, direction):
                middle_node = self.get_node_in_direction_of_node(move.start_node, direction)

        result_middle_node = self.get_node_in_direction_of_node(middle_node, move.direction)

        if move.is_inline_move():
            # push_node is the node that potentially will be pushed, so if A1-C1-TL, then it would be D1
            if result_middle_node == move.start_node:
                push_node = result_start_node
            else:
                push_node = result_end_node

            if push_node.node_value == NodeValue.INVALID:  # edge of board
                return False
            if push_node.node_value == NodeValue.EMPTY:
                return True

            # if node being pushed is opposite colour
            if push_node.node_value.value == abs(3 - move.start_node.node_value.value):

                # if node behind pushed node is empty or off the board (3 pushing 1)
                if (self.get_node_in_direction_of_node(push_node, move.direction).node_value == NodeValue.INVALID) | \
                        (self.get_node_in_direction_of_node(push_node, move.direction).node_value == NodeValue.EMPTY):
                    return True

                behind_push_node = self.get_node_in_direction_of_node(push_node, move.direction)

                # if node behind pushed node is also opposite colour
                if behind_push_node.node_value.value == abs(3 - move.start_node.node_value.value):

                    # if node behind pushed node is empty or off the board (3 pushing 2)
                    if (self.get_node_in_direction_of_node(behind_push_node, move.direction).node_value
                        == NodeValue.INVALID) | \
                            (self.get_node_in_direction_of_node(behind_push_node, move.direction).node_value
                             == NodeValue.EMPTY):
                        return True

        # sidestep move
        else:
            if (result_start_node.node_value == NodeValue.EMPTY) & \
                    (result_end_node.node_value == NodeValue.EMPTY) & \
                    (result_middle_node.node_value == NodeValue.EMPTY):
                return True
        return False

    def get_node_in_direction_of_node(self, node, direction):
        result_row = node.row + direction.value[0][0]
        result_column = node.column + direction.value[0][1]
        return self.state_rep.get_node(result_row, result_column)

    def get_node_in_opposite_direction_of_node(self, node, direction):
        result_row = node.row - direction.value[0][0]
        result_column = node.column - direction.value[0][1]
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
        Used when generating selections of 2 marbles in a row.
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
    print(stateSpaceGen.get_valid_three_marble_selections())
    print(stateSpaceGen.generate_three_marble_moves())
