from typing import Callable, Dict, Union

from ..enums import Game


def calculate_game_result(game: Game, bet_amount: int, dice_value: int) -> Union[int, float]:
    """
    Calculate the result of a game based on the game, the bet amount and the dice value.

    :param game: The game to calculate the result for.
    :param bet_amount: The amount of money bet.
    :param dice_value: The value of the dice.
    :return: The result of the game.
    """
    game_calculators: Dict[Game, Callable[[int, int], Union[int, float]]] = {
        Game.BASKET: lambda bet, dice: bet * {4: 1.5, 5: 2.5}.get(dice, -1),
        Game.BOWLING: lambda bet, dice: bet * {5: 1.5, 6: 5}.get(dice, -1),
        Game.SLOTS: lambda bet, dice: bet * {1: 4, 22: 4, 43: 4, 16: 3, 32: 3, 48: 3, 64: 5}.get(dice, -1),
        Game.FOOTBALL: lambda bet, dice: bet * {3: 1.5, 4: 1.5, 5: 1.5}.get(dice, -1),
        Game.DARTS: lambda bet, dice: bet * {4: 1, 5: 1.5, 6: 2}.get(dice, -1),
        Game.DICE: lambda bet, dice: bet * {4: 1.5, 5: 2, 6: 3}.get(dice, -1),
    }

    return game_calculators[game](bet_amount, dice_value)
