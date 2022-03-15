import node_arrays
from settings import Settings
from state_representation import StateRepresentation


class Game:

    def __init__(self, settings=Settings.default_settings()):
        self.settings = settings
        self.state_rep = StateRepresentation.get_start_state_rep(node_arrays.STARTING_LAYOUT[settings.layout])
        self.last_state_rep = self.state_rep  # Used for undo later?
        self.turn_counter = 1

    def start_game(self):
        pass

    def apply_move(self, move):
        self.last_state_rep = self.state_rep
        self.state_rep = self.state_rep.apply_move(move)
        self.turn_counter += 1
