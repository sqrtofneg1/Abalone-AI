"""
This module houses the Game class.
"""
from layouts import layout_arrays
from gui.settings import Settings
from core.state import State


class Game:
    """
    Represents the game itself, which has settings, the current state,
    and the previous state.
    """

    def __init__(self, settings=Settings.default_settings()):
        """
        Initializes a Game object.

        :param settings: a Settings object
        """
        self.settings = settings
        self.state = State.get_start_state(layout_arrays.STARTING_LAYOUT[settings.layout])
        self.last_state = self.state
        self.turn_counter = 1

    def start_game(self):
        pass

    def apply_move(self, move):
        """
        Applies the given move and progresses the states.

        :param move: a Move object
        :return: None
        """
        self.last_state = self.state
        self.state = self.state.apply_move(move)
        self.turn_counter += 1
