"""
This module houses the implementation of heuristic
functions, which are used to evaluate the desirability
of any given game state from one player's perspective.
"""
import os
import sys

sys.path.append(os.path.realpath('..'))
from core.move import Direction


class HeuristicsBach:
    w_center, w_group, w_score = 3, 6, 100

    @staticmethod
    def get_both_players_nodes(state):
        """
        Returns a list containing nodes for both players.

        :param state: a State object
        :return: a list of Nodes
        """
        return [node for row in state.board for node in row
                if node.node_value.value == 1 or node.node_value.value == 2]

    @staticmethod
    def get_distance_to_center(node):
        """
        Returns the distance between given node to the center of the board.

        :param node: a Node object
        :return: an int between 0 and 4 inclusive
        """
        return abs(5 - node.row) + abs(5 - node.column)

    @staticmethod
    def get_adjacent_allies(state, node, player):
        """
        Returns the adjacent marbles for the same player.

        :param state: a State object
        :param node: a Node object
        :param player: an int
        :return: an list of
        """
        adj_nodes = [state.get_node_in_direction_of_node(node, direction)
                     for direction in Direction]
        return [node for node in adj_nodes if node.node_value.value == player]

    @staticmethod
    def get_adjacent_enemies(state, node, player):
        """
        Counts the number of adjacent marbles for the same player.

        :param state: a State object
        :param node: a Node object
        :param player: an int
        :return: an int
        """
        return len([1 for direction in Direction if state
                   .get_node_in_direction_of_node(node, direction).node_value.value == player])

    @classmethod
    def evaluate(cls, state):
        centering = cls.w_center * cls.eval_centering(state)
        grouping = cls.w_group * cls.eval_grouping(state)
        scoring = cls.w_score * cls.eval_scoring(state)
        return centering + grouping + scoring

    @classmethod
    def eval_centering(cls, state):
        ally_ratio, enemy_ratio = 1, 1
        total = 0
        both_players_nodes = cls.get_both_players_nodes(state)
        for node in both_players_nodes:
            if node.node_value.value == state.player:
                total += ally_ratio * (12.0 / (cls.get_distance_to_center(node) + 1.0))
            else:
                total -= enemy_ratio * (12.0 / (cls.get_distance_to_center(node) + 1.0))
        return total

    @classmethod
    def eval_grouping(cls, state):
        ally_ratio, enemy_ratio = 1, 1
        total = 0
        other_player = state.get_other_player_num(state.player)
        both_players_nodes = cls.get_both_players_nodes(state)
        for node in both_players_nodes:
            if node.node_value.value == state.player:
                total += ally_ratio * len(cls.get_adjacent_allies(state, node, state.player)) * 2
            else:
                total -= enemy_ratio * len(cls.get_adjacent_allies(state, node, other_player)) * 2
        return total

    @classmethod
    def eval_scoring(cls, state):
        ally_ratio, enemy_ratio = 1, 1
        ally_count = 14 - state.scores[0]
        enemy_count = 14 - state.scores[1]
        total = ally_ratio * ally_count - enemy_ratio * enemy_count
        return total


class HeuristicsMan:
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


class HeuristicsSunmin:

    @classmethod
    def heuristic(cls, state):
        h = 0
        self_nodes = state.get_all_nodes_for_player(state.player)
        opp_nodes = state.get_all_nodes_for_player(state.get_other_player_num(state.player))
        h += len(self_nodes) * 80
        h -= len(opp_nodes) * 80
        for node in self_nodes:
            h += HeuristicsSunmin.centerness_value(node)
            h += HeuristicsSunmin.togetherness_value(state, node, state.player)
        for node in opp_nodes:
            h -= HeuristicsSunmin.centerness_value(node)
            h -= HeuristicsSunmin.togetherness_value(state, node, state.get_other_player_num(state.player))
        return h

    @staticmethod
    def centerness_value(node):
        horizontal_centerness = abs(7.5 - ((9 - (9 - node.row)) / 2 + node.column))
        vertical_centerness = abs(5 - node.row)
        return (6 - horizontal_centerness) * (6 - horizontal_centerness) + \
               (6 - vertical_centerness) * (6 - vertical_centerness)

    @staticmethod
    def togetherness_value(state, node, player):
        value = 0
        for direction in Direction.left_directions():
            node_front = state.get_node_in_direction_of_node(node, direction)
            node_back = state.get_node_in_opposite_direction_of_node(node, direction)
            if node_front.node_value.value == player & node_back.node_value.value == player:
                value += 2
            else:
                if node_front.node_value.value == player | node_back.node_value.value == player:
                    value += 0.75
                if node_front.node_value.value == 0 | node_back.node_value.value == 0:
                    value -= 2
        if (value == 6) | (value == 0):
            value += 2
        return value
