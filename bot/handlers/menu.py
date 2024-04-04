from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext

from ..enums import Back, Menu
from ..keyboards import Language, games, menu, select_language

if TYPE_CHECKING:
    from ..services.database import DBUser

menu_router: Final[Router] = Router(name=__name__)


@menu_router.callback_query(F.data == Menu.GAMES)
async def choose_a_game(callback: CallbackQuery, i18n: I18nContext, user: DBUser) -> Any:
    """
    Select a game.

    :param callback: The callback query.
    :param i18n: The i18n context.
    :param user: The user.
    :return: The edited message.
    """
    return callback.message.edit_text(
        text=i18n.get("select-game", balance=user.balance), reply_markup=games(i18n=i18n)
    )


@menu_router.callback_query(F.data == Back.DEFAULT)
async def back_menu(callback: CallbackQuery, i18n: I18nContext, user: DBUser) -> Any:
    """
    Go back to the menu.

    :param callback: The callback query.
    :param i18n: The i18n context.
    :param user: The user.
    :return: The edited message.
    """
    return callback.message.edit_text(
        text=i18n.get("start", balance=user.balance, name=user.mention),
        reply_markup=menu(i18n=i18n),
    )


@menu_router.callback_query(F.data == Back.GAME)
async def back_games(callback: CallbackQuery, i18n: I18nContext, user: DBUser) -> Any:
    """
    Go back to the games.

    :param callback: The callback query.
    :param i18n: The i18n context.
    :param user: The user.
    :return: The edited message.
    """
    return callback.message.edit_text(
        text=i18n.get("select-game", balance=user.balance, name=user.mention),
        reply_markup=games(i18n=i18n),
    )


@menu_router.callback_query(F.data == Menu.LANGUAGE)
async def choose_a_language(callback: CallbackQuery, i18n: I18nContext, user: DBUser) -> Any:
    """
    Select a language.

    :param callback: The callback query.
    :param i18n: The i18n context.
    :param user: The user.
    :return: The edited message.
    """
    return callback.message.edit_text(
        text=i18n.get("language", name=user.mention), reply_markup=select_language(i18n=i18n)
    )


@menu_router.callback_query(Language.filter())
async def language_changed(
    callback: CallbackQuery, callback_data: Language, i18n: I18nContext, user: DBUser
) -> Any:
    """
    Handle the language selection callback.
    Change the user's language.

    :param callback: The callback.
    :param callback_data: The callback data.
    :param i18n: The i18n context.
    :param user: The user.
    :return: The response.
    """
    await i18n.set_locale(locale=callback_data.language)
    return callback.message.edit_text(
        text=i18n.get("start", balance=user.balance, name=user.mention),
        reply_markup=menu(i18n=i18n),
    )
