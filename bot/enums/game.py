from enum import StrEnum, auto


class Game(StrEnum):
    """
    Enumeration representing games.
    """

    SLOTS = auto()
    DICE = auto()
    BASKET = auto()
    DARTS = auto()
    BOWLING = auto()
    FOOTBALL = auto()

    PLAY = auto()
