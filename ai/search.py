"""
This module houses the adversarial search algorithm implementation
for Abalone AI - Minimax and Alpha-Beta pruning.
"""
import os
import sys

sys.path.append(os.path.realpath('..'))
from time import perf_counter
from state_space_gen.file_processor import FileProcessor
from state_space_gen.state_space_generator import StateSpaceGenerator


class AlphaBeta:
    """
    Represents an adversarial search algorithm
    using Minimax with Alpha-Beta pruning.
    """

    def __init__(self, max_time=5):
        """
        Initializes an object of this class.

        :param max_time: an int of the max time to search
        """
        self._max_time = max_time
        self._best_move_found = None
        self.start_time = None
        # performance trackers
        self.pruned = 0

    @property
    def max_time(self):
        """
        Returns the max time allowed for this search.

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

    def start_new_search(self, state, heuristic_func):
        """
        Resets all attributes and begins a new search.

        :param state: a State object
        :param heuristic_func: the heuristic to use
        :return: a Move object
        """
        func_name = str(heuristic_func).split(" ", 3)[-2]
        print(f"Starting search with {func_name}")
        self.pruned = 0
        self.best_move_found = None
        self.start_time = perf_counter()
        return self.iter_deep_search(state, heuristic_func)

    def iter_deep_search(self, state, heuristic_func):
        """
        Iteratively deepens the search for the best move, returns the last best move
        found when time runs out.

        :param state: a State object
        :param heuristic_func: the heuristic to use
        :return: a Move object
        """
        try:
            for depth in range(1, 100):
                print(f"Depth {depth} - current timer {perf_counter() - self.start_time}")
                if self.out_of_time():
                    raise OutOfTimeException
                self.best_move_found = self.alpha_beta_search(state, depth, heuristic_func)
        except OutOfTimeException:
            pass
        return self.best_move_found

    def alpha_beta_search(self, state, max_depth, heuristic_func):
        """
        Returns the estimated-best-next-move the player can make using
        alpha-beta search algorithm.

        :param state: a State object
        :param max_depth: an int of the max depth to search to
        :param heuristic_func: the heuristic function to use
        :return: a Move object
        """
        alpha, beta, value = float('-inf'), float('inf'), float('-inf')
        generator = StateSpaceGenerator(state)
        moves = generator.generate_all_valid_moves()
        next_states = generator.generate_next_states()
        next_states_values = {}

        for next_state in next_states:
            if self.out_of_time():
                raise OutOfTimeException
            next_state_depth = next_state, 1
            value = max(value, self.min_value(next_state_depth, alpha, beta, max_depth, heuristic_func))
            alpha = max(alpha, value)
            next_states_values.update({next_state: value})

        max_valued_moves = [moves[next_states.index(s)]
                            for s, v in next_states_values.items() if v == value]
        chosen_move = max_valued_moves[0]

        # TEST: log results to console
        # print(f"Max value: {value}\nMove: {chosen_move}")

        return chosen_move

    def max_value(self, state_depth, alpha, beta, max_depth, heuristic_func):
        """
        For the given state, returns the highest value obtainable from the next states,
        from the current player's perspective.
        :param state_depth: a tuple with a State and an int for depth
        :param alpha: an int of the highest value found by max so far
        :param beta: an int of the lowest value found by min so far
        :param max_depth: an int of the max depth to search to
        :param heuristic_func: the heuristic function to use
        :return: an int of the highest value obtainable from next states
        """
        if self.out_of_time():
            raise OutOfTimeException
        if state_depth[1] == max_depth:
            return self.get_value(state_depth[0], heuristic_func)

        value = float('-inf')
        generator = StateSpaceGenerator(state_depth[0])
        next_states = generator.generate_state_space()

        for next_state in next_states:
            next_state_depth = next_state, state_depth[1] + 1
            value = max(value, self.min_value(next_state_depth, alpha, beta, max_depth, heuristic_func))
            if value >= beta:
                self.pruned += 1
                return value
            alpha = max(alpha, value)

        return value

    def min_value(self, state_depth, alpha, beta, max_depth, heuristic_func):
        """
        For the given state, returns the lowest value obtainable from the next states,
        from the current player's perspective.
        :param state_depth: a tuple with a State and an int for depth
        :param alpha: an int of the highest value found by max so far
        :param beta: an int of the lowest value found by min so far
        :param max_depth: an int of the max depth to search to
        :param heuristic_func: the heuristic function to use
        :return: an int of the lowest value obtainable from next states
        """
        if self.out_of_time():
            raise OutOfTimeException
        if state_depth[1] == max_depth:
            return self.get_value(state_depth[0], heuristic_func)

        value = float('inf')
        generator = StateSpaceGenerator(state_depth[0])
        next_states = generator.generate_state_space()

        for next_state in next_states:
            next_state_depth = next_state, state_depth[1] + 1
            value = min(value, self.max_value(next_state_depth, alpha, beta, max_depth, heuristic_func))
            if value <= alpha:
                self.pruned += 1
                return value
            beta = min(beta, value)

        return value

    @staticmethod
    def get_value(state, heuristic_func):
        """
        Returns the estimated value of this state according to heuristic functions.

        :param state: a State object
        :param heuristic_func: the function of the heuristic
        :return: an int of the value of this state
        """
        # return heuristic-evaluated value of this state
        value = heuristic_func(state)
        return value


class OutOfTimeException(Exception):
    pass


if __name__ == "__main__":
    from ai.heuristics import Heuristics

    # TEST: run algo with test input file
    search_algo = AlphaBeta(2)

    heuristic = Heuristics.evaluate

    print("\nTest1.input")
    start = perf_counter()  # TEST: start timer
    search_algo.start_new_search(
        FileProcessor.get_state_from_file("../dist/test_inputs/Test1.input"), heuristic)
    timer = perf_counter() - start
    print(f"Time taken: {timer}, pruned: {search_algo.pruned}")

    print("\nTest2.input")
    start = perf_counter()  # TEST: start timer
    search_algo.start_new_search(
        FileProcessor.get_state_from_file("../dist/test_inputs/Test2.input"), heuristic)
    timer = perf_counter() - start
    print(f"Time taken: {timer}, pruned: {search_algo.pruned}")

    print("\nTest3.input")
    start = perf_counter()  # TEST: start timer
    search_algo.start_new_search(
        FileProcessor.get_state_from_file("../dist/test_inputs/Test3.input"), heuristic)
    timer = perf_counter() - start
    print(f"Time taken: {timer}, pruned: {search_algo.pruned}")
