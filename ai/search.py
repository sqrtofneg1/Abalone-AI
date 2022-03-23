"""
This module houses the adversarial search algorithm implementation
for Abalone AI - Minimax and Alpha-Beta pruning.
"""
from random import Random

from state_space_gen.file_processor import FileProcessor
from state_space_gen.state_space_generator import StateSpaceGenerator


class MinimaxAlphaBeta:
    """
    Represents an adversarial search algorithm
    using Minimax with Alpha-Beta pruning.
    """

    def __init__(self, max_depth=2):
        """
        Initializes an object of this class.

        :param max_depth: an int of
        """
        self._max_depth = max_depth
        self._cache = {}  # transposition table

    @property
    def max_depth(self):
        """
        Returns the max depth of this search algorithm.

        :return: an int
        """
        return self._max_depth

    @max_depth.setter
    def max_depth(self, new_max):
        """
        Sets the max depth to a new number.

        :param new_max: an int
        """
        self._max_depth = new_max

    @property
    def cache(self):
        """
        Returns the transposition table (cache).

        :return: a dictionary
        """
        return self._cache

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
        next_states_values_dict = {}

        for next_state in next_states:
            next_state_depth = next_state, state_depth[1] + 1
            next_states_values_dict.update({next_state: self.min_value(next_state_depth)})

        max_value = max(next_states_values_dict.values())
        max_valued_states = [s for s, v in next_states_values_dict.items() if v == max_value]
        chosen_state = max_valued_states[Random.randint(Random(), 0, len(max_valued_states) - 1)]
        chosen_move = moves[next_states.index(chosen_state)]

        # TEST: log results to console
        logging.info(f"Max value: {max_value}\nMove: {chosen_move}"
                     f"\nMax Result State:{chosen_state}")

        return chosen_move

    def max_value(self, state_depth):
        """
        For the given state, returns the highest value obtainable from the next states,
        from the current player's perspective.

        :param state_depth: a tuple with a State and an int for depth
        :return: an int of the highest value obtainable from next states
        """
        if self.is_terminal(state_depth):
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
        if self.is_terminal(state_depth):
            return self.get_value(state_depth[0])

        value = float('inf')
        generator = StateSpaceGenerator(state_depth[0])
        next_states = generator.generate_state_space()

        for next_state in next_states:
            next_state_depth = next_state, state_depth[1] + 1
            value = min(value, self.max_value(next_state_depth))

        return value

    def is_terminal(self, state_depth):
        """
        Checks if this state is considered terminal (at max depth).

        :param state_depth: a tuple with a State and an int for depth
        :return: True if state is at max depth, otherwise False
        """
        return state_depth[1] == self._max_depth

    def get_value(self, state):
        """
        Returns the estimated value of this state according to heuristic functions.

        :param state: a State object
        :return: an int of the value of this state
        """
        if state in self.cache:
            return self.cache[state]  # avoids recalculating previously seen states
        # return heuristic-evaluated value of this state
        value = Random.randint(Random(), 1, 100)  # PLACEHOLDER: randomize a value
        self.cache.update({state: value})
        return value


if __name__ == "__main__":
    from time import perf_counter
    from sys import stdout
    import logging

    # TEST: run algo with test input file
    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(stdout)])
    search_algo = MinimaxAlphaBeta()
    start = perf_counter()  # TEST: start timer
    search_algo.minimax_decision(
        FileProcessor.get_state_from_file("../dist/test_inputs/Test1.input"))
    end = perf_counter()  # TEST: end timer
    logging.info(f"Time taken: {end - start}")
