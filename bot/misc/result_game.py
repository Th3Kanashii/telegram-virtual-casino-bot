from typing import Union

from ..enums import Game
from ._calculate_game import (
    calculate_basketball,
    calculate_bowling,
    calculate_dart,
    calculate_dice,
    calculate_football,
    calculate_slot,
)


def get_result_game(data: dict, dice: int) -> Union[int, float]:
    """
    Get the result of the game.

    :param data: The data.
    :param dice: The dice.
    :return: The win.
    """
    if data["game"] == Game.BASKET:
        is_win = calculate_basketball(bet_amount=data["bet"], dice_value=dice)
    elif data["game"] == Game.BOWLING:
        is_win = calculate_bowling(bet_amount=data["bet"], dice_value=dice)
    elif data["game"] == Game.SLOTS:
        is_win = calculate_slot(bet_amount=data["bet"], dice_value=dice)
    elif data["game"] == Game.FOOTBALL:
        is_win = calculate_football(bet_amount=data["bet"], dice_value=dice)
    elif data["game"] == Game.DARTS:
        is_win = calculate_dart(bet_amount=data["bet"], dice_value=dice)
    else:
        is_win = calculate_dice(bet_amount=data["bet"], dice_value=dice)

    return is_win
