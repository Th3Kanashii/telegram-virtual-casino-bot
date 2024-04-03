from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram_i18n import I18nContext

from ..keyboards import menu

if TYPE_CHECKING:
    from ..services.database import DBUser, UoW

common_router: Final[Router] = Router(name=__name__)


@common_router.message(CommandStart(), flags={"throttling_key": "default"})
async def start_command(message: Message, i18n: I18nContext, user: DBUser, uow: UoW) -> Any:
    """
    Handle the /start command.

    :param message: The message.
    :param i18n: The i18n context.
    :param user: The user.
    :return: The response.
    """
    user.balance = 10000
    await uow.commit(user)
    return message.answer(
        text=i18n.get("start", balance=user.balance, name=user.name),
        reply_markup=menu(i18n=i18n),
    )


@common_router.message(Command("help"), flags={"throttling_key": "default"})
async def help_command(message: Message, i18n: I18nContext, user: DBUser) -> Any:
    """
    Handle the /help command.
    Show the help message.

    :param message: The message.
    :param i18n: The i18n context.
    :param user: The user.
    :return: The response.
    """
    return message.answer_photo(
        photo="https://imgur.com/BIAW92Z", caption=i18n.get("help", name=user.name)
    )
