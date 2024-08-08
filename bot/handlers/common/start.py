from __future__ import annotations

from typing import TYPE_CHECKING, Final

from aiogram import Router
from aiogram.filters import Command, CommandStart

from bot.keyboards.inline import menu


if TYPE_CHECKING:
    from aiogram.filters import CommandObject
    from aiogram.types import Message
    from aiogram_i18n import I18nContext

    from bot.services.database import DBUser, Repository, UoW

MINIMUM_BALANCE: Final[int] = 10000

flags: Final[dict[str, str]] = {"throttling_key": "default"}
router: Final[Router] = Router(name=__name__)


@router.message(CommandStart(deep_link=True, deep_link_encoded=True), flags=flags)
async def start_deep_link_command(
    message: Message,
    command: CommandObject,
    i18n: I18nContext,
    user: DBUser,
    uow: UoW,
    repository: Repository,
) -> None:
    """
    Handle the /start command.
    Decode the deep link and give the user a bonus if they have not yet received it.

    :param message: The message.
    :param command: The command.
    :param i18n: The i18n context.
    :param user: The user.
    :param uow: The unit of work.
    :param repository: The repository.
    """
    referrer_id = int(command.args)
    if not user.refferal and user.id != referrer_id:
        refferal = await repository.user.get(user_id=referrer_id)
        refferal.balance += 10000
        user.refferal = referrer_id
        user.balance += 30000
        await uow.commit(user, refferal)

    await message.answer(
        text=i18n.get("start", balance=user.balance, name=user.mention),
        reply_markup=menu(i18n=i18n),
    )


@router.message(Command("start"), flags=flags)
async def start_command(message: Message, i18n: I18nContext, user: DBUser, uow: UoW) -> None:
    """
    Handle the /start command.
    Show the start message.

    :param message: The message.
    :param i18n: The i18n context.
    :param user: The user.
    :param uow: The unit of work.
    """
    if user.balance <= MINIMUM_BALANCE:
        user.balance += 10000
        await uow.commit(user)

    await message.answer(
        text=i18n.get("start", balance=user.balance, name=user.mention),
        reply_markup=menu(i18n=i18n),
    )
