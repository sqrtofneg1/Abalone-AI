import node_arrays
from settings import Settings
from state_representation import StateRepresentation


class Game:

    def __init__(self, settings=Settings.default_settings()):
        self.settings = settings
        self.state_rep = StateRepresentation.get_start_state_rep(node_arrays.STARTING_LAYOUT[settings.layout])
        self.last_state_rep = self.state_rep  # Used for undo later?

    def start_game(self):
        pass
