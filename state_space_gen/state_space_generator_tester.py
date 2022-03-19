"""
This module drives the testing of the State Space Generator.
"""
import os

if __name__ == "__main__":
    from os import listdir
    from os.path import isfile, join
    import sys
    from file_processor import FileProcessor
    from state_space_generator import StateSpaceGenerator

    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(__file__)

    directory_name = f"{application_path}/test_inputs"

    all_test_inputs = [f for f in listdir(directory_name) if isfile(join(directory_name, f))]
    for test_input_file_name in all_test_inputs:
        file_path = f"{directory_name}/{test_input_file_name}"

        state = FileProcessor.get_state_from_file(file_path)

        state_space_gen = StateSpaceGenerator(state)
        valid_moves_list = state_space_gen.generate_all_valid_moves()
        resulting_state_spaces = state_space_gen.generate_state_space()

        FileProcessor.create_move_file(test_input_file_name, valid_moves_list)
        FileProcessor.create_board_file(test_input_file_name, resulting_state_spaces)
