"""
This module houses the implementation of heuristic
functions, which are used to evaluate the desirability
of any given game state from one player's perspective.
"""
from core.move import Direction


class Heuristics:
    """

    """

    w_center, w_group, w_score, w_threat = 3, 3, 5, 1

    @staticmethod
    def get_player_nodes(state):
        """
        Returns a list containing only nodes for both players.

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
        other_player = state.get_other_player_num(state.player)
        centering = cls.w_center * cls.eval_centering(state)
        grouping = cls.w_group * cls.eval_grouping(state)
        scoring = cls.w_score * cls.eval_scoring(state)
        return centering + grouping + scoring

    @classmethod
    def eval_centering(cls, state):
        ally_ratio, enemy_ratio = 1, 1
        total = 0
        player_nodes = cls.get_player_nodes(state)
        for node in player_nodes:
            if node.node_value.value == state.player:
                total += ally_ratio * (12 / (cls.get_distance_to_center(node) + 2))
            else:
                total -= enemy_ratio * (12 / (cls.get_distance_to_center(node) + 2))
        return total

    @classmethod
    def eval_grouping(cls, state):
        ally_ratio, enemy_ratio = 1, 1
        total = 0
        other_player = state.get_other_player_num(state.player)
        player_nodes = cls.get_player_nodes(state)
        for node in player_nodes:
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
