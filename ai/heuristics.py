"""
This module houses the implementation of heuristic
functions, which are used to evaluate the desirability
of any given game state from one player's perspective.
"""
import sys,os
sys.path.append(os.path.realpath('..'))
from core.node import NodeValue


class HeuristicFunctionMan:
    PUSH_OPPONENT_MARBLE_OFF_BOARD_VALUE = 100
    GAME_BOARD_VALUES_PLAYER = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
                                [0, 0, 0, 0, 1, 2, 2, 2, 2, 1, 0],
                                [0, 0, 0, 1, 2, 3, 3, 3, 2, 1, 0],
                                [0, 0, 1, 2, 3, 4, 4, 3, 2, 1, 0],
                                [0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0],
                                [0, 1, 2, 3, 4, 4, 3, 2, 1, 0, 0],
                                [0, 1, 2, 3, 3, 3, 2, 1, 0, 0, 0],
                                [0, 1, 2, 2, 2, 2, 1, 0, 0, 0, 0],
                                [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    GAME_BOARD_VALUES_OPPONENT = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, -20, -20, -20, -20, -20, 0],
                                  [0, 0, 0, 0, -20, -8, -8, -8, -8, -20, 0],
                                  [0, 0, 0, -20, -8, 5, 5, 5, -8, -20, 0],
                                  [0, 0, -20, -8, -5, -2, -2, -5, -8, -20, 0],
                                  [0, -20, -8, -5, -2, -1, -2, -5, -8, -20, 0],
                                  [0, -20, -8, -5, -2, -2, -5, -8, -20, 0, 0],
                                  [0, -20, -8, -5, -5, -5, -8, -20, 0, 0, 0],
                                  [0, -20, -8, -8, -8, -8, -20, 0, 0, 0, 0],
                                  [0, -20, -20, -20, -20, -20, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    def __init__(self, state):
        self._state = state

    def heuristic_function(self):
        game_board_player_values = self.GAME_BOARD_VALUES_PLAYER
        game_board_opponent_values = self.GAME_BOARD_VALUES_OPPONENT
        value = 0
        player = self._state.player

        if player == 1:
            opponent_player = 2
        else:
            opponent_player = 1

        set_of_player_nodes = self._state.get_all_nodes_for_player(player)
        set_of_opponent_nodes = self._state.get_all_nodes_for_player(opponent_player)

        # This code below checks to see if the player has more marbles than that of the opponents. This will make the AI
        # pick states where this is true so that it will lead to them to pushing marbles off the board.
        if self._state.get_nodes_count_for_player(player) > \
                self._state.get_nodes_count_for_player(opponent_player):
            value = value + self.PUSH_OPPONENT_MARBLE_OFF_BOARD_VALUE

        # The bottom 4 lines of codes will search for the player's nodes, extract their coordinates (rows and columns),
        # and then insert them into the GAME_BOARD_VALUE_PLAYER 2D array to find how much their positions are worth and
        # add the sum total of their worth to the value. This will goad the AI to move their marbles to the center
        # (which) is considered the safest/strategic position in the board.
        list_of_row_and_column_of_player_nodes = [[node.row, node.column] for node in set_of_player_nodes]
        list_of_player_nodes__game_board_values = [game_board_player_values[row_and_column[0]][row_and_column[1]]
                                                   for row_and_column in list_of_row_and_column_of_player_nodes]
        value = value + sum(list_of_player_nodes__game_board_values)

        # The bottom 4 lines of codes is pretty much the same as the above 4 lines but with the opponent's marbles with
        # the GAME_BOARD_VALUE_OPPONENT 2D array. This array has bigger values near the border of the board and smaller
        # values as you get closer to the center (The complete opposite of GAME_BOARD_VALUE_PLAYER). This behaviour will
        # persuade the AI to push the opponents marbles to the borders.
        list_of_row_and_column_of_opponents_nodes = [[node.row, node.column] for node in set_of_opponent_nodes]
        list_of_opponents_nodes__game_board_values = [game_board_opponent_values[row_and_column[0]][row_and_column[1]]
                                                      for
                                                      row_and_column in list_of_row_and_column_of_opponents_nodes]
        value = value + sum(list_of_opponents_nodes__game_board_values)

        return value
