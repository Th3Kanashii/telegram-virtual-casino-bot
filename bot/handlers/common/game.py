from __future__ import annotations

import asyncio
import secrets
from contextlib import suppress
from typing import TYPE_CHECKING, Final

from aiogram import F, Router
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.exceptions import TelegramBadRequest

from bot.enums import Back, Game, Menu
from bot.keyboards.inline import Bet, Games, games, play
from bot.misc import calculate_game_result, get_operation_snippet


if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext
    from aiogram.types import CallbackQuery, Message
    from aiogram_i18n import I18nContext

    from bot.services.database import DBUser, UoW

DICES: Final[dict[Game, DiceEmoji]] = {
    Game.DICE: DiceEmoji.DICE,
    Game.FOOTBALL: DiceEmoji.FOOTBALL,
    Game.BASKET: DiceEmoji.BASKETBALL,
    Game.DARTS: DiceEmoji.DART,
    Game.BOWLING: DiceEmoji.BOWLING,
    Game.SLOTS: DiceEmoji.SLOT_MACHINE,
}
router: Final[Router] = Router(name=__name__)


@router.callback_query(F.data == Menu.GAMES)
async def choose_a_game(callback: CallbackQuery, i18n: I18nContext, user: DBUser) -> None:
    """
    Select a game.

    :param callback: The callback query.
    :param i18n: The i18n context.
    :param user: The user.
    """
    await callback.message.edit_text(
        text=i18n.get("select-game", balance=user.balance),
        reply_markup=games(i18n=i18n),
    )


@router.callback_query(F.data == Back.GAME)
async def back_games(callback: CallbackQuery, i18n: I18nContext, user: DBUser) -> None:
    """
    Go back to the games.

    :param callback: The callback query.
    :param i18n: The i18n context.
    :param user: The user.
    """
    await callback.message.edit_text(
        text=i18n.get("select-game", balance=user.balance, name=user.mention),
        reply_markup=games(i18n=i18n),
    )


@router.callback_query(Games.filter())
async def selected_game(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: Games,
    i18n: I18nContext,
    user: DBUser,
) -> None:
    """
    Select a bet.

    :param callback: The callback query.
    :param callback_data: The callback data.
    :param i18n: The i18n context.
    :param user: The user.
    :param state: The FSM state.
    """
    await state.update_data(game=callback_data.game, bet=10)
    await callback.message.edit_text(
        text=i18n.get(callback_data.game, balance=user.balance),
        reply_markup=play(i18n=i18n, game=callback_data.game),
    )


@router.callback_query(Bet.filter())
async def bet(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: Bet,
    i18n: I18nContext,
) -> None:
    """
    Change the bet.

    :param callback: The callback query.
    :param state: The FSM state.
    :param callback_data: The callback data.
    :param i18n: The i18n context.
    """
    data = await state.get_data()
    get_operation_snippet(data=data, operation=callback_data.operation)
    await state.update_data(data)

    with suppress(TelegramBadRequest):
        await callback.message.edit_reply_markup(
            reply_markup=play(i18n=i18n, game=data["game"], bet=data["bet"]),
        )


@router.callback_query(F.data == Game.PLAY)
async def play_game(
    callback: CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
    user: DBUser,
    uow: UoW,
) -> None:
    """
    Play the game.

    :param callback: The callback query.
    :param state: The FSM state.
    :param i18n: The i18n context.
    :param user: The user.
    :param uow: The unit of work.
    """
    data = await state.get_data()
    if user.balance < data["bet"]:
        await callback.message.edit_text(text=i18n.get("zero-balance"))
        return

    game: Message = await callback.message.edit_text(i18n.get("good-luck"))
    dice: Message = await callback.message.answer_dice(emoji=DICES[data["game"]])

    result = calculate_game_result(
        game=data["game"],
        bet_amount=data["bet"],
        dice_value=dice.dice.value,
    )
    lose = secrets.choice(i18n.get("lose").split(","))
    await asyncio.sleep(2)

    user.balance += round(result)
    await uow.commit(user)
    await game.edit_text(text=i18n.get("win", number=result - data["bet"]) if result > 0 else lose)
    await callback.message.answer(
        text=i18n.get(data["game"], balance=user.balance),
        reply_markup=play(i18n=i18n, game=data["game"], bet=data["bet"]),
    )
