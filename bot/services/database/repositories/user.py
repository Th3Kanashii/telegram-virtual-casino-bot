from typing import Optional, cast

from sqlalchemy import select

from ..models import DBUser
from .base import BaseRepository


class UserRepository(BaseRepository):
    """
    The repository for the users.
    """

    async def get(self, user_id: int) -> Optional[DBUser]:
        """
        Get a user by their ID.

        :param user_id: The user's ID.
        :return: The user, if found.
        """
        return cast(
            Optional[DBUser],
            await self._session.scalar(select(DBUser).where(DBUser.id == user_id)),
        )
