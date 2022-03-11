from node import NodeValue, Node
from state_representation import StateRepresentation
from state_space_generator import StateSpaceGenerator


class FileProcessor:

    @staticmethod
    def get_state_rep_from_file(file_name):
        """
        Processes the given file and returns a StateRepresentation object.
        """
        lines = FileProcessor.read_lines_from_file(file_name)
        marble_list = FileProcessor.get_marble_list_from_lines(lines)
        curr_player, board = FileProcessor.get_player_and_board_from_marble_list(marble_list)
        return StateRepresentation(FileProcessor.get_player_num_from_color(curr_player).value,
                                   StateRepresentation.get_board_from_nodes(board))

    @staticmethod
    def read_lines_from_file(file_name):
        """
        Returns an array of lines.
        """
        lines = []
        with open(file_name, "r") as input_file:
            for line in input_file:
                lines.append(line)
        return lines

    @staticmethod
    def get_marble_list_from_lines(lines):
        """
        Returns an array which has the user as the first index.
        """
        player = lines[0].replace("\n", "")
        board = lines[1].replace("\n", "").split(",")
        return FileProcessor.flatten([player, board])

    @staticmethod
    def flatten(array):
        result = []
        for item in array:
            if isinstance(item, list):
                result.extend(FileProcessor.flatten(item))
            else:
                result.append(item)
        return result

    @staticmethod
    def get_player_num_from_color(color_char):
        """
        Returns the corresponding NodeValue of the given color char.
        """
        return NodeValue.BLACK if color_char.lower() == "b" else NodeValue.WHITE

    @staticmethod
    def get_player_and_board_from_marble_list(marble_list):
        """
        Returns a list consisting of Nodes representing marbles.
        """
        curr_player = marble_list.pop(0)
        nodes_list = []
        for marble in marble_list:
            row = int(Node.get_row_from_alpha(marble[0]))
            col = int(marble[1])
            node_val = FileProcessor.get_player_num_from_color(marble[2])
            new_node = Node(node_val, row, col)
            nodes_list.append(new_node)
        return curr_player, nodes_list

    @staticmethod
    def create_move_file(file_name, moves_list):
        """
        This method will create the Test<#>.move file.

        :param file_name: name of file to create
        :param moves_list: a list of Move objects.
        """
        new_file_name = file_name.split(".")[0] + ".move"
        with open(new_file_name, "w") as f:
            for move in moves_list:
                f.write(str(move) + "\n")

    @staticmethod
    def create_board_file(file_name, state_space):
        """
        This method will create the Test<#>.board file.

        :param file_name: name of file to create
        :param state_space: a set of StateRepresentation objects.
        """
        new_file_name = file_name.split(".")[0] + ".board"
        with open(new_file_name, "w+") as f:
            for state in state_space:
                data = [
                    str(FileProcessor.sort_marbles_for_player(state.get_all_marbles_for_player(NodeValue.BLACK.value)))
                        .replace("[", "").replace("]", "").replace(" ", "").replace("[", "").replace("]", ""),
                    str(FileProcessor.sort_marbles_for_player(state.get_all_marbles_for_player(NodeValue.WHITE.value)))
                        .replace("[", "").replace("]", "").replace(" ", "").replace("[", "").replace("]", "")
                ]
                data_string_version = str(data).replace("[", "").replace("]", "").replace(" ", "").replace("'", "") \
                                      + "\n"
                f.write(data_string_version)

    @staticmethod
    def sort_marbles_for_player(marbles_for_player):
        return sorted(marbles_for_player, key=lambda node: (-node.row, node.column))


if __name__ == "__main__":
    state_rep = FileProcessor.get_state_rep_from_file("test_inputs/Test1.input")
    state_space_gen = StateSpaceGenerator(state_rep)

    valid_moves_list = state_space_gen.generate_all_valid_moves()
    for valid_move in valid_moves_list:
        print(valid_move)
    FileProcessor.create_move_file("Test1", valid_moves_list)

    new_state_space = state_space_gen.generate_state_space()
    for new_state in new_state_space:
        print(new_state)
    FileProcessor.create_board_file("Test1", new_state_space)
