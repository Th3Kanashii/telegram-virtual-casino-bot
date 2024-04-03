from __future__ import annotations

from enum import StrEnum, auto


class Menu(StrEnum):
    """
    Enumeration representing menu items.
    """

    GAMES = auto()
    LANGUAGE = auto()


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


class Operation(StrEnum):
    """
    Enumeration representing operations.
    """

    ADD = auto()
    SUB = auto()
    DOUBLE = auto()
    MIN = auto()
    MAX = auto()

    DEFAULT = auto()


class Back(StrEnum):
    """
    Enumeration representing back actions.
    """

    MENU = auto()
    GAME = auto()

    DEFAULT = MENU
