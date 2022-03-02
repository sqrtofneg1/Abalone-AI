from enum import Enum, auto


class Settings:
    def __init__(self, layout, colour, gamemode, move_limit, time_limit_p1, time_limit_p2):
        self.layout = layout
        self.colour = colour
        self.gamemode = gamemode
        self.move_limit = move_limit
        self.time_limit_p1 = time_limit_p1
        self.time_limit_p2 = time_limit_p2

    @staticmethod
    def default_settings():
        return Settings(1, 1, 1, 0, 0, 0)

class Layout(Enum):
    DEFAULT = auto()
    BELGIAN_DAISY = auto()
    GERMAN_DAISY = auto()


class Colour(Enum):
    BLACK = auto()
    WHITE = auto()


class Gamemode(Enum):
    HUMAN_HUMAN = auto()
    HUMAN_AI = auto()
    AI_AI = auto()
