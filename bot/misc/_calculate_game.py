from functools import lru_cache
from typing import Any, Dict, Union


@lru_cache(maxsize=64)
def calculate_slot(bet_amount: int, dice_value: int) -> int:
    """
    Checks for the winning combination

    :param dice_value: dice value (1-64)
    :return: user score change (integer)
    """
    win_multipliers: Dict[int, int] = {1: 4, 22: 4, 43: 4, 16: 3, 32: 3, 48: 3, 64: 5}
    return bet_amount * win_multipliers.get(dice_value, -1)


@lru_cache(maxsize=64)
def calculate_basketball_football(bet_amount: int, dice_value: int) -> Union[int, float]:
    """
    Determines the winning amount for the user's bet.

    :param bet_amount: The amount the user has bet.
    :param dice_value: The value rolled on the dice (1-5).
    :return: The amount won by the user.
    """
    win_multipliers: Dict[int, float] = {4: 1.5, 5: 2.5}
    return bet_amount * win_multipliers.get(dice_value, -1)


@lru_cache(maxsize=64)
def calculate_dice_dart_bowling(bet_amount: int, dice_value: int) -> Union[int, float]:
    """
    Determines the winning amount for the user's bet.

    :param bet_amount: The amount the user has bet.
    :param dice_value: The value rolled on the dice (1-6).
    :return: The amount won by the user.
    """
    win_multipliers: Dict[int, Any] = {4: 1.5, 5: 2, 6: 3}
    return bet_amount * win_multipliers.get(dice_value, -1)
