"""
This module houses the adversarial search algorithm implementation
for Abalone AI - Minimax and Alpha-Beta pruning.
"""
import math

from ai.heuristics import Heuristics
from state_space_gen.file_processor import FileProcessor
from state_space_gen.state_space_generator import StateSpaceGenerator


class AlphaBeta:
    """
    Represents an adversarial search algorithm
    using Minimax with Alpha-Beta pruning.
    """

    def __init__(self, max_time):
        """
        Initializes an object of this class.

        :param max_time: an int for seconds
        """
        self._max_time = max_time
        self._transpos_table = {}   # not working yet
        self._best_move_found = None
        self.start_time = None
        # performance trackers
        self.pruned = 0

    @property
    def max_time(self):
        """
        Returns the max time available to search.

        :return: an int
        """
        return self._max_time

    @max_time.setter
    def max_time(self, new_max):
        """
        Sets the max time to a new number.

        :param new_max: an int
        """
        self._max_time = new_max

    @property
    def transpos_table(self):
        """
        Returns the transposition table.

        :return: a dictionary
        """
        return self._transpos_table

    @property
    def best_move_found(self):
        """
        Returns the best move found so far.

        :return: a Move object
        """
        return self._best_move_found

    @best_move_found.setter
    def best_move_found(self, new_move):
        """
        Sets a new move as the best move found so far.

        :param new_move: a Move object
        """
        self._best_move_found = new_move

    def out_of_time(self):
        """
        Checks whether time has run out for searching.

        :return: True if time ran out, otherwise False
        """
        return perf_counter() - self.start_time >= self.max_time

    def start_new_search(self, state):
        """
        Resets all attributes and begins a new search.

        :param state: a State object
        :return: a Move object
        """
        self._transpos_table.clear()
        self.pruned = 0
        # self.transpos_table_hits = 0
        self.best_move_found = None
        self.start_time = perf_counter()
        return self.iter_deep_search(state)

    def iter_deep_search(self, state):
        """
        Iteratively deepens the search for the best move, returns the last best move
        found when time runs out.

        :param state: a State object
        :return: a Move object
        """
        try:
            for depth in range(1, 100):
                print(f"Depth {depth} - current timer {perf_counter() - self.start_time}")
                if self.out_of_time():
                    raise OutOfTimeException
                self.best_move_found = self.alpha_beta_search(state, depth)
        except OutOfTimeException:
            pass
        return self.best_move_found

    def alpha_beta_search(self, state, max_depth):
        """
        Returns the estimated-best-next-move the player can make using
        alpha-beta search algorithm.

        :param state: a State object
        :param max_depth: an int
        :return: a Move object
        """
        alpha, beta, value = -math.inf, math.inf, -math.inf
        generator = StateSpaceGenerator(state)
        moves = generator.generate_all_valid_moves()
        next_states = generator.generate_next_states()
        next_states_values = {}

        for next_state in next_states:
            if self.out_of_time():
                raise OutOfTimeException
            next_state_depth = next_state, 1
            value = max(value, self.min_value(next_state_depth, alpha, beta, max_depth))
            alpha = max(alpha, value)
            next_states_values.update({next_state: value})

        max_valued_moves = [moves[next_states.index(s)]
                            for s, v in next_states_values.items() if v == value]
        chosen_move = generator.sort_moves(max_valued_moves)[0]

        # TEST: log results to console
        logging.info(f"Max value: {value}\nMove: {chosen_move}")

        return chosen_move

    def max_value(self, state_depth, alpha, beta, max_depth):
        """
        For the given state, returns the highest value obtainable from the next states,
        from the current player's perspective.

        :param state_depth: a tuple with a State and an int for depth
        :param alpha: an int of the highest value found by max so far
        :param beta: an int of the lowest value found by min so far
        :param max_depth: an int
        :return: an int of the highest value obtainable from next states
        """
        if self.out_of_time():
            raise OutOfTimeException
        if state_depth[1] == max_depth:
            return self.get_value(state_depth[0])

        value = -math.inf
        generator = StateSpaceGenerator(state_depth[0])
        moves = generator.generate_all_valid_moves()
        next_states = generator.generate_next_states()

        for next_state in next_states:
            next_state_depth = next_state, state_depth[1] + 1
            value = max(value, self.min_value(next_state_depth, alpha, beta, max_depth))
            if value >= beta:
                self.pruned += 1
                return value
            alpha = max(alpha, value)

        return value

    def min_value(self, state_depth, alpha, beta, max_depth):
        """
        For the given state, returns the lowest value obtainable from the next states,
        from the current player's perspective.

        :param state_depth: a tuple with a State and an int for depth
        :param alpha: an int of the highest value found by max so far
        :param beta: an int of the lowest value found by min so far
        :param max_depth: an int
        :return: an int of the lowest value obtainable from next states
        """
        if self.out_of_time():
            raise OutOfTimeException
        if state_depth[1] == max_depth:
            return self.get_value(state_depth[0])

        value = math.inf
        generator = StateSpaceGenerator(state_depth[0])
        moves = generator.generate_all_valid_moves()
        next_states = generator.generate_next_states()

        for next_state in next_states:
            next_state_depth = next_state, state_depth[1] + 1
            value = min(value, self.max_value(next_state_depth, alpha, beta, max_depth))
            if value <= alpha:
                self.pruned += 1
                return value
            beta = min(beta, value)

        return value

    def get_value(self, state):
        """
        Returns the estimated value of this state according to heuristic functions.

        :param state: a State object
        :return: an int of the value of this state
        """
        if state in self.transpos_table.keys():
            return self.transpos_table.get(state)  # not working yet
        value = Heuristics.evaluate(state)
        self.transpos_table.update({state: value})  # not working yet
        return value


class OutOfTimeException(Exception):
    pass


if __name__ == "__main__":
    from time import perf_counter
    from sys import stdout
    import logging

    # TEST: run algo with test input file
    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(stdout)])
    alpha_beta = AlphaBeta(5)
    start = perf_counter()  # TEST: start timer

    alpha_beta.start_new_search(
        FileProcessor.get_state_from_file("../dist/test_inputs/Test1.input"))

    timer = perf_counter() - start
    logging.info(f"Time taken: {timer}, pruned: {alpha_beta.pruned}")
