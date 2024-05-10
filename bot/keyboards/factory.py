from aiogram.filters.callback_data import CallbackData


class Language(CallbackData, prefix="language"):
    """
    Language callback data
    """

    language: str


class Games(CallbackData, prefix="game"):
    """
    Games callback data
    """

    game: str


class Bet(CallbackData, prefix="bet"):
    """
    Bet callback data
    """

    operation: str
