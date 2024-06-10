from __future__ import annotations

from typing import TYPE_CHECKING, Final

from aiogram import Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload
from aiogram_i18n import I18nContext

from ...keyboards import menu

if TYPE_CHECKING:
    from ...services.database import DBUser, Repository, UoW

router: Final[Router] = Router(name=__name__)


@router.message(CommandStart(), flags={"throttling_key": "default"})
async def start_command(
    message: Message,
    command: CommandObject,
    i18n: I18nContext,
    user: DBUser,
    uow: UoW,
    repository: Repository,
) -> None:
    """
    Handle the /start command.

    :param message: The message.
    :param command: The command.
    :param i18n: The i18n context.
    :param user: The user.
    :param uow: The unit of work.
    :param repository: The repository.
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

    await message.answer(
        text=i18n.get("start", balance=user.balance, name=user.mention),
        reply_markup=menu(i18n=i18n),
    )
