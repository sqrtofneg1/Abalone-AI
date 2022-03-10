from file_reader import File
from move import Move, Direction
from state_representation import StateRepresentation


class StateSpaceGenerator:

    def __init__(self, state_rep):
        self.state_rep = state_rep

    @staticmethod
    def is_valid_move(move):
        pass

    def generate_state_space(self, state_rep):
        pass  # should return an array of Move objects

    def generate_one_marble_moves(self):
        curr_player_marbles = self.state_rep.get_all_marbles_for_player(self.state_rep.player)
        moves_generated = []
        for node in curr_player_marbles:
            direction_dict = self.get_adjacent_nodes_values(node)
            for direction, adj_node_value in direction_dict.items():
                if adj_node_value.value == 3:
                    moves_generated.append(Move(node, node, direction))
        return moves_generated

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

if __name__ == "__main__":
    import node_arrays
    stateSpaceGen = StateSpaceGenerator(StateRepresentation.get_start_state_rep(node_arrays.DEFAULT_START))
    # print(stateSpaceGen.generate_one_marble_moves())    # implement a way to sort move outputs alphabetically?
    # file = File("Test1.txt")
    # file.create_move_file(stateSpaceGen.generate_one_marble_moves())
    # file.create_board_file()
    # print(stateSpaceGen.state_rep)
    # print(stateSpaceGen.state_rep._board)
    # print(stateSpaceGen.state_rep.get_all_marbles_for_player(1)[0].get_front_end_coords() + stateSpaceGen.state_rep.get_all_marbles_for_player(1)[0]._node_value.)
    print(stateSpaceGen.state_rep.get_all_marbles_for_player(2))
    print(stateSpaceGen.state_rep.sort_all_marbles_for_player(stateSpaceGen.state_rep.get_all_marbles_for_player(2)))

