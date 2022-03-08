def read_from_file(file_name):
    """
    Returns an array of lines.
    @params: file_name: String.
    """
    lines = []
    file_reader = open(file_name, "r")
    for line in file_reader:
        lines.append(line)
    file_reader.close()
    return lines


def parse_test_file(file_name):
    """
    Returns an array which has the user as the first index.
    @params: file_name: String.
    """
    lines = read_from_file(file_name)
    player = lines[0].replace("\n", "")
    board = lines[1].replace("\n", "").split(",")
    return flatten([player, board])


def flatten(array):
    rt = []
    for item in array:
        if isinstance(item, list):
            rt.extend(flatten(item))
        else:
            rt.append(item)
    return rt


print(parse_test_file("./test_inputs/Test1.input"))
