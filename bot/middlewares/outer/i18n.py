from __future__ import annotations

from typing import TYPE_CHECKING, Optional, cast

from aiogram.types import User
from aiogram_i18n.managers import BaseManager

if TYPE_CHECKING:
    from ...services.database import DBUser, UoW


class UserManager(BaseManager):
    """
    The user manager for the i18n middleware.
    """

    async def get_locale(
        self, event_from_user: Optional[User] = None, user: Optional[DBUser] = None
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
        :param companion: The companion to set the locale for.
        """
        user.locale = locale
        await uow.commit(user)
