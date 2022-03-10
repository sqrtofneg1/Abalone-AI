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
        new_file_name = self._file_name.split(".")[0] + ".move.txt"
        f = open(new_file_name, "w")
        for move in list_of_moves:
            f.write(str(move) + "\n")
        f.close()

    def create_board_file(self, list_of_state_representation):
        new_file_name = self._file_name.split(".")[0] + ".board.txt"
        data = set()
        f = open(new_file_name, "w")
        for state_representation in list_of_state_representation:
            data.add(
                str(state_representation.get_all_marbles_for_player(1)).replace("{", "").replace("}", "").replace(" ",
                                                                                                                  ""))
            data.add(
                str(state_representation.get_all_marbles_for_player(2)).replace("{", "").replace("}", "").replace(" ",
                                                                                                                  ""))
        f.write(data + "\n")
        f.close()


# print(parse_test_file("./test_inputs/Test1.input"))

# if __name__ == "__main__":
#     # import node_arrays
#     # stateSpaceGen = StateSpaceGenerator(StateRepresentation.get_start_state_rep(node_arrays.DEFAULT_START))
#     # print(stateSpaceGen.generate_one_marble_moves())    # implement a way to sort move outputs alphabetically?
#     file = File("./test_inputs/Test1.input")
#     file.read_from_file()
#     print(file.parse_test_file())
