"""
This module houses the FileProcessor class.
"""
from core.node import NodeValue, Node
from core.state import State
from state_space_gen.state_space_generator import StateSpaceGenerator


class FileProcessor:
    """
    Responsible for taking input test files, converting the data into
    a State, then taking the output of the State Space Generator to
    write to output files.
    """

    @staticmethod
    def get_state_from_file(file_name):
        """
        Processes the given file and returns a State object.

        :param file_name: a string of the file name
        :return: a State object
        """
        lines = FileProcessor.read_lines_from_file(file_name)
        marble_list = FileProcessor.get_marble_list_from_lines(lines)
        curr_player, board = FileProcessor.get_player_and_board_from_marble_list(marble_list)
        return State(FileProcessor.get_player_num_from_color(curr_player).value,
                     State.get_board_from_nodes(board))

    @staticmethod
    def read_lines_from_file(file_name):
        """
        Reads and returns lines from the given file.

        :param file_name: a string of the file name
        :return: a list of strings read from file
        """
        lines = []
        with open(file_name, "r") as input_file:
            for line in input_file:
                lines.append(line)
        return lines

    @staticmethod
    def get_marble_list_from_lines(lines):
        """
        Returns a list with the current player as the first index,
        followed by the marbles on the board.

        :param lines: a list of strings read from file
        :return: a list of strings
        """
        player = lines[0].replace("\n", "")
        board = lines[1].replace("\n", "").split(",")
        result = []
        for item in [player, board]:
            if isinstance(item, list):
                result.extend(item)
            else:
                result.append(item)
        return result

    @staticmethod
    def get_player_num_from_color(color_char):
        """
        Returns the corresponding NodeValue of the given color char.

        :param color_char: a character equal to 'b' or 'w'
        :return: a NodeValue equal to BLACK or WHITE
        """
        return NodeValue.BLACK if color_char.lower() == "b" else NodeValue.WHITE

    @staticmethod
    def get_player_and_board_from_marble_list(marble_list):
        """
        Returns a list consisting of Nodes representing marbles.

        :param marble_list: a list of strings with current player at first index
        :return: a tuple of the current player and a list of Nodes
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
        with open(f"test_outputs/{new_file_name}", "w") as f:
            for move in moves_list:
                f.write(str(move) + "\n")

    @staticmethod
    def create_board_file(file_name, state_space):
        """
        This method will create the Test<#>.board file.

        :param file_name: name of file to create
        :param state_space: a set of State objects.
        """
        new_file_name = file_name.split(".")[0] + ".board"
        with open(f"test_outputs/{new_file_name}", "w+") as f:
            for state in state_space:
                data = [
                    str(FileProcessor.sort_marbles_for_player(state.get_all_nodes_for_player(NodeValue.BLACK.value)))
                        .replace("[", "").replace("]", "").replace(" ", "").replace("[", "").replace("]", ""),
                    str(FileProcessor.sort_marbles_for_player(state.get_all_nodes_for_player(NodeValue.WHITE.value)))
                        .replace("[", "").replace("]", "").replace(" ", "").replace("[", "").replace("]", "")
                ]
                data_string_version = str(data).replace("[", "").replace("]", "").replace(" ", "").replace("'", "") \
                                      + "\n"
                f.write(data_string_version)

    @staticmethod
    def sort_marbles_for_player(marbles_for_player):
        """
        Returns a sorted list of marbles.

        :param marbles_for_player: a list of marbles for one player
        :return: a sorted list of marbles
        """
        return sorted(marbles_for_player, key=lambda node: (-node.row, node.column))


if __name__ == "__main__":
    start_state = FileProcessor.get_state_from_file("../dist/test_inputs/Test1.input")
    state_space_gen = StateSpaceGenerator(start_state)

    valid_moves_list = state_space_gen.generate_all_valid_moves()
    for valid_move in valid_moves_list:
        print(valid_move)
    FileProcessor.create_move_file("Test1", valid_moves_list)

    new_state_space = state_space_gen.generate_state_space()
    for new_state in new_state_space:
        print(new_state)
    FileProcessor.create_board_file("Test1", new_state_space)
