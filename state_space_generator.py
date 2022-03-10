from copy import deepcopy

from node import NodeValue
from move import Move, Direction, MoveType
from move import Move, Direction
from state_representation import StateRepresentation


class StateSpaceGenerator:

    def __init__(self, state_rep):
        self.state_rep = state_rep

    @staticmethod
    def generate_change_matrix_from_nodes(moving_player, original_positions, new_positions, pushed_nodes=None):
        players_dict = {1: NodeValue.BLACK,
                        2: NodeValue.WHITE}
        change_matrix = [[NodeValue.INVALID for row in range(11)] for column in range(11)]
        for node in original_positions:
            change_matrix[node.row][node.column] = NodeValue.EMPTY
        for node in new_positions:
            change_matrix[node.row][node.column] = players_dict[moving_player]
        if pushed_nodes:
            other_player = 2 if moving_player == 1 else 1
            for node in pushed_nodes:
                change_matrix[node.row][node.column] = players_dict[other_player]
        return change_matrix

    def generate_state_space(self):
        all_valid_moves = set()
        all_valid_moves.update(self.generate_one_marble_moves())
        all_valid_moves.update(self.generate_multi_marbles_moves())
        state_space = {self.apply_move(move) for move in all_valid_moves}
        print(next(iter(state_space)))
        return state_space

    def generate_one_marble_moves(self):
        curr_player_marbles = self.state_rep.get_all_marbles_for_player(self.state_rep.player)
        moves_generated = set()
        for node in curr_player_marbles:
            direction_dict = self.get_adjacent_nodes(node)
            for direction, adj_node in direction_dict.items():
                if adj_node.node_value == NodeValue.EMPTY:
                    change_matrix = self.generate_change_matrix_from_nodes(self.state_rep.player,
                                                                           [node],
                                                                           [adj_node])
                    moves_generated.add(Move(MoveType.Inline, node, node, direction, change_matrix))
        return moves_generated

    def generate_multi_marbles_moves(self):
        two_marble_selections = self.get_valid_two_marble_selections()
        two_marble_incomplete_moves_generator = (Move(MoveType.Unknown, node1, node2, direction)
                                                 for (node1, node2) in two_marble_selections
                                                 for direction in Direction)
        two_marble_moves = {self.process_two_marble_move(move)
                            for move in two_marble_incomplete_moves_generator}
        valid_moves = {move for move in two_marble_moves if move.move_type != MoveType.Invalid}

        three_marble_selections = self.get_valid_three_marble_selections()
        three_marble_incomplete_moves_generator = (Move(MoveType.Unknown, node1, node2, direction)
                                                   for (node1, node2) in three_marble_selections
                                                   for direction in Direction)
        three_marble_moves = {self.process_three_marble_move(move)
                              for move in three_marble_incomplete_moves_generator}
        return valid_moves.union({move for move in three_marble_moves if move.move_type != MoveType.Invalid})

    def get_valid_two_marble_selections(self):
        """
        Returns a set of tuples of nodes (Node1, Node2) for all valid 2 marble selections
        for the current player.
        :return: a set of tuples of nodes, the valid selections for two marbles
        """
        curr_player_marbles = self.state_rep.get_all_marbles_for_player(self.state_rep.player)
        return {(marble1, marble2) for marble1 in curr_player_marbles for marble2 in self.get_left_nodes(marble1)
                if marble1.node_value == marble2.node_value}

    def process_two_marble_move(self, move):
        moved_start_node = self.get_node_in_direction_of_node(move.start_node,
                                                              move.direction)  # location of start node after move
        moved_end_node = self.get_node_in_direction_of_node(move.end_node,
                                                            move.direction)  # location of end node after move
        if move.is_inline_move():
            # first_pushed_node is the node that potentially will be pushed, so if A1-B1-TL, then it would be C1
            first_pushed_node = moved_start_node if moved_end_node == move.start_node else moved_end_node

            if first_pushed_node.node_value == NodeValue.INVALID:  # edge of board
                return Move(MoveType.Invalid, move.start_node, move.end_node, move.direction)
            if first_pushed_node.node_value == NodeValue.EMPTY:
                change_matrix = self.generate_change_matrix_from_nodes(self.state_rep.player,
                                                                       [move.start_node, move.end_node],
                                                                       [moved_start_node, moved_end_node])
                return Move(MoveType.Inline, move.start_node, move.end_node, move.direction, change_matrix)
            # if node being pushed is opposite colour
            if first_pushed_node.node_value.value == abs(3 - move.start_node.node_value.value):
                node_behind_pushed_node = self.get_node_in_direction_of_node(first_pushed_node, move.direction)
                # if node behind pushed node is empty or off the board
                if node_behind_pushed_node.node_value == NodeValue.INVALID:
                    change_matrix = self.generate_change_matrix_from_nodes(self.state_rep.player,
                                                                           [move.start_node, move.end_node],
                                                                           [moved_start_node, moved_end_node])
                    return Move(MoveType.Scoring, move.start_node, move.end_node, move.direction, change_matrix)
                if node_behind_pushed_node.node_value == NodeValue.EMPTY:
                    change_matrix = self.generate_change_matrix_from_nodes(self.state_rep.player,
                                                                           [move.start_node, move.end_node],
                                                                           [moved_start_node, moved_end_node],
                                                                           [node_behind_pushed_node])
                    return Move(MoveType.Push, move.start_node, move.end_node, move.direction, change_matrix)
        # sidestep move
        else:
            if (moved_start_node.node_value == NodeValue.EMPTY) \
                    and (moved_end_node.node_value == NodeValue.EMPTY):
                change_matrix = self.generate_change_matrix_from_nodes(self.state_rep.player,
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

    def process_three_marble_move(self, move):
        moved_start_node = self.get_node_in_direction_of_node(move.start_node,
                                                              move.direction)  # location of start node after move
        moved_end_node = self.get_node_in_direction_of_node(move.end_node,
                                                            move.direction)  # location of end node after move

        middle_node = None
        for direction in Direction:
            if self.get_node_in_opposite_direction_of_node(move.end_node, direction) \
                    == self.get_node_in_direction_of_node(move.start_node, direction):
                middle_node = self.get_node_in_direction_of_node(move.start_node, direction)

        result_middle_node = self.get_node_in_direction_of_node(middle_node, move.direction)

        if move.is_inline_move():
            # first_pushed_node is the node that potentially will be pushed, so if A1-C1-TL, then it would be D1
            first_pushed_node = moved_start_node if result_middle_node == move.start_node \
                else moved_end_node

            if first_pushed_node.node_value == NodeValue.INVALID:  # edge of board
                return Move(MoveType.Invalid, move.start_node, move.end_node, move.direction)
            if first_pushed_node.node_value == NodeValue.EMPTY:
                change_matrix = self.generate_change_matrix_from_nodes(
                    self.state_rep.player,
                    [move.start_node, middle_node, move.end_node],
                    [moved_start_node, result_middle_node, moved_end_node])
                return Move(MoveType.Inline, move.start_node, move.end_node, move.direction, change_matrix)
            # if first_pushed_node is opposite colour
            if first_pushed_node.node_value.value == abs(3 - move.start_node.node_value.value):
                # second_pushed_node is the node behind first_pushed_node
                second_pushed_node = self.get_node_in_direction_of_node(first_pushed_node, move.direction)
                # if second_pushed_node is off the board or an empty space (3 pushing 1)
                if second_pushed_node.node_value == NodeValue.INVALID:
                    change_matrix = self.generate_change_matrix_from_nodes(
                        self.state_rep.player,
                        [move.start_node, middle_node, move.end_node],
                        [moved_start_node, result_middle_node, moved_end_node])
                    return Move(MoveType.Scoring, move.start_node, move.end_node, move.direction, change_matrix)
                if second_pushed_node.node_value == NodeValue.EMPTY:
                    change_matrix = self.generate_change_matrix_from_nodes(
                        self.state_rep.player,
                        [move.start_node, middle_node, move.end_node],
                        [moved_start_node, result_middle_node, moved_end_node],
                        [second_pushed_node])
                    return Move(MoveType.Push, move.start_node, move.end_node, move.direction, change_matrix)
                # if second_pushed_node is also opposite colour
                if second_pushed_node.node_value.value == abs(3 - move.start_node.node_value.value):
                    node_behind_second_pushed_node = self.get_node_in_direction_of_node(second_pushed_node,
                                                                                        move.direction)
                    # and if the node behind second_pushed_node is off the board or an empty space (3 pushing 2)
                    if node_behind_second_pushed_node.node_value == NodeValue.INVALID:
                        change_matrix = self.generate_change_matrix_from_nodes(
                            self.state_rep.player,
                            [move.start_node, middle_node, move.end_node],
                            [moved_start_node, result_middle_node, moved_end_node],
                            [second_pushed_node])
                        return Move(MoveType.Scoring, move.start_node, move.end_node, move.direction, change_matrix)
                    if node_behind_second_pushed_node.node_value == NodeValue.EMPTY:
                        change_matrix = self.generate_change_matrix_from_nodes(
                            self.state_rep.player,
                            [move.start_node, middle_node, move.end_node],
                            [moved_start_node, result_middle_node, moved_end_node],
                            [second_pushed_node, node_behind_second_pushed_node])
                        return Move(MoveType.Push, move.start_node, move.end_node, move.direction, change_matrix)
        # sidestep move
        else:
            if (moved_start_node.node_value == NodeValue.EMPTY) & \
                    (moved_end_node.node_value == NodeValue.EMPTY) & \
                    (result_middle_node.node_value == NodeValue.EMPTY):
                change_matrix = self.generate_change_matrix_from_nodes(
                    self.state_rep.player,
                    [move.start_node, middle_node, move.end_node],
                    [moved_start_node, result_middle_node,
                     moved_end_node])
                return Move(MoveType.Sidestep, move.start_node, move.end_node, move.direction, change_matrix)
        return Move(MoveType.Invalid, move.start_node, move.end_node, move.direction)

    def apply_move(self, move):
        next_player = 2 if self.state_rep.player == 1 else 1
        new_state_rep = StateRepresentation(next_player, deepcopy(self.state_rep.board))
        if move.move_type == MoveType.Scoring:
            new_state_rep.scores[next_player - 1] += 1
        for row in new_state_rep.board:
            for node in row:
                if node.node_value.value:
                    new_val = move.change_matrix[node.row][node.column]
                    if new_val.value:
                        new_state_rep.board[node.row][node.column].node_value = new_val
        return new_state_rep

    def get_node_in_direction_of_node(self, node, direction):
        result_row = node.row + direction.value[0][0]
        result_column = node.column + direction.value[0][1]
        return self.state_rep.get_node(result_row, result_column)

    def get_node_in_opposite_direction_of_node(self, node, direction):
        result_row = node.row - direction.value[0][0]
        result_column = node.column - direction.value[0][1]
        return self.state_rep.get_node(result_row, result_column)

    def get_adjacent_nodes(self, node):
        """
        Returns a dictionary with the adjacent nodes in all 6 directions.
        :param node: a Node
        :return: dictionary of direction : adjacent nodes
        """
        return {direction: self.get_node_in_direction_of_node(node, direction)
                for direction in Direction}

    def get_left_nodes(self, node):
        """
        Returns a set with the adjacent nodes in left directions (TL, L, BL).
        Used when generating selections of 2 marbles in a row.
        :param node: a Node
        :return: set of Nodes in the left directions
        """
        return {self.get_node_in_direction_of_node(node, direction) for direction in Direction.left_directions()}

    @staticmethod
    def get_board_from_file(file_name):
        file_reader

if __name__ == "__main__":
    import node_arrays

    stateSpaceGen = StateSpaceGenerator(StateRepresentation.get_start_state_rep(node_arrays.PUSHABLE_START))
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
