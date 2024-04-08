from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload
from aiogram_i18n import I18nContext

from ..keyboards import menu

if TYPE_CHECKING:
    from ..services.database import DBUser, Repository, UoW

common_router: Final[Router] = Router(name=__name__)


@common_router.message(CommandStart(), flags={"throttling_key": "default"})
async def start_command(
    message: Message,
    command: CommandObject,
    i18n: I18nContext,
    user: DBUser,
    uow: UoW,
    repository: Repository,
) -> Any:
    """
    Handle the /start command.

    :param message: The message.
    :param command: The command.
    :param i18n: The i18n context.
    :param user: The user.
    :param uow: The unit of work.
    :param repository: The repository.
    :return: The response.
    """
    encode_id = int(decode_payload(command.args)) if command.args else None
    if command.args and user.refferal is None and user.id != encode_id:
        refferal = await repository.user.get(user_id=encode_id)
        refferal.balance += 10000
        user.refferal = encode_id
        user.balance += 30000
        await uow.commit(user, refferal)

    if user.balance <= 1000:
        user.balance += 10000
        await uow.commit(user)

    return message.answer(
        text=i18n.get("start", balance=user.balance, name=user.mention),
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
        photo="https://imgur.com/BIAW92Z", caption=i18n.get("help", name=user.mention)
    )


@common_router.message()
async def delete(message: Message) -> Any:
    """
    Delete the message.

    :param message: The message.
    """
    return message.delete()
