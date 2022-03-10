from node import NodeValue
from state_representation import StateRepresentation
from state_space_generator import StateSpaceGenerator


def flatten(array):
    rt = []
    for item in array:
        if isinstance(item, list):
            rt.extend(flatten(item))
        else:
            rt.append(item)
    return rt


class File:

    def __init__(self, file_name):
        """
        A constructor that helps build and initializes its variables.
        :param file_name: A String that represents a name of the file
        """
        self._file_name = file_name

    def read_from_file(self):
        """
        Returns an array of lines.
        @params: file_name: String.
        """
        lines = []
        file = open(self._file_name, "r")
        for line in file:
            lines.append(line)
        file.close()
        return lines

    def parse_test_file(self):
        """
        Returns an array which has the user as the first index.
        @params: file_name: String.
        """
        lines = self.read_from_file()
        player = lines[0].replace("\n", "")
        board = lines[1].replace("\n", "").split(",")
        return flatten([player, board])

    def create_move_file(self, list_of_moves):
        """
        This method will create the Test<#>.move txt file.
        :param list_of_moves: a list of Move objects.
        """
        new_file_name = self._file_name.split(".")[0] + ".move"
        f = open(new_file_name, "w")
        for move in list_of_moves:
            f.write(str(move) + "\n")
        f.close()

    def create_board_file(self, set_of_state_representation):
        """
        This method will create the Test<#>.board txt file.
        :param set_of_state_representation: a set of StateRepresentation objects.
        """
        new_file_name = self._file_name.split(".")[0] + ".board"
        f = open(new_file_name, "a+")
        for state_representation in set_of_state_representation:
            data = [str(state_representation.sort_all_marbles_for_player(
                state_representation.get_all_marbles_for_player(NodeValue.BLACK.value)))
                        .replace("[", "").replace("]", "").replace(" ",
                                                                   "").replace("[", "").replace("]", ""),
                    str(state_representation.sort_all_marbles_for_player(
                        state_representation.get_all_marbles_for_player(NodeValue.WHITE.value)))
                        .replace("[", "").replace("]", "").replace(" ",
                                                                   "").replace("[", "").replace("]", "")]
            data_string_version = str(data).replace("[", "").replace("]", "").replace(" ", "").replace("'", "") + "\n"
            f.write(data_string_version)
        f.close()


if __name__ == "__main__":
    import node_arrays

    stateSpaceGen = StateSpaceGenerator(StateRepresentation.get_start_state_rep(node_arrays.DEFAULT_START))
    # print(stateSpaceGen.generate_one_marble_moves())
    # print(stateSpaceGen.state_rep.get_all_marbles_for_player(2))
    file = File("Test1.input")
    file.read_from_file()
    file.create_board_file(stateSpaceGen.generate_state_space())
    # print(file.parse_test_file())
