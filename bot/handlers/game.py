from __future__ import annotations

import asyncio
import secrets
from typing import TYPE_CHECKING, Any, Dict, Final

from aiogram import F, Router
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext

from ..enums import Game
from ..keyboards import Bet, Games, play
from ..misc import get_operation_snippet, get_result_game

if TYPE_CHECKING:
    from ..services.database import DBUser, UoW

dices: Final[Dict[Game, DiceEmoji]] = {
    Game.DICE: DiceEmoji.DICE,
    Game.FOOTBALL: DiceEmoji.FOOTBALL,
    Game.BASKET: DiceEmoji.BASKETBALL,
    Game.DARTS: DiceEmoji.DART,
    Game.BOWLING: DiceEmoji.BOWLING,
    Game.SLOTS: DiceEmoji.SLOT_MACHINE,
}
game_router: Final[Router] = Router(name=__name__)


@game_router.callback_query(Games.filter())
async def selected_game(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: Games,
    i18n: I18nContext,
    user: DBUser,
) -> Any:
    """
    Select a bet.

    :param callback: The callback query.
    :param callback_data: The callback data.
    :param i18n: The i18n context.
    :param user: The user.
    :param state: The FSM state.
    :return: The edited message.
    """
    await state.update_data(game=callback_data.game, bet=10)
    return callback.message.edit_text(
        text=i18n.get(callback_data.game, balance=user.balance),
        reply_markup=play(i18n=i18n, game=callback_data.game),
    )


@game_router.callback_query(Bet.filter())
async def bet(
    callback: CallbackQuery, state: FSMContext, callback_data: Bet, i18n: I18nContext
) -> Any:
    """
    Change the bet.

    :param callback: The callback query.
    :param state: The FSM state.
    :param callback_data: The callback data.
    :param i18n: The i18n context.
    :return: The edited message.
    """
    data = await state.get_data()
    get_operation_snippet(data=data, operation=callback_data.operation)

    await state.update_data(data)
    return callback.message.edit_reply_markup(
        reply_markup=play(i18n=i18n, game=data["game"], bet=data["bet"])
    )


@game_router.callback_query(F.data.endswith(Game.PLAY))
async def play_game(
    callback: CallbackQuery, state: FSMContext, i18n: I18nContext, user: DBUser, uow: UoW
) -> Any:
    """
    Play the game.

    :param callback: The callback query.
    :param state: The FSM state.
    :param i18n: The i18n context.
    :param user: The user.
    :param uow: The unit of work.
    :return: The edited message.
    """
    data = await state.get_data()
    if user.balance < data["bet"]:
        return callback.message.edit_text(text=i18n.get("zero-balance"))

    result: Message = await callback.message.edit_text(i18n.get("good-luck"))
    dice: Message = await callback.message.answer_dice(emoji=dices[data["game"]])

    number = get_result_game(data=data, dice=dice.dice.value, user=user)
    lose = secrets.choice(i18n.get("lose").split(","))
    await asyncio.sleep(2)

    await uow.commit(user)
    await result.edit_text(
        text=i18n.get("win", number=number - data["bet"]) if number > 0 else lose
    )

    return callback.message.answer(
        text=i18n.get(data["game"], balance=user.balance),
        reply_markup=play(i18n=i18n, game=data["game"], bet=data["bet"]),
    )
