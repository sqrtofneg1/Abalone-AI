"""
This module houses the StateSpaceGenerator class.
"""

from core.node import NodeValue
from core.move import Move, Direction, MoveType, ChangeMatrix
from core.state import State


class StateSpaceGenerator:
    """
    Responsible for generating all legal moves for a given state, and
    applying those moves to create the resulting states.
    """

    def __init__(self, state):
        """
        Initializes a StateSpaceGenerator object.

        :param state: a State object
        """
        self._state = state

    @property
    def state(self):
        """
        Returns the state used by this generator class.

        :return: a State object
        """
        return self._state

    def generate_state_space(self):
        """
        Generates all legal resulting states from the starting state.

        :return: a list of States
        """
        all_valid_moves = self.generate_all_valid_moves()
        state_space = [self.state.apply_move(move) for move in all_valid_moves]
        return state_space

    def generate_all_valid_moves(self):
        """
        Generates all legal moves from the starting state.

        :return: a list of Moves
        """
        all_valid_moves = []
        all_valid_moves.extend(self.generate_one_marble_moves())
        all_valid_moves.extend(self.generate_multi_marbles_moves())
        return all_valid_moves

    def generate_one_marble_moves(self):
        """
        Generates all legal one-marble moves.

        :return: a list of Moves
        """
        curr_player_marbles = self.state.get_all_nodes_for_player(self.state.player)
        valid_moves = []
        for node in curr_player_marbles:
            direction_dict = self.get_adjacent_nodes(node)
            for direction, adj_node in direction_dict.items():
                if adj_node.node_value == NodeValue.EMPTY:
                    change_matrix = ChangeMatrix(self.state.player,
                                                 [node],
                                                 [adj_node])
                    valid_moves.append(Move(MoveType.Inline, node, node, direction, change_matrix))
        return valid_moves

    def generate_multi_marbles_moves(self):
        """
        Generates all legal two and three marble moves.

        :return: a list of Moves
        """
        two_marble_selections = self.get_valid_two_marble_selections()
        two_marble_incomplete_moves_generator = (Move(MoveType.Unknown, node1, node2, direction)
                                                 for (node1, node2) in two_marble_selections
                                                 for direction in Direction)
        two_marble_moves = [self.process_two_marble_move(move)
                            for move in two_marble_incomplete_moves_generator]
        valid_moves = [move for move in two_marble_moves if move.move_type != MoveType.Invalid]

        three_marble_selections = self.get_valid_three_marble_selections()
        three_marble_incomplete_moves_generator = (Move(MoveType.Unknown, node1, node2, direction)
                                                   for (node1, node2) in three_marble_selections
                                                   for direction in Direction)
        three_marble_moves = [self.process_three_marble_move(move)
                              for move in three_marble_incomplete_moves_generator]
        valid_moves.extend([move for move in three_marble_moves if move.move_type != MoveType.Invalid])
        return valid_moves

    def get_valid_two_marble_selections(self):
        """
        Returns a set of tuples of nodes (Node1, Node2) for all valid 2 marble selections
        for the current player.

        :return: a set of tuples of Nodes, the valid selections for two marbles
        """
        curr_player_marbles = self.state.get_all_nodes_for_player(self.state.player)
        return [(marble1, marble2) for marble1 in curr_player_marbles for marble2 in self.get_left_nodes(marble1)
                if marble1.node_value == marble2.node_value]

    def process_two_marble_move(self, move):
        """
        Determines the type and change matrix (if applicable) of
        the given two-marble move.

        :param move: a Move object
        :return: a Move object
        """
        moved_start_node = self.state.get_node_in_direction_of_node(
            move.start_node, move.direction)  # location of start node after move
        moved_end_node = self.state.get_node_in_direction_of_node(
            move.end_node, move.direction)  # location of end node after move

        if move.is_inline_move():
            # first_pushed_node is the node that potentially will be pushed, so if A1-B1-TL, then it would be C1
            first_pushed_node = moved_start_node if moved_end_node == move.start_node else moved_end_node

            if first_pushed_node.node_value == NodeValue.INVALID:  # edge of board
                return Move(MoveType.Invalid, move.start_node, move.end_node, move.direction)
            if first_pushed_node.node_value == NodeValue.EMPTY:
                change_matrix = ChangeMatrix(self.state.player,
                                             [move.start_node, move.end_node],
                                             [moved_start_node, moved_end_node])
                return Move(MoveType.Inline, move.start_node, move.end_node, move.direction, change_matrix)
            # if node being pushed is opposite colour
            if first_pushed_node.node_value.value == abs(3 - move.start_node.node_value.value):
                node_behind_pushed_node = self.state.get_node_in_direction_of_node(first_pushed_node,
                                                                                   move.direction)
                # if node behind pushed node is empty or off the board
                if node_behind_pushed_node.node_value == NodeValue.INVALID:
                    change_matrix = ChangeMatrix(self.state.player,
                                                 [move.start_node, move.end_node],
                                                 [moved_start_node, moved_end_node])
                    return Move(MoveType.Scoring, move.start_node, move.end_node, move.direction, change_matrix)
                if node_behind_pushed_node.node_value == NodeValue.EMPTY:
                    change_matrix = ChangeMatrix(self.state.player,
                                                 [move.start_node, move.end_node],
                                                 [moved_start_node, moved_end_node],
                                                 [node_behind_pushed_node])
                    return Move(MoveType.Push, move.start_node, move.end_node, move.direction, change_matrix)
        # sidestep move
        else:
            if (moved_start_node.node_value == NodeValue.EMPTY) \
                    and (moved_end_node.node_value == NodeValue.EMPTY):
                change_matrix = ChangeMatrix(self.state.player,
                                             [move.start_node, move.end_node],
                                             [moved_start_node, moved_end_node])
                return Move(MoveType.Sidestep, move.start_node, move.end_node, move.direction, change_matrix)
        return Move(MoveType.Invalid, move.start_node, move.end_node, move.direction)

    def get_valid_three_marble_selections(self):
        """
        Returns a set of tuples of nodes (Node1, Node2) for all valid 3 marble selections
        for the current player.

        :return: a set of tuples of nodes, the valid selections for three marbles
        """
        valid_marble_selections = []
        curr_player_marbles = self.state.get_all_nodes_for_player(self.state.player)
        for marble1 in curr_player_marbles:
            for direction in Direction.left_directions():
                marble2 = self.state.get_node_in_direction_of_node(marble1, direction)
                if marble2.node_value is not NodeValue.INVALID:
                    marble3 = self.state.get_node_in_direction_of_node(marble2, direction)
                    if (marble1.node_value == marble2.node_value) & (marble1.node_value == marble3.node_value):
                        valid_marble_selections.append((marble1, marble3))
        return valid_marble_selections

    def process_three_marble_move(self, move):
        """
        Determines the type and change matrix (if applicable) of
        the given three-marble move.

        :param move: a Move object
        :return: a Move object
        """
        moved_start_node = self.state.get_node_in_direction_of_node(
            move.start_node, move.direction)  # location of start node after move
        moved_end_node = self.state.get_node_in_direction_of_node(
            move.end_node, move.direction)  # location of end node after move
        middle_node = None
        for direction in Direction:
            if self.state.get_node_in_opposite_direction_of_node(move.end_node, direction) \
                    == self.state.get_node_in_direction_of_node(move.start_node, direction):
                middle_node = self.state.get_node_in_direction_of_node(move.start_node, direction)

        result_middle_node = self.state.get_node_in_direction_of_node(middle_node, move.direction)

        if move.is_inline_move():
            # first_pushed_node is the node that potentially will be pushed, so if A1-C1-TL, then it would be D1
            first_pushed_node = moved_start_node if result_middle_node == move.start_node \
                else moved_end_node

            if first_pushed_node.node_value == NodeValue.INVALID:  # edge of board
                return Move(MoveType.Invalid, move.start_node, move.end_node, move.direction)
            if first_pushed_node.node_value == NodeValue.EMPTY:
                change_matrix = ChangeMatrix(
                    self.state.player,
                    [move.start_node, middle_node, move.end_node],
                    [moved_start_node, result_middle_node, moved_end_node])
                return Move(MoveType.Inline, move.start_node, move.end_node, move.direction, change_matrix)
            # if first_pushed_node is opposite colour
            if first_pushed_node.node_value.value == abs(3 - move.start_node.node_value.value):
                # second_pushed_node is the node behind first_pushed_node
                second_pushed_node = self.state.get_node_in_direction_of_node(first_pushed_node, move.direction)
                # if second_pushed_node is off the board or an empty space (3 pushing 1)
                if second_pushed_node.node_value == NodeValue.INVALID:
                    change_matrix = ChangeMatrix(
                        self.state.player,
                        [move.start_node, middle_node, move.end_node],
                        [moved_start_node, result_middle_node, moved_end_node])
                    return Move(MoveType.Scoring, move.start_node, move.end_node, move.direction, change_matrix)
                if second_pushed_node.node_value == NodeValue.EMPTY:
                    change_matrix = ChangeMatrix(
                        self.state.player,
                        [move.start_node, middle_node, move.end_node],
                        [moved_start_node, result_middle_node, moved_end_node],
                        [second_pushed_node])
                    return Move(MoveType.Push, move.start_node, move.end_node, move.direction, change_matrix)
                # if second_pushed_node is also opposite colour
                if second_pushed_node.node_value.value == abs(3 - move.start_node.node_value.value):
                    node_behind_second_pushed_node = self.state.get_node_in_direction_of_node(second_pushed_node,
                                                                                              move.direction)
                    # and if the node behind second_pushed_node is off the board or an empty space (3 pushing 2)
                    if node_behind_second_pushed_node.node_value == NodeValue.INVALID:
                        change_matrix = ChangeMatrix(
                            self.state.player,
                            [move.start_node, middle_node, move.end_node],
                            [moved_start_node, result_middle_node, moved_end_node],
                            [second_pushed_node])
                        return Move(MoveType.Scoring, move.start_node, move.end_node, move.direction, change_matrix)
                    if node_behind_second_pushed_node.node_value == NodeValue.EMPTY:
                        change_matrix = ChangeMatrix(
                            self.state.player,
                            [move.start_node, middle_node, move.end_node],
                            [moved_start_node, result_middle_node, moved_end_node],
                            [second_pushed_node, node_behind_second_pushed_node])
                        return Move(MoveType.Push, move.start_node, move.end_node, move.direction, change_matrix)
        # sidestep move
        else:
            if (moved_start_node.node_value == NodeValue.EMPTY) & \
                    (moved_end_node.node_value == NodeValue.EMPTY) & \
                    (result_middle_node.node_value == NodeValue.EMPTY):
                change_matrix = ChangeMatrix(
                    self.state.player,
                    [move.start_node, middle_node, move.end_node],
                    [moved_start_node, result_middle_node,
                     moved_end_node])
                return Move(MoveType.Sidestep, move.start_node, move.end_node, move.direction, change_matrix)
        return Move(MoveType.Invalid, move.start_node, move.end_node, move.direction)

    def get_adjacent_nodes(self, node):
        """
        Returns a dictionary with the adjacent nodes in all 6 directions.

        :param node: a Node
        :return: dictionary of direction : adjacent nodes
        """
        return {direction: self.state.get_node_in_direction_of_node(node, direction)
                for direction in Direction}

    def get_left_nodes(self, node):
        """
        Returns a set with the adjacent nodes in left directions (TL, L, BL).
        Used when generating selections of 2 marbles in a row.

        :param node: a Node
        :return: set of Nodes in the left directions
        """
        return {self.state.get_node_in_direction_of_node(node, direction) for direction in
                Direction.left_directions()}


if __name__ == "__main__":
    # run from this file for a quick test of the state space generator using a test layout
    from layouts import layout_arrays

    stateSpaceGen = StateSpaceGenerator(State.get_start_state(layout_arrays.PUSHABLE_TEST_START))
    print("One Marble Moves:\n",
          sorted(stateSpaceGen.generate_one_marble_moves(), key=lambda move: move.start_node.get_front_end_coords()))
    print("Two Marble Selections:\n",
          sorted(stateSpaceGen.get_valid_two_marble_selections(),
                 key=lambda selection: selection[0].get_front_end_coords()))
    print("Three Marble Selections:\n",
          sorted(stateSpaceGen.get_valid_three_marble_selections(),
                 key=lambda selection: selection[0].get_front_end_coords()))
    print("Two & Three Marble Moves:\n",
          sorted(stateSpaceGen.generate_multi_marbles_moves(), key=lambda move: move.start_node.get_front_end_coords()))
    print("\n", stateSpaceGen.generate_state_space())
