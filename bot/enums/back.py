from enum import StrEnum, auto


class Back(StrEnum):
    """
    Enumeration representing back actions.
    """

    MENU = auto()
    GAME = auto()

    DEFAULT = MENU
