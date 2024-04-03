from __future__ import annotations

from typing import TYPE_CHECKING

from ._calculate_game import (
    calculate_basketball_football,
    calculate_dice_dart_bowling,
    calculate_slot,
)

if TYPE_CHECKING:
    from ..services.database import DBUser


def get_result_game(data: dict, dice: int, user: DBUser) -> int:
    """
    Get the result of the game.

    :param data: The data.
    :param dice: The dice.
    :param user: The user.
    :return: The win.
    """
    if data["game"] in ("basket", "football"):
        is_win = calculate_basketball_football(bet_amount=data["bet"], dice_value=dice)
    elif data["game"] in ("dice", "darts", "bowling"):
        is_win = calculate_dice_dart_bowling(bet_amount=data["bet"], dice_value=dice)
    else:
        is_win = calculate_slot(bet_amount=data["bet"], dice_value=dice)

    user.balance += is_win
    return is_win
