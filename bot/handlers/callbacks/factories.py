from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, Final

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext

from ...keyboards import Bet, Games, Language, menu, play
from ...misc import get_operation_snippet

if TYPE_CHECKING:
    from ...services.database import DBUser

router: Final[Router] = Router(name=__name__)


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
    callback: CallbackQuery, state: FSMContext, callback_data: Bet, i18n: I18nContext
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
            reply_markup=play(i18n=i18n, game=data["game"], bet=data["bet"])
        )


@router.callback_query(Language.filter())
async def language_changed(
    callback: CallbackQuery, callback_data: Language, i18n: I18nContext, user: DBUser
) -> None:
    """
    Handle the language selection callback.
    Change the user's language.

    :param callback: The callback.
    :param callback_data: The callback data.
    :param i18n: The i18n context.
    :param user: The user.
    """
    await i18n.set_locale(locale=callback_data.language)
    await callback.message.edit_text(
        text=i18n.get("start", balance=user.balance, name=user.mention),
        reply_markup=menu(i18n=i18n),
    )
