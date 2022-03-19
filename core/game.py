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
        self.last_state = self.state  # Used for undo later?

    def start_game(self):
        pass
