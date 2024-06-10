from __future__ import annotations

from typing import TYPE_CHECKING, Final

from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.deep_linking import create_start_link
from aiogram_i18n import I18nContext

from ...enums import Back, Menu
from ...keyboards import back_menu, games, menu, select_language

if TYPE_CHECKING:
    from ...services.database import DBUser, Repository

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
        text=i18n.get("select-game", balance=user.balance), reply_markup=games(i18n=i18n)
    )


@router.callback_query(F.data == Menu.REFERRALS)
async def refferals(
    callback: CallbackQuery, bot: Bot, i18n: I18nContext, user: DBUser, repository: Repository
) -> None:
    """
    Show the user's referrals.

    :param callback: The callback query.
    :param i18n: The i18n context.
    :param user: The user.
    """
    count = await repository.user.count_refferals(user_id=user.id)
    link = await create_start_link(bot=bot, payload=str(user.id), encode=True)
    await callback.message.edit_text(
        text=i18n.get("refferal", name=user.mention, link=link, count=count),
        reply_markup=back_menu(i18n=i18n, link=link),
    )


@router.callback_query(F.data == Menu.LANGUAGE)
async def choose_a_language(callback: CallbackQuery, i18n: I18nContext, user: DBUser) -> None:
    """
    Select a language.

    :param callback: The callback query.
    :param i18n: The i18n context.
    :param user: The user.
    """
    await callback.message.edit_text(
        text=i18n.get("language", name=user.mention), reply_markup=select_language(i18n=i18n)
    )


@router.callback_query(F.data == Back.DEFAULT)
async def back_main_menu(callback: CallbackQuery, i18n: I18nContext, user: DBUser) -> None:
    """
    Go back to the menu.

    :param callback: The callback query.
    :param i18n: The i18n context.
    :param user: The user.
    """
    await callback.message.edit_text(
        text=i18n.get("start", balance=user.balance, name=user.mention),
        reply_markup=menu(i18n=i18n),
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
