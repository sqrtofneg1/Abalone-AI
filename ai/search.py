"""
This module houses the adversarial search algorithm implementation
for Abalone AI - Minimax and Alpha-Beta pruning.
"""
import math
from random import Random

import sys,os
sys.path.append(os.path.realpath('..'))
from state_space_gen.file_processor import FileProcessor
from state_space_gen.state_space_generator import StateSpaceGenerator
from ai.heuristics import HeuristicFunctionMan


class AlphaBeta:
    """
    Represents an adversarial search algorithm
    using Minimax with Alpha-Beta pruning.
    """

    def __init__(self, max_depth=2):
        """
        Initializes an object of this class.
        :param max_depth: an int of the max depth to search
        """
        self._max_depth = max_depth
        self._transpos_table = {}
        # performance trackers
        self.pruned = 0
        self.table_retrieved = 0

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
    def transpos_table(self):
        """
        Returns the transposition table.
        :return: a dictionary
        """
        return self._transpos_table

    def alpha_beta_search(self, state):
        """
        Returns the estimated-best-next-move the player can make using
        alpha-beta search algorithm.
        :param state: a State object
        :param max_depth: an int
        :return: a Move object
        """
        alpha, beta, value = float('-inf'), float('inf'), float('-inf')
        generator = StateSpaceGenerator(state)
        moves = generator.generate_all_valid_moves()
        next_states = generator.generate_next_states()
        next_states_values_dict = {}

        for next_state in next_states:
            next_state_depth = next_state, 1
            value = max(value, self.min_value(next_state_depth, alpha, beta))
            alpha = max(alpha, value)
            next_states_values_dict.update({next_state: value})

        max_valued_moves = [moves[next_states.index(s)]
                            for s, v in next_states_values_dict.items() if v == value]
        chosen_move = generator.sort_moves(max_valued_moves)[0]

        # TEST: log results to console
        # logging.info(f"Max value: {value}\nMove: {chosen_move}")

        return chosen_move

    def max_value(self, state_depth, alpha, beta):

        """
        For the given state, returns the highest value obtainable from the next states,
        from the current player's perspective.
        :param state_depth: a tuple with a State and an int for depth
        :param alpha: an int of the highest value found by max so far
        :param beta: an int of the lowest value found by min so far
        :param max_depth: an int
        :return: an int of the highest value obtainable from next states
        """
        if state_depth[1] == max_depth:
            return self.get_value(state_depth[0])

        value = -math.inf
        generator = StateSpaceGenerator(state_depth[0])
        moves = generator.generate_all_valid_moves()
        next_states = generator.generate_next_states()

        for next_state in next_states:
            next_state_depth = next_state, state_depth[1] + 1
            value = max(value, self.min_value(next_state_depth, alpha, beta))
            if value >= beta:
                self.pruned += 1
                return value
            alpha = max(alpha, value)

        return value

    def min_value(self, state_depth, alpha, beta):
        """
        For the given state, returns the lowest value obtainable from the next states,
        from the current player's perspective.
        :param state_depth: a tuple with a State and an int for depth
        :param alpha: an int of the highest value found by max so far
        :param beta: an int of the lowest value found by min so far
        :return: an int of the lowest value obtainable from next states
        """
        if self.is_terminal(state_depth):
            return self.get_value(state_depth[0])

        value = math.inf
        generator = StateSpaceGenerator(state_depth[0])
        moves = generator.generate_all_valid_moves()
        next_states = generator.generate_next_states()

        for next_state in next_states:
            next_state_depth = next_state, state_depth[1] + 1
            value = min(value, self.max_value(next_state_depth, alpha, beta))
            if value <= alpha:
                self.pruned += 1
                return value
            beta = min(beta, value)

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
        heufunc = HeuristicFunctionMan(state)
        if state in self.transpos_table:
            self.table_retrieved += 1
            return self.transpos_table.get(state)  # avoids recalculating previously seen states
        # return heuristic-evaluated value of this state
        value = heufunc.heuristic_function()  # PLACEHOLDER: randomize a value
        print(value)
        self.transpos_table.update({state: value})
        return value


if __name__ == "__main__":
    from time import perf_counter
    from sys import stdout
    import logging

    # TEST: run algo with test input file
    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(stdout)])
    search_algo = AlphaBeta()
    start = perf_counter()  # TEST: start timer

    search_algo.alpha_beta_search(
        FileProcessor.get_state_from_file("../dist/test_inputs/Test2.input"))

    timer = perf_counter() - start
    logging.info(f"Time taken: {timer}, pruned: {search_algo.pruned},"
                 f" transpos_table retrieved: {search_algo.table_retrieved}")
