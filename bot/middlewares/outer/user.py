from __future__ import annotations

from typing import TYPE_CHECKING, Any, Awaitable, Callable, cast

from aiogram import BaseMiddleware

from bot.services.database import DBUser


if TYPE_CHECKING:
    from aiogram.types import Chat, TelegramObject, User
    from aiogram_i18n import I18nMiddleware

    from bot.services.database import Repository, UoW


class UserMiddleware(BaseMiddleware):
    """
    Middleware for handling users.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        aiogram_user: User | None = data.get("event_from_user")
        chat: Chat | None = data.get("event_chat")
        if aiogram_user is None or chat is None or aiogram_user.is_bot:
            return await handler(event, data)

        repository: Repository = data["repository"]
        user: DBUser | None = await repository.user.get(user_id=aiogram_user.id)
        if user is None:
            i18n: I18nMiddleware = data["i18n_middleware"]
            uow: UoW = data["uow"]
            user = DBUser.from_aiogram(
                user=aiogram_user,
                locale=(
                    aiogram_user.language_code
                    if aiogram_user.language_code in i18n.core.available_locales
                    else cast(str, i18n.core.default_locale)
                ),
            )
            await uow.commit(user)

        data["user"] = user
        return await handler(event, data)
