from __future__ import annotations

from typing import TYPE_CHECKING, cast

from aiogram_i18n.managers import BaseManager


if TYPE_CHECKING:
    from aiogram.types import User

    from bot.services.database import DBUser, UoW


class UserManager(BaseManager):
    """
    The user manager for the i18n middleware.
    """

    async def get_locale(
        self,
        event_from_user: User | None = None,
        user: DBUser | None = None,
    ) -> str:
        """
        Get the user's locale.

        :param event_from_user: The user from the event.
        :param user: The user from the database.
        :return: The user's locale.
        """
        if user:
            return user.locale
        if event_from_user and event_from_user.language_code is not None:
            return event_from_user.language_code
        return cast(str, self.default_locale)

    async def set_locale(self, locale: str, user: DBUser, uow: UoW) -> None:
        """
        Set the user's locale.

        :param locale: The locale to set.
        :param user: The user to set the locale for.
        :param uow: The unit of work.
        """
        user.locale = locale
        await uow.commit(user)
