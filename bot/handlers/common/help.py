from __future__ import annotations

from typing import TYPE_CHECKING, Final

from aiogram import Router
from aiogram.filters import Command


if TYPE_CHECKING:
    from aiogram.types import Message
    from aiogram_i18n import I18nContext

    from bot.services.database import DBUser

router: Final[Router] = Router(name=__name__)


@router.message(Command("help"), flags={"throttling_key": "default"})
async def help_command(message: Message, i18n: I18nContext, user: DBUser) -> None:
    """
    Handle the /help command.
    Show the help message.

    :param message: The message.
    :param i18n: The i18n context.
    :param user: The user.
    """
    await message.answer_photo(
        photo="https://imgur.com/BIAW92Z",
        caption=i18n.get("help", name=user.mention),
    )
