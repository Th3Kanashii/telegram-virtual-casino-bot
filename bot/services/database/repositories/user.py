from __future__ import annotations

from sqlalchemy import func, select

from bot.services.database.models import DBUser

from .base import BaseRepository


class UserRepository(BaseRepository):
    """
    The repository for the users.
    """

    async def get(self, user_id: int) -> DBUser | None:
        """
        Get a user by their ID.

        :param user_id: The user's ID.
        :return: The user, if found.
        """
        return await self._session.scalar(select(DBUser).where(DBUser.id == user_id))

    async def count_referrals(self, user_id: int) -> int | None:
        """
        Count the number of referrals for a user.

        :param user_id: The user's ID.
        :return: The number of referrals.
        """
        return await self._session.scalar(
            select(func.count(DBUser.id)).where(DBUser.refferal == user_id)
        )
