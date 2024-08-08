from __future__ import annotations

from typing import TYPE_CHECKING, Final

from aiogram import F, Router

from bot.enums import Menu
from bot.keyboards.inline import Language, menu, select_language


if TYPE_CHECKING:
    from aiogram.types import CallbackQuery
    from aiogram_i18n import I18nContext

    from bot.services.database import DBUser

router: Final[Router] = Router(name=__name__)


@router.callback_query(F.data == Menu.LANGUAGE)
async def choose_a_language(callback: CallbackQuery, i18n: I18nContext, user: DBUser) -> None:
    """
    Select a language.

    :param callback: The callback query.
    :param i18n: The i18n context.
    :param user: The user.
    """
    await callback.message.edit_text(
        text=i18n.get("language", name=user.mention),
        reply_markup=select_language(i18n=i18n),
    )


@router.callback_query(Language.filter())
async def language_changed(
    callback: CallbackQuery,
    callback_data: Language,
    i18n: I18nContext,
    user: DBUser,
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
