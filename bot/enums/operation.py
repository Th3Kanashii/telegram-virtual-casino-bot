from enum import StrEnum, auto


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
