"""
This module houses the adversarial search implementations
for Abalone AI - Minimax and Alpha-Beta pruning.
"""
from random import Random

from state_space_gen.file_processor import FileProcessor
from state_space_gen.state_space_generator import StateSpaceGenerator


class MinimaxAlphaBeta:
    """
    Represents a search algorithm using Minimax with Alpha-Beta pruning.
    """

    def __init__(self, max_depth=2):
        self._max_depth = max_depth

    def minimax_decision(self, state):
        """
        Returns the estimated-best-next-move the player can make using
        minimax algorithm.

        :param state: a State object
        :return: a Move object
        """
        state_depth = state, 0
        generator = StateSpaceGenerator(state_depth[0])
        moves = generator.generate_all_valid_moves()
        next_states = generator.generate_next_states()
        min_values_dict = {}

        for next_state in next_states:
            next_state_depth = next_state, state_depth[1] + 1
            min_values_dict.update({self.min_value(next_state_depth): next_state})

        max_value = max(min_values_dict.keys())
        max_valued_state = min_values_dict[max_value]
        max_valued_move = moves[next_states.index(max_valued_state)]
        print(f"Max value: {max_value}\nMove: {max_valued_move}\nMax Result State:{max_valued_state}")

        return max_valued_move

    def max_value(self, state_depth):
        """
        For the given state, returns the highest value obtainable from the next states,
        from the current player's perspective.

        :param state_depth: a tuple with a State and an int for depth
        :return: an int of the highest value obtainable from next states
        """
        if self.is_terminal(state_depth[1]):
            return self.get_value(state_depth[0])

        value = float('-inf')
        generator = StateSpaceGenerator(state_depth[0])
        next_states = generator.generate_state_space()

        for next_state in next_states:
            next_state_depth = next_state, state_depth[1] + 1
            value = max(value, self.min_value(next_state_depth))

        return value

    def min_value(self, state_depth):
        """
        For the given state, returns the lowest value obtainable from the next states,
        from the current player's perspective.

        :param state_depth: a tuple with a State and an int for depth
        :return: an int of the lowest value obtainable from next states
        """
        if self.is_terminal(state_depth[1]):
            return self.get_value(state_depth)

        value = float('inf')
        generator = StateSpaceGenerator(state_depth[0])
        next_states = generator.generate_state_space()

        for next_state in next_states:
            next_state_depth = next_state, state_depth[1] + 1
            value = min(value, self.max_value(next_state_depth))

        return value

    def is_terminal(self, depth):
        return depth == self._max_depth

    def get_value(self, state_depth):
        # return heuristic-evaluated value of this state
        return Random.randint(Random(), 1, 100)     # placeholder: randomize a value


if __name__ == "__main__":
    # testing
    search_algo = MinimaxAlphaBeta()
    search_algo.minimax_decision(
        FileProcessor.get_state_from_file("../dist/test_inputs/Test1.input"))
