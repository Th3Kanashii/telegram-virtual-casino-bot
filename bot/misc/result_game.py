from typing import Union

from ..enums import Game
from ._calculate_game import (
    calculate_basketball_football,
    calculate_dice_dart_bowling,
    calculate_slot,
)


def get_result_game(data: dict, dice: int) -> Union[int, float]:
    """
    Get the result of the game.

    :param data: The data.
    :param dice: The dice.
    :return: The win.
    """
    if data["game"] in (Game.BASKET, Game.FOOTBALL):
        is_win = calculate_basketball_football(bet_amount=data["bet"], dice_value=dice)
    elif data["game"] in (Game.DICE, Game.DARTS, Game.BOWLING):
        is_win = calculate_dice_dart_bowling(bet_amount=data["bet"], dice_value=dice)
    else:
        is_win = calculate_slot(bet_amount=data["bet"], dice_value=dice)

    return is_win
