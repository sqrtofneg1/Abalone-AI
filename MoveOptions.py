from enum import Enum, auto


class Move(Enum):
    """
    Move notation for Abalone game.
    """

    """
    Notation for amount of marble to be moved.
    """
    S = 1, 'Single (moving a single marble)'
    D = 2, 'Double (moving a double marble)'
    T = 3, 'Triple (moving a triple marble)'

    """
    Notation for direction of movement.
    """
    L = auto(), 'Left'
    R = auto(), 'Right'
    TL = auto(), 'Top-Left'
    TR = auto(), 'Top-Right'
    BL = auto(), 'Bottom-Left'
    BR = auto(), 'Bottom-Right'
